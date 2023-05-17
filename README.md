# prompt-eval-be

## Installation

Follow the instructions below for installation

1. Check you have installed python version greater than or equal to 3.9
2. Create a python virtual environment

```sh { language=sh }
python3 -m venv .venv

```

3. Activate the virtual environment

```sh { language=sh }
source .venv/bin/activate

```

3. Upgrade to the latest pip version

```sh { language=sh }
python -m pip install --upgrade pip

```

4. Clone the [evals](https://github.com/openai/evals) submodule

```sh { language=sh }
git submodule update --init --recursive

```

5. Install the dependencies

```sh { language=sh }
pip install -r requirements.txt

```

6. Copy the contents of .env.sample file in .env file and add the values for all env variables.
7. Run the api server using following command

```sh { language=sh }
python manage.py runserver 8000

```

8. Run the test cases using following command

```sh { language=sh }
python manage.py test graphQL

```

9. Run the following command to generate test coverage report

```sh { language=sh }
coverage run manage.py test
coverage report

```

## Documents

1. Sequence diagrams: - [docs/sequenceDiagram.mermaid](./docs/sequenceDiagram.mermaid)
2. DBML diagrams: - [docs/db.dbml](./docs/db.dbml)
