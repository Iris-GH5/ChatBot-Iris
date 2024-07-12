from termcolor import colored
from models.openai_models import get_open_ai, get_open_ai_json
from models.ollama_models import OllamaModel, OllamaJSONModel
from models.vllm_models import VllmJSONModel, VllmModel
from models.groq_models import GroqModel, GroqJSONModel
from models.claude_models import ClaudModel, ClaudJSONModel
from models.gemini_models import GeminiModel, GeminiJSONModel
from prompts.prompts import (
    planner_prompt_template,
    selector_prompt_template,
    reporter_prompt_template,
    reviewer_prompt_template,
    router_prompt_template
)
from utils.helper_functions import get_current_utc_datetime, check_for_content
from states.state import AgentGraphState

class Agent:
    def __init__(self, state: AgentGraphState, model=None, server=None, temperature=0, model_endpoint=None, stop=None, guided_json=None):
        self.state = state
        self.model = model
        self.server = server
        self.temperature = temperature
        self.model_endpoint = model_endpoint
        self.stop = stop
        self.guided_json = guided_json

    def get_llm(self, json_model=True):
        if self.server == 'openai':
            return get_open_ai_json(model=self.model, temperature=self.temperature) if json_model else get_open_ai(model=self.model, temperature=self.temperature)
        if self.server == 'ollama':
            return OllamaJSONModel(model=self.model, temperature=self.temperature) if json_model else OllamaModel(model=self.model, temperature=self.temperature)
        if self.server == 'vllm':
            return VllmJSONModel(
                model=self.model, 
                guided_json=self.guided_json,
                stop=self.stop,
                model_endpoint=self.model_endpoint,
                temperature=self.temperature
            ) if json_model else VllmModel(
                model=self.model,
                model_endpoint=self.model_endpoint,
                stop=self.stop,
                temperature=self.temperature
            )
        if self.server == 'groq':
            return GroqJSONModel(
                model=self.model,
                temperature=self.temperature
            ) if json_model else GroqModel(
                model=self.model,
                temperature=self.temperature
            )
        if self.server == 'claude':
            return ClaudJSONModel(
                model=self.model,
                temperature=self.temperature
            ) if json_model else ClaudModel(
                model=self.model,
                temperature=self.temperature
            )
        if self.server == 'gemini':
            return GeminiJSONModel(
                model=self.model,
                temperature=self.temperature
            ) if json_model else GeminiModel(
                model=self.model,
                temperature=self.temperature
            )      

    def update_state(self, key, value):
        self.state = {**self.state, key: value}
        
class ConsultantAgent:
    def __init__(self, prompt):
        self.prompt = prompt
    
    def provide_support(self, user_input):
        # Logic to process user input and generate a response using the consultant_prompt
        response = self._generate_response(user_input)
        return response

    def _generate_response(self, user_input):
        # Placeholder for AI model integration to generate responses
        # This can be an API call to a language model like OpenAI's GPT
        return f"Consultant Response to: {user_input}"

class ReporterAgent:
    def __init__(self, prompt):
        self.prompt = prompt
    
    def document_incident(self, user_input):
        # Logic to process user input and generate a response using the reporter_prompt
        response = self._generate_response(user_input)
        return response

    def _generate_response(self, user_input):
        # Placeholder for AI model integration to generate responses
        # This can be an API call to a language model like OpenAI's GPT
        return f"Reporter Response to: {user_input}"

class HealthAnalystAgent:
    def __init__(self, prompt):
        self.prompt = prompt
    
    def analyze_health(self, user_input):
        # Logic to process user input and generate a response using the health_analyst_prompt
        response = self._generate_response(user_input)
        return response

    def _generate_response(self, user_input):
        # Placeholder for AI model integration to generate responses
        # This can be an API call to a language model like OpenAI's GPT
        return f"Health Analyst Response to: {user_input}"