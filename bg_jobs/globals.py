PROCESS_COMPLETED = True

SIGINT_TRIGGERED = False

EVALS_CLASS_DICT = {
"match": "evals.elsuite.basic.match:Match",
"fuzzy_match": "evals.elsuite.basic.fuzzy_match:FuzzyMatch",
"graphql-fuzzy": "evals.elsuite.graphql:GraphQL"
}