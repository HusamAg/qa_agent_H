from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai import Agent

class TestingAgent:
    def __init__(self, model_name, provider):
        self.model = OpenAIModel(
            model_name=model_name, 
            provider=OpenAIProvider(base_url=provider)
        )
    
    def run_sync(self, prompt):
        testingAgent = Agent(  
            self.model,
            deps_type=str,
            output_type=str,
        )
        return testingAgent.run_sync(prompt)