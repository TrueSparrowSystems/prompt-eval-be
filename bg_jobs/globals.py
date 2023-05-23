PROCESS_COMPLETED = True

SIGINT_TRIGGERED = False

EVALS_CLASS_DICT = {
"match": "evals.elsuite.basic.match:Match",
"fuzzy-match": "evals.elsuite.basic.fuzzy_match:FuzzyMatch",
"graphql": "evals.elsuite.graphql:GraphQL"
}