from typing import Generator, AsyncGenerator
from tenacity import retry, stop_after_attempt, retry_if_exception_type
from requests import RequestException, HTTPError, ConnectionError
from httpx import Client, AsyncClient
from json import loads
import requests

from src.inference import BaseInference
from src.message import AIMessage, BaseMessage, HumanMessage, ImageMessage


class ChatOpenAI(BaseInference):
    def __init__(self, model: str, api_key: str, temperature: float = 0.7):
        self.model = model
        self.api_key = api_key
        self.temperature = temperature
        self.base_url = "https://api.openai.com/v1"

    @retry(stop=stop_after_attempt(3), retry=retry_if_exception_type(RequestException))
    def invoke(self, messages: list[BaseMessage], json_output=False) -> AIMessage:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        contents = []
        system_instruction = None

        for msg in messages:
            if isinstance(msg, HumanMessage):
                contents.append({"role": "user", "content": msg.content})
            elif isinstance(msg, AIMessage):
                contents.append({"role": "assistant", "content": msg.content})
            elif isinstance(msg, ImageMessage):
                # OpenAI image endpoint is separate
                text, _ = msg.content
                return self.generate_image(text)
            else:
                system_instruction = msg.content

        payload = {
            "model": self.model,
            "messages": [{"role": "system", "content": system_instruction}] + contents if system_instruction else contents,
            "temperature": self.temperature
        }

        try:
            with Client() as client:
                response = client.post(f"{self.base_url}/chat/completions", headers=headers, json=payload, timeout=None)
            response.raise_for_status()
            resp_json = response.json()
            content = resp_json['choices'][0]['message']['content']
            if json_output:
                content = loads(content)
            return AIMessage(content)
        except HTTPError as err:
            print(f"HTTP Error: {err.response.text}")
            exit()
        except ConnectionError as err:
            print(err)
            exit()

    @retry(stop=stop_after_attempt(3), retry=retry_if_exception_type(RequestException))
    async def async_invoke(self, messages: list[BaseMessage], json_output=False) -> AIMessage:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        contents = []
        system_instruction = None

        for msg in messages:
            if isinstance(msg, HumanMessage):
                contents.append({"role": "user", "content": msg.content})
            elif isinstance(msg, AIMessage):
                contents.append({"role": "assistant", "content": msg.content})
            elif isinstance(msg, ImageMessage):
                text, _ = msg.content
                return self.generate_image(text)
            else:
                system_instruction = msg.content

        payload = {
            "model": self.model,
            "messages": [{"role": "system", "content": system_instruction}] + contents if system_instruction else contents,
            "temperature": self.temperature
        }

        async with AsyncClient() as client:
            response = await client.post(f"{self.base_url}/chat/completions", headers=headers, json=payload, timeout=None)
            resp_json = response.json()
            content = resp_json['choices'][0]['message']['content']
            if json_output:
                content = loads(content)
            return AIMessage(content)

    @retry(stop=stop_after_attempt(3), retry=retry_if_exception_type(RequestException))
    def stream(self, messages: list[BaseMessage], json_output=False) -> Generator[str, None, None]:
        # OpenAI does support streaming via SSE
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        contents = []
        system_instruction = None

        for msg in messages:
            if isinstance(msg, HumanMessage):
                contents.append({"role": "user", "content": msg.content})
            elif isinstance(msg, AIMessage):
                contents.append({"role": "assistant", "content": msg.content})
            else:
                system_instruction = msg.content

        payload = {
            "model": self.model,
            "messages": [{"role": "system", "content": system_instruction}] + contents if system_instruction else contents,
            "temperature": self.temperature,
            "stream": True
        }

        response = requests.post(f"{self.base_url}/chat/completions", headers=headers, json=payload, stream=True)
        response.raise_for_status()
        for line in response.iter_lines(decode_unicode=True):
            if line and line.startswith("data: "):
                chunk = loads(line.replace("data: ", ""))
                if "choices" in chunk and chunk["choices"][0].get("delta", {}).get("content"):
                    yield chunk["choices"][0]["delta"]["content"]

    def available_models(self):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        try:
            with Client() as client:
                resp = client.get(f"{self.base_url}/models", headers=headers)
            resp.raise_for_status()
            models = resp.json().get("data", [])
            return [m["id"] for m in models]
        except HTTPError as err:
            print(f"HTTP Error: {err.response.text}")
            exit()
        except ConnectionError as err:
            print(err)
            exit()

    def generate_image(self, prompt: str) -> AIMessage:
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {"prompt": prompt, "n": 1, "size": "1024x1024"}
        try:
            with Client() as client:
                resp = client.post(f"{self.base_url}/images/generations", headers=headers, json=payload)
            resp.raise_for_status()
            image_url = resp.json()["data"][0]["url"]
            return AIMessage(f"[Image generated] URL: {image_url}")
        except HTTPError as err:
            print(f"HTTP Error: {err.response.text}")
            exit()
        except ConnectionError as err:
            print(err)
            exit()
