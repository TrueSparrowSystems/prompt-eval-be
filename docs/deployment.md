# Deploy an Application to AWS

AWS is where we have set up our application. The following document provides a clear explanation of the necessary components for launching applications on AWS that run on Kubernetes.  If you have already provisioned a Kubernetes cluster on EKS using Terraform, jump right into CI/CD section.

### Contents:

- **[Install Terraform](https://www.notion.so/Deploy-an-Application-to-AWS-4603994803e84783b2f966972ff1d17c?pvs=21)**
- [**Terraform Code for Provisioning AWS EKS**](https://www.notion.so/Deploy-an-Application-to-AWS-4603994803e84783b2f966972ff1d17c?pvs=21)
- **CI/CD**

### Install Terraform

To leverage infrastructure-as-code (IaC), we will install Terraform. This tool allows us to manage infrastructure in a code-centric manner.

The following link provides detailed instructions on how to install Terraform on your system

[Install Terraform | Terraform | HashiCorp Developer](https://developer.hashicorp.com/terraform/tutorials/gcp-get-started/install-cli)

Additionally, we strongly advise creating a [Terraform Cloud Account](https://app.terraform.io/session). By doing so, the infrastructure provisioning process will be handled by Terraform Cloud,  eliminating the burden on your personal computer's bandwidth. Terraform Cloud maintains a state file that tracks the latest infrastructure setup, including the provisioned components.

**Note: Connection drop during infrastructure provisioning may result in a lock on the state file, leading to various issues. Terraform Cloud helps in avoiding such situations.**

### Terraform Code for Provisioning AWS EKS

Now that all the necessary prerequisites have been successfully set up, let's start looking into the Terraform code.

To begin, we will create a local values that will be utilized for our infrastructure. Feel free to modify the values according to your specific requirements.

```jsx
locals {
  tags = {
    "Project"         = var.name
    "Environment"     = var.environment
    "Provisioned Via" = "Terraform"
    "Team"            = "DevOps"
  }
  azs          = data.aws_availability_zones.available.names
  cluster_name = "${var.name}-${var.environment}"
  domain_name  = var.domain_name
  region       = var.region

  aws_auth_users = [for username in values(data.aws_iam_user.all) : {
    userarn  = username.arn
    username = username.user_name
    groups   = ["system:masters"]
  }]

  aws_auth_roles = [for username in values(data.aws_iam_role.all) : {
    rolearn  = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/${username.name}"
    username = "{{SessionName}}"
    groups   = ["system:masters"]
  }]

  route53_zone_ids = [
    for i in data.awscc_route53_hosted_zones.this.ids : "arn:aws:route53:::hostedzone/${i}"
  ]
}
```

Define some data sources. The below mentioned data sources fetches a few information such the availability zones for example: us-east-2a, us-east-2b etc. considering the AWS Region is us-east-2 or Ohio. Few other data sources such as Route53 Zone IDs which is related to DNS mapping, partitions and the details about the user running the Terraform code are also being fetched which we will be using internally. 

```jsx
data "aws_availability_zones" "available" {
  state         = "available"
  exclude_names = var.availability_zones_exclude

}

data "aws_region" "current" {}

data "aws_caller_identity" "current" {}

data "aws_partition" "current" {}

data "awscc_route53_hosted_zones" "this" {}

data "aws_route53_zone" "this" {
  name = var.domain_name
}

data "aws_iam_user" "all" {
  for_each  = toset(var.aws_auth_users)
  user_name = each.key
}

data "aws_iam_role" "all" {
  for_each = toset(var.aws_auth_roles)
  name     = each.key
}
```

Next, we will proceed with the creation of a VPC Network. This network will serve as the host for our Kubernetes cluster and all other resources.

```jsx
module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  name   = "${var.name}-${var.environment}"
  cidr   = var.cidr

  public_subnets      = [for k, v in local.azs : cidrsubnet(var.cidr, 5, k)]
  private_subnets     = [for k, v in local.azs : cidrsubnet(var.cidr, 5, k + length(local.azs))]
  database_subnets    = [for k, v in local.azs : cidrsubnet(var.cidr, 5, k + 2 * length(local.azs))]
  intra_subnets       = [for k, v in local.azs : cidrsubnet(var.cidr, 5, k + 3 * length(local.azs))]
  elasticache_subnets = [for k, v in local.azs : cidrsubnet(var.cidr, 5, k + 4 * length(local.azs))]

  enable_nat_gateway   = true
  single_nat_gateway   = true
  enable_dns_hostnames = true

  azs  = local.azs
  tags = local.tags

  public_subnet_tags = {
    "kubernetes.io/cluster/${local.cluster_name}" = "shared"
    "kubernetes.io/role/elb"                      = 1
  }

  private_subnet_tags = {
    "kubernetes.io/cluster/${local.cluster_name}" = "shared"
    "kubernetes.io/role/internal-elb"             = 1
    "karpenter.sh/discovery"                      = local.cluster_name
  }
}
```

With the VPC and Subnet(s) configuration in place, we will now proceed to create a Kubernetes Cluster. We will also be granting access to the Kubernetes Cluster to all IAM Users.  

```jsx
module "node_security_group" {
  source = "terraform-aws-modules/security-group/aws"
  name   = "${local.cluster_name}-eks-nodes-security-group"
  vpc_id = module.vpc.vpc_id
  ingress_with_cidr_blocks = [
    {
      from_port   = 0
      to_port     = 0
      protocol    = "-1"
      cidr_blocks = "0.0.0.0/0"
    }
  ]
  egress_with_cidr_blocks = [
    {
      from_port   = 0
      to_port     = 0
      protocol    = "-1"
      cidr_blocks = "0.0.0.0/0"
    }
  ]
  tags = {
    "karpenter.sh/discovery" = local.cluster_name
  }
}

module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 18.0"

  cluster_name    = local.cluster_name
  cluster_version = var.cluster_version

  cluster_endpoint_private_access = true
  cluster_endpoint_public_access  = true
  create_kms_key                  = true
  kms_key_deletion_window_in_days = 7
  enable_kms_key_rotation         = true
  manage_aws_auth_configmap       = true

  cluster_encryption_config = [{
    resources = ["secrets"]
  }]

  vpc_id                   = module.vpc.vpc_id
  subnet_ids               = module.vpc.private_subnets
  control_plane_subnet_ids = module.vpc.intra_subnets

  create_node_security_group = false
  node_security_group_id     = module.node_security_group.security_group_id

  aws_auth_users = local.aws_auth_users

  aws_auth_roles = local.aws_auth_roles

  eks_managed_node_group_defaults = {
    disk_size                  = 500
    iam_role_attach_cni_policy = true
    create_launch_template     = false
    launch_template_name       = ""
    iam_role_additional_policies = [
      "arn:${data.aws_partition.current.partition}:iam::aws:policy/AmazonSSMManagedInstanceCore"
    ]
  }

  eks_managed_node_groups = {
    default_node_group = {
      instance_types                        = ["t3a.xlarge"]
      attach_cluster_primary_security_group = true
      create_security_group                 = false
      min_size                              = 1
      max_size                              = 5
      desired_size                          = 1
    }
  }

  cluster_addons = {
    coredns = {
      resolve_conflicts = "OVERWRITE"
    }
    kube-proxy = {
      resolve_conflicts = "OVERWRITE"
    }
    vpc-cni = {
      resolve_conflicts = "OVERWRITE"
    }
    aws-ebs-csi-driver = {
      resolve_conflicts = "OVERWRITE"
    }
  }

  tags = {
    "karpenter.sh/discovery" = local.cluster_name
  }
}
```

Next, we will proceed with the installation of the Nginx Load Balancer Controller. This controller will facilitate the forwarding of external connections to the pods.

```jsx
provider "helm" {
  kubernetes {
    host                   = module.eks.cluster_endpoint
    cluster_ca_certificate = base64decode(module.eks.cluster_certificate_authority_data)

    exec {
      api_version = "client.authentication.k8s.io/v1beta1"
      command     = "aws"
      args        = ["eks", "get-token", "--cluster-name", module.eks.cluster_id]
    }
  }
}

provider "kubectl" {
  apply_retry_count      = 5
  host                   = module.eks.cluster_endpoint
  cluster_ca_certificate = base64decode(module.eks.cluster_certificate_authority_data)
  load_config_file       = false

  exec {
    api_version = "client.authentication.k8s.io/v1beta1"
    command     = "aws"
    args        = ["eks", "get-token", "--cluster-name", module.eks.cluster_id]
  }
}

provider "kubernetes" {
  host                   = module.eks.cluster_endpoint
  cluster_ca_certificate = base64decode(module.eks.cluster_certificate_authority_data)

  exec {
    api_version = "client.authentication.k8s.io/v1beta1"
    command     = "aws"
    args        = ["eks", "get-token", "--cluster-name", module.eks.cluster_id]
  }
}

module "eks_blueprints_kubernetes_addons" {
  source         = "github.com/aws-ia/terraform-aws-eks-blueprints//modules/kubernetes-addons?ref=v4.28.0"
  eks_cluster_id = module.eks.cluster_id

  enable_aws_load_balancer_controller = true
  enable_aws_node_termination_handler = true
  enable_metrics_server               = true
  enable_cluster_autoscaler           = true 
}

```

We will use AWS ACM for SSL. This is for generating a Security Certificate and making the website secure. 

```jsx
data "aws_route53_zone" "this" {
  name = var.domain_name
}

module "acm" {
  source              = "terraform-aws-modules/acm/aws"
  domain_name         = local.domain_name
  zone_id             = data.aws_route53_zone.this.id
  wait_for_validation = true

  subject_alternative_names = [
    "*.${local.domain_name}"
  ]
  tags = local.tags
}
```

Let’s define the variables which are being used during infrastructure creation. These variables contain information such as AWS Region, name of the application/infrastructure, CIDR blocks, list of IAM users, domain names, etc.   

```jsx
variable "name" {
  description = "Name to be used on all the resources as identifier"
}

variable "region" {
  description = "The AWS region to use"
  default     = "us-east-2"
}

variable "cidr" {
  description = "The CIDR block for the VPC"
  default     = "10.0.0.0/16"
}

variable "environment" {
  description = "The environment for the resources"
  default     = "staging"
}

variable "domain_name" {
  description = "The domain name for the resources"
  default     = "staging.quick-poc.com"
}

variable "aws_auth_users" {
  description = "The users to be added to aws-auth configmap"
  type        = list(string)
}

variable "cluster_version" {
  description = "The EKS cluster version"
  default     = "1.23"
}

variable "availability_zones_exclude" {
  description = "The availability zones to exclude"
  type        = list(string)
  default     = []
}

variable "aws_auth_roles" {
	description = "The roles to be added to aws-auth configmap"
  default = []
}
```

After preparing and committing the code, [connect your Terraform Cloud Account to the GitHub repository](https://developer.hashicorp.com/terraform/tutorials/cloud/github-oauth). Ensure that you add the necessary variables in the workspace, then proceed by clicking on "Start New Run".

This action will trigger the execution of a "terraform plan" in the background, which will display the anticipated changes. Take a careful look at the proposed modifications. If everything appears satisfactory, proceed with applying the plan. Please note that applying the changes may take some time, during which you will be able to observe the resources being created or brought up gradually.

With our cluster now set up, let us proceed to create Helm charts in our application repository.

### **CI/CD for Backend**

Create a fork of our prompt-eval-be repository into your Organization.

We have developed a Helm chart for deploying the backend of the Evals Framework. This Helm chart utilizes a YAML file to specify the pod configuration. Here's an example of the YAML file structure:

```jsx

# Number of Replicas for Backend application
replicaCount: 1

service:
  type: ClusterIP
  port: 8000

# Creating Nginx ingress loadbalancer
ingress:
  enabled: true
  className: nginx
  tls:
    - hosts:
      - <dns_name>
      secretName: <secret name containing tls certificate of above domain>
  hosts:
    - host: <dns_name> # DNS where backend is hosted
      paths:
        - path: /graphql
          pathType: Prefix`

# Resource allocation for pods i.e. the max cpu and memory
resources:
  limits:
    cpu: 1
    memory: 2Gi
  requests:
    cpu: 1
    memory: 2Gi
```

Please save the aforementioned file in the `kubernetes-values` directory with the name staging.yaml or production.yaml. Additionally, our codebase includes a Dockerfile, which specifies the dependencies to be installed when creating a Docker Image. These dependencies will be included in the pod after deployment. If needed, you can modify the Dockerfile to add any extra packages based on your requirements.

Now, let's move on to the CI/CD process for the Evals Framework. We will leverage GitHub Actions for the deployment.

To get started, create a folder named .github/workflows/ and within it, create a file named staging.yaml.

```jsx
name: Deploy to Production

jobs:
  deploy:
    name: Deploy
    runs-on: ubuntu-latest
    environment: production

    steps:
      - name: Checkout
        uses: actions/checkout@v2
        
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v1
        with:
          aws-access-key-id: ${{ secrets.AWS_PRODUCTION_ACCESS_KEY }}
          aws-secret-access-key: ${{ secrets.AWS_PRODUCTION_SECRET_KEY }}
          aws-region: us-east-1

      - name: Login to Amazon ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v1
      - name: Create a ECR repo
        shell: bash
        run: |
          aws ecr describe-repositories --repository-names ${{ github.event.repository.name }} || ( aws ecr create-repository --repository-name ${{ github.event.repository.name }}  && aws ecr put-lifecycle-policy --repository-name ${{ github.event.repository.name }} --lifecycle-policy-text "{\"rules\":[{\"rulePriority\":1,\"description\":\"Keep last 5 images\",\"selection\":{\"tagStatus\":\"any\",\"countType\":\"imageCountMoreThan\",\"countNumber\":5},\"action\":{\"type\":\"expire\"}}]}"  )

      - name: Build, tag, and push image to Amazon ECR
        id: build-image
        env:
          ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
          ECR_REPOSITORY: ${{ github.event.repository.name }}
          IMAGE_TAG: ${{ github.sha }}
          ENV: prod
        run: |
          docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG  --build-arg ENV=$ENV .
          docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
          echo "::set-output name=image::$ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG"

      - uses: azure/setup-kubectl@v2.0
        with:
          version: "v1.23.6"
        id: install

      - name: "Deploy to EKS"
        id: deploy-eks
        env:
          ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
          ECR_REPOSITORY: ${{ github.event.repository.name }}
          IMAGE_TAG: ${{ github.sha }}
          AWS_REGION: us-east-1
          AWS_EKS_CLUSTER_NAME: ${CLUSTER_NAME}
        run: |-
          aws eks update-kubeconfig --name ${AWS_EKS_CLUSTER_NAME} --region ${AWS_REGION}
          helm upgrade --install --set image.repository=$ECR_REGISTRY/$ECR_REPOSITORY --set image.tag=${IMAGE_TAG}  --values ./kubernetes-values/staging.yaml prompt-eval-api ./helm
```

To proceed, please create the following secrets in your GitHub repository's settings under Secrets and variables → Actions → New Repository Secret:

The Docker image is then built and uploaded to the ECR. Helm is responsible for installing or updating the service with the latest Docker image during each deployment. As a new deployment occurs, a new Pod is created and enters a running state. Once it is verified that the newly spawned Pod is functioning correctly, Kubernetes removes the old Pod and ensures that all requirements are met.
