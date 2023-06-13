# Prompt Evaluator Backend

## Introduction

Prompt Evaluator is an AI assistant tool specifically designed for product managers and developers. With a strong emphasis on versatility, our tool empowers users to effectively solve a wide range of problems tailored to their unique use cases. By enabling prompt template engineering and enhancement, we ensure that prompts are both easily testable and maintainable. Our tool also provides a seamless integration with the OpenAI API, allowing users to quickly generate and evaluate prompts. With a robust and intuitive UI, we ensure that users can easily navigate through the tool and leverage its full potential.

## Features

- **Experiments** - The experiment feature in our product allows users to create collections of prompt templates. Users can define their own conversations with various roles and prompts, incorporating variables where necessary. Users can evaluate the performance of prompts by executing them with different OpenAI models and associated test cases. 

- **Prompt Templates** - Prompt templates are the building blocks of an Experiment which allow users to define their own prompts. They are highly customizable, allowing users the flexibility to modify the content, format, and variables according to their requirements. 

- **Test Cases** - These are the cases on which the accuracy of a prompt is evaluated. Users can define their own test cases and associate them with prompts. Test cases can be defined as a list of inputs and expected outputs. 

By running prompt templates with different models and test cases, users gain valuable insights into the performance and suitability of their prompts for different scenarios. For detailed information on the features, please refer to the [product guide](./docs/productGuide.md).

## Architecture

Prompt Evaluator has two components:

- [**Frontend**](https://github.com/TrueSparrowSystems/prompt-eval-fe)
- [**Backend**](https://github.com/TrueSparrowSystems/prompt-eval-be)

This is the backend component of the Prompt Evaluator tool. It is built using Django and MongoDB. It exposes a GraphQL API for the frontend to consume. The frontend is built using Next.js. The frontend and backend communicate with each other using the GraphQL API. It is a standalone application that can be deployed separately. For better understanding of the architecture, please refer to the following diagrams:

- [**Sequence diagrams**](./docs/sequenceDiagram.mermaid)
- [**DBML diagrams**](./docs/db.dbml)


## Tech Stack

- **Language**: - Python 3.9
- **Framework**: - Django 3.2.7
- **Database**: - MongoDB 5.0.3
- **API**: - GraphQL

## Installation

Follow the instructions below for installation:

1. Check you have installed python version greater than or equal to 3.9
2. [Install MongoDB](https://www.mongodb.com/docs/manual/administration/install-community/): If MongoDB is not installed on your system, you can download the MongoDB installer from the official website, run it, and follow the installation instructions. Make sure to have MongoDB installed before proceeding.

3. Copy the contents of .env.sample file in .env file and add the values for all env variables.

```sh { language=sh }
# For Linux/macOS
cp .env.sample .env
# For Windows
copy .env.sample .env
```

4. Generate `OPENAI_API_KEY` using this [link](https://platform.openai.com/account/api-keys) and update the same in .env file.

5. Run below command to specify the management of large files with Git.

```sh { language=sh }
brew install git-lfs
```

6. Create a python virtual environment

```sh { language=sh }
python3 -m venv .venv
```

7. Activate the virtual environment

```sh { language=sh }
source .venv/bin/activate
```

8. Upgrade to the latest pip version

```sh { language=sh }
python -m pip install --upgrade pip
```

9. Clone the [evals](https://github.com/openai/evals) submodule

```sh { language=sh }
git submodule update --init --recursive
pip install -e evals_framework
```

10. Install the dependencies

```sh { language=sh }
pip install -r requirements.txt
```

11. Run the api server using following command

```sh { language=sh }
python manage.py runserver 8000
```

12. Run the test cases using following command

```sh { language=sh }
python manage.py test graphQL
```

13. Run the following command to generate test coverage report

```sh { language=sh }
coverage run manage.py test
coverage report
```

## Contribution

We welcome more helping hands to make **Prompt Evaluator** better. Feel free to report issues, raise PRs for fixes & enhancements. We are constantly working towards addressing broader, more generic issues to provide a clear and user-centric solution that unleashes your full potential. Stay tuned for exciting updates as we continue to enhance our tool.

<p align="left">Built with :heart: by <a href="https://truesparrow.com/" target="_blank">True Sparrow</a></p>