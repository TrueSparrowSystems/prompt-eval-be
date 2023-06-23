import re

"""
create prompt by replacing dynamic variables with values in prompt template by test case

@class CreatePrompt
"""
class CreatePrompt:
    """
    Initialize the CreatePrompt object with the provided parameters
    
    @params {Object} params
    @params {Object} params.test_case
    @params {Object} params.prompt_template_obj

    @returns {Object} params
    """
    def __init__(self, params):
        self.test_case = params['test_case']
        self.prompt_template_obj = params['prompt_template_obj']

    """
    perfrom create prompt which replace dynamic variables with values in prompt template by test case

    @returns {Object} prompt
    """
    def perform(self):
        try:
            prompt = []
            template_conversations = self.prompt_template_obj.conversation
            
            # Regex pattern to find dynamic variables in prompt template
            pattern = r"\{\{[a-zA-Z0-9_]+\}\}"

            for conversion in template_conversations:
                content = conversion['content']
        
                matches = re.findall(pattern, content)
    
                replaced_content = content
                for match in matches:
                    key = match.replace("{{", "").replace("}}", "")
                    if key in self.test_case.dynamic_var_values:
                        replaced_content = content.replace(match, self.test_case.dynamic_var_values[key])
                prompt.append({'role': conversion['role'], 'content': replaced_content})          
            
            return prompt
        except Exception as e:
            print(e)
            return(e)
            
        
    def raise_error(self, message, code= "bg_j_b_cp",debug="SOMETHING_WENT_WRONG" ):
        error_data = {
            "message": message,
            "debug": debug,
            "code":code
        }
                
        raise Exception(error_data)
    
