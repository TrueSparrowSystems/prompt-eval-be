class CommonValidator:
    def validate_string(variable):
        return type(variable) == str

    def validate_integer(variable):
        variable = int(variable)
        return type(variable) == int

    def is_var_none(variable):
        return variable == None

    def validate_dictionary(variable):
        return type(variable) !=  dict

    def validate_non_empty_dictonary(variable):
        return type(variable) ==  dict and len(variable) > 0

    def validate_non_empty_list(variable):
        return type(variable) ==  list and len(variable) > 0

    def max_length_validation(variable, length):
        return len(variable) <= length