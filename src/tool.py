from pydantic import BaseModel
from inspect import getdoc

def tool(name: str, args_schema: BaseModel):
    """
    Decorator to attach metadata to a function:
    - name
    - schema (from Pydantic model)
    - description (from docstring)
    """
    def decorator(func):
        func.name = name
        func.schema = args_schema.model_json_schema()
        func.schema.pop('title', None)  # safe pop
        func.description = getdoc(func)
        return func
    return decorator
