from core.config import Config
from openai import OpenAI
import json
from core.src.utils import postprocess_classification_respond

class AgentException(Exception):
    def __init__(self, *args):
        super().__init__(*args)

    def __str__(self):
        return "Something went wrong when setup LLM!"

class Agent:
    def __init__(self):
        self.base_url = "https://api.upstage.ai/v1"
        self.api_key = Config.UPSTAGE_API_KEY
        self.client = OpenAI(api_key=self.api_key,
                             base_url=self.base_url)

        
    def run(self, messages):
        response = self.client.chat.completions.create(
            model='solar-pro',
            messages=messages,
        )
        print(type(response.choices[0].message.content))
        return response.choices[0].message.content
    
    def perform_classification(self, user_request):
        messages = [
            {
                "role": "system",
                "content": Config.SYS_PROMPTS_CLASSIFICATION,
            },
            {
                "role": "user",
                "content": user_request,
            }
        ]
        response = self.client.chat.completions.create(
            model="solar-pro",
            messages=messages,
        )
        return postprocess_classification_respond(response.choices[0].message.content)
    
    def perform_function_mapping(self, user_request, system_prompt, structured_output):
        messages = [
                {
                    'role': 'system',
                    'content': system_prompt
                },
                {
                    'role': 'user',
                    'content': user_request
                }
            ]
        response = self.client.chat.completions.create(
                model="solar-pro",
                messages=messages,
                response_format=structured_output
            )
        return response.choices[0].message.content
    
    def process_user_request(self, user_request):
        '''
        Outpupt: function_name (string), function_parameters (JSON), model_respond (string)
        Return the JSON string with the information of the function that the user want to call together the respond of the system.
        '''
        try:
            classification = self.perform_classification(user_request)
            print(classification)
            function_name = Config.CLASSIFICATIONS[classification]
            function_parameters = {}
            
            if classification != 0:
                function_parameters = self.perform_function_mapping(
                    user_request, 
                    system_prompt = Config.SYS_PROMPTS[Config.CLASSIFICATIONS[classification]], 
                    structured_output = Config.STRUCTURED_OUTPUT[Config.CLASSIFICATIONS[classification]])
                function_parameters = json.loads(function_parameters)
            return True, function_name, function_parameters
        except Exception as e:
            return False, e, {}
