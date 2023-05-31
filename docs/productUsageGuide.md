<div align="center">
   
# Prompt Evaluator
</div>

Prompt Evaluator is an AI assistant tool specifically designed for product managers and developers. With a strong emphasis on versatility, our tool empowers users to effectively solve a wide range of problems tailored to their unique use cases. By enabling prompt template engineering and enhancement, we ensure that prompts are both easily testable and maintainable. We are constantly working towards addressing broader, more generic issues to provide a clear and user-centric solution that unleashes your full potential. Stay tuned for exciting updates as we continue to enhance our tool.

<details>
   <summary>
Table of Content
   </summary>

- [Experiments](#experiments)
   - [What are experiments?](#what-are-experiments)
   - [Viewing Experiment Details](#to-see-details-of-individual-experiment)
   - [Creating and Updating Experiments](#to-createupdate-experiments)

- [Prompt Templates](#prompt-templates)
   - [Creating and Updating Templates](#to-create-new-template)
   - [Cloning Templates](#to-clone-the-template)

- [Test Cases](#test-cases)
   - [Creating Test Cases](#to-create-new-test-case)

- [Running Prompt Templates](#to-run-the-prompt-template)
- [Reports](#reports)
   - [Comparing Expected and Actual Outputs](#compare-expected-output-and-actual-output-in-reports)
   - [Share Reports](#share-report)
</details>

# Experiments:

## What are experiments?

The experiment feature in our product allows users to create collections of prompt templates. These templates are for user-defined conversations that may include variables. Users can define their own conversations with various roles and prompts, incorporating variables where necessary. Users can evaluate the performance of prompts by executing them with different OpenAI models and associated test cases. By running prompt templates with different models and test cases, users gain valuable insights into the performance and suitability of their prompts for different scenarios.

## To see details of individual experiment:

Select the desired experiment to view its details. Read the experiment title, description, and other related details to understand its purpose and context.

![img](https://promt-eval-assests.s3.amazonaws.com/snapShots/experiment_1.png)

## To create/update experiments:

To start a new experiment, just click on the "Create experiment" button. A brand new experiment will be created with a default title and description. The title and description are basic details that briefly explain what the experiment is about. 

![img](https://promt-eval-assests.s3.amazonaws.com/snapShots/Experiment_2.png)

## To update the experiment

We can update the title for the experiment in two ways:

1. Using the rename button associated with each experiment cell.

![img](https://promt-eval-assests.s3.amazonaws.com/snapShots/Experiment_3.png)

2. Simply click on the title located at the top of the page.

![img](https://promt-eval-assests.s3.amazonaws.com/snapShots/Experiment_4.png)

We can add a clear and concise description in this section to explicitly state the experiment's goals and objectives by modifying the default description as shown below.

![img](https://promt-eval-assests.s3.amazonaws.com/snapShots/Experiment_5.png)

# Prompt Templates:

## To create new template:

Step 1: Navigate to the Prompt Template section.

![img](https://promt-eval-assests.s3.amazonaws.com/snapShots/Prompt_1.png)

Step 2: Click on the "Add New Template" option.

![img](https://promt-eval-assests.s3.amazonaws.com/snapShots/Prompt_2.png)

Step 3: A page for creating a new template will appear, allowing users to define and customize the content, format, and variables used in the prompt templates, aligning them with the experiment's objectives and requirements.

![img](https://promt-eval-assests.s3.amazonaws.com/snapShots/Prompt_3.png)

To customize the prompt template, you have the flexibility to modify the content, format, and variables according to your requirements. In this process, you need to provide both the system role and user role based on your specific needs. When declaring variables in the conversation, please use the format {{variable\_name}}. For a better understanding, refer to the example provided below.

![img](https://promt-eval-assests.s3.amazonaws.com/snapShots/Prompt_4.png)

To add a new role, simply click on the "Add message" button located above the create button.

![img](https://promt-eval-assests.s3.amazonaws.com/snapShots/Prompt_5.png)

To change the role of a conversation, you can toggle the role from within the conversation itself.

![img](https://promt-eval-assests.s3.amazonaws.com/snapShots/Prompt_6.png)

Step 4: Click the "Create" button at the bottom of the page to create the template.

![img](https://promt-eval-assests.s3.amazonaws.com/snapShots/Prompt_7.png)

You can see the newly created prompt template under the prompt template list.

![img](https://promt-eval-assests.s3.amazonaws.com/snapShots/Prompt_8.png)

## To update the template:

Step 1: Click the prompt template cell you wish to update.

![img](https://promt-eval-assests.s3.amazonaws.com/snapShots/Prompt_9.png)

Step 2: Then, provide the necessary changes to the template, as demonstrated earlier when creating a new template.

Step 3: Save the template after making any changes or edits.

![img](https://promt-eval-assests.s3.amazonaws.com/snapShots/Prompt_10.png)

## To clone the template:

Step 1: Please click on the "Clone" button provided under each prompt template cell.

![img](https://promt-eval-assests.s3.amazonaws.com/snapShots/Prompt_11.png)

Step 2: After making the necessary changes to the template, clone it using the clone button.

![img](https://promt-eval-assests.s3.amazonaws.com/snapShots/Prompt_12.png)

Below, you will see a newly created clone template.

![img](https://promt-eval-assests.s3.amazonaws.com/snapShots/Prompt_13.png)

# Test Cases:

## To create new test case:

Step 1: Access the Test Case section or tab.

![img](https://promt-eval-assests.s3.amazonaws.com/snapShots/TestCases_1.png)

Step 2: Click on the "Add new test case".

![img](https://promt-eval-assests.s3.amazonaws.com/snapShots/TestCases_2.png)

Step 3: Specify the variable values, expected outputs, and additional parameters for each test case.

Add title and description as shown below:

![img](https://promt-eval-assests.s3.amazonaws.com/snapShots/TestCases_3.png)

Now, specify the template that should replace it, along with the corresponding value for the given variable name.

![img](https://promt-eval-assests.s3.amazonaws.com/snapShots/TestCases_4.png)

Add acceptable results which will be used to compare the actual and expected result to generate a report.

![img](https://promt-eval-assests.s3.amazonaws.com/snapShots/TestCases_5.png)

Step 4: Create the test case after defining the necessary details.

![img](https://promt-eval-assests.s3.amazonaws.com/snapShots/TestCases_6.png)

# To Run the Prompt Template:

Step 1: Click on the run button provided under each prompt template cell.

![img](https://promt-eval-assests.s3.amazonaws.com/snapShots/RunPropmts_1.png)

Step 2: Choose the required model and evaluation from the drop down menu

![img](https://promt-eval-assests.s3.amazonaws.com/snapShots/RunPropmts_2.png)

Step 3: To initiate the process, please click the "Run" button.

![img](https://promt-eval-assests.s3.amazonaws.com/snapShots/RunPropmts_3.png)

Step 4: After a few seconds, a report will be generated, which you can then examine.

![img](https://promt-eval-assests.s3.amazonaws.com/snapShots/RunPropmts_4.png)

# Reports:

## Compare Expected Output and Actual Output in Reports:

To view the report, click the view report button located under the desired prompt template cell.

![img](https://promt-eval-assests.s3.amazonaws.com/snapShots/RunPropmts_4.png)

Please review the side-by-side comparison of the expected and actual outcomes. Pay attention to any differences, problems with performance, or areas that need improvement. Using this analysis, make informed decisions and adjustments to optimize the experiment.

![img](https://promt-eval-assests.s3.amazonaws.com/snapShots/RunPropmts_5.png)

## Share Report:

You can use the "Share Report" button found below the test case within the report. Alternatively, you can copy the link directly from the Google tab.
