from io import BytesIO
from abc import ABC
import requests
import base64
import re

class BaseMessage(ABC):
    def to_dict(self) -> dict[str, str]:
        return {
            'role': self.role,
            'content': f'{self.content}'
        }

    def __repr__(self):
        class_name = self.__class__.__name__
        attrs = ", ".join(f"{k}={v}" for k, v in self.__dict__.items())
        return f"{class_name}({attrs})"


class HumanMessage(BaseMessage):
    def __init__(self, content: str):
        self.role = 'user'
        self.content = content


class AIMessage(BaseMessage):
    def __init__(self, content: str):
        self.role = 'assistant'
        self.content = content


class SystemMessage(BaseMessage):
    def __init__(self, content: str):
        self.role = 'system'
        self.content = content


class ImageMessage(BaseMessage):
    def __init__(self, text: str = None, image_path: str = None, image_base_64: str = None):
        self.role = 'user'
        if image_base_64 is not None or image_path is None:
            self.content = (text, image_base_64)
        elif image_path is not None or image_base_64 is None:
            self.content = (text, self.__image_to_base64(image_path))
        else:
            raise ValueError("image_path and image_base_64 cannot be both None or both not None")

    def __is_url(self, path: str) -> bool:
        return bool(re.match(r'^https?://', path))

    def __is_file_path(self, path: str) -> bool:
        pattern = r'^([./~]|([a-zA-Z]:)|\\|//)?\.?/?[a-zA-Z0-9._-]+(\.[a-zA-Z0-9]+)?$'
        return bool(re.match(pattern, path))

    def __image_to_base64(self, source: str) -> str:
        if self.__is_url(source):
            response = requests.get(source)
            image_bytes = BytesIO(response.content).read()
        elif self.__is_file_path(source):
            with open(source, 'rb') as f:
                image_bytes = f.read()
        else:
            raise ValueError("Invalid image source. Must be a URL or file path.")
        return base64.b64encode(image_bytes).decode('utf-8')


class ToolMessage(BaseMessage):
    def __init__(self, content: str, tool_call: str, tool_args: dict):
        self.role = 'assistant'
        self.content = content
        self.tool_call = tool_call
        self.tool_args = tool_args
