PROCESS_COMPLETED = True

SIGINT_TRIGGERED = False

EVALS_CLASS_DICT = {
"test-match": "evals.elsuite.basic.match:Match",
"coqa-match": "evals.elsuite.basic.match:Match",
"regex-match": "evals.elsuite.basic.match:Match",
"graphql-fuzzy": "evals.elsuite.graphql:GraphQL"
}