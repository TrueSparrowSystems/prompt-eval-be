import re

class CreatePrompt:
    def __init__(self, params):
        self.test_case = params['test_case']
        self.prompt_template_obj = params['prompt_template_obj']

    def perform(self):
        try:
            prompt = []
            template_conversations = self.prompt_template_obj.conversation
            pattern = r"\{\s*[a-zA-Z0-9\s]+\s*\}"

            print('Conversations:   ', template_conversations)
            for conversion in template_conversations:
                content = conversion['content']
                print('content:   ', content)
                #content = "{a} and {b} are friends"
                matches = re.findall(pattern, content)
                print('matches:   ', matches)
                for match in matches:
                    key = match.replace("{", "").replace("}", "")
                    print('self.test_case.dynamic_var_values:   ', self.test_case.dynamic_var_values)
                    if key in self.test_case.dynamic_var_values:
                        replaced_content = content.replace(match, self.test_case.dynamic_var_values[key])
                print('replaced_content:   ', replaced_content)
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
    
