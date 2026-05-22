from langchain_openai import ChatOpenAI
from openai import OpenAI
from config.settings import model_settings as config

def get_chat_llm_deepseek():
    return ChatOpenAI(
        api_key=config.DEEPSEEK_API_KEY,
        base_url=config.DEEPSEEK_BASE_URL,
        model=config.DEEPSEEK_MODEL
    )

def get_chat_llm_local():
    return ChatOpenAI(
        base_url=config.LOCAL_LLM_URL,
        model=config.LOCAL_LLM_MODEL
    )


class DeepSeekClient:
    def __init__(self):
        self.client = OpenAI(
            api_key=config.DEEPSEEK_API_KEY,
            base_url=config.DEEPSEEK_BASE_URL,
        )
        self.model = config.DEEPSEEK_MODEL
    def chat(self,prompt: str) -> str:
        response = self.client.chat.completions.create(
            model= self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
