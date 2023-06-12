# prompt-eval-be

## Installation

Follow the instructions below for installation

1. Check you have installed python version greater than or equal to 3.9
2. [Install MongoDB](https://www.mongodb.com/docs/manual/administration/install-community/): If MongoDB is not installed on your system, you can download the MongoDB installer from the official website, run it, and follow the installation instructions. Make sure to have MongoDB installed before proceeding.
3. Create a python virtual environment

```sh { language=sh }
python3 -m venv .venv


```

4. Activate the virtual environment

```sh { language=sh }
source .venv/bin/activate


```

5. Upgrade to the latest pip version

```sh { language=sh }
python -m pip install --upgrade pip


```

6. Clone the [evals](https://github.com/openai/evals) submodule

```sh { language=sh }
git submodule update --init --recursive
pip install -e evals_framework

```

7. Run below command if **Unable to checkout git submodule path** error faced

```sh { language=sh }
brew install git-lfs


```

8. Install the dependencies

```sh { language=sh }
pip install -r requirements.txt


```

9. Copy the contents of .env.sample file in .env file and add the values for all env variables.
10. Generate OPENAI_API_KEY using this [link](https://platform.openai.com/account/api-keys) and update the same in .env 
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

## Documents

1. Sequence diagrams: - [docs/sequenceDiagram.mermaid](./docs/sequenceDiagram.mermaid)
2. DBML diagrams: - [docs/db.dbml](./docs/db.dbml)
3. Product usage guide: - [docs/productGuide.md](./docs/productGuide.md)
