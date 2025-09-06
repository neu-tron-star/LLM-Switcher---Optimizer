from abc import ABC,abstractmethod
from src.message import AIMessage
from typing import Generator

class BaseInference(ABC):
    def __init__(self,model:str='',api_key:str='',base_url:str='',temperature:float=0.5):
        self.name=self.__class__.__name__.replace('Chat','')
        self.model=model
        self.api_key=api_key
        self.base_url=base_url
        self.temperature=temperature
        self.headers={'Content-Type': 'application/json'}

    @abstractmethod
    def invoke(self,messages:list[dict])->AIMessage:
        pass
    
    def stream(self,messages:list[dict])->Generator[str,None,None]:
        pass