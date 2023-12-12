from fastapi import FastAPI
from pydantic import BaseModel
from typing import Union


class Container_Model(BaseModel):
    container_name: Union[str, None] = None
    container_tag: Union[str, None] = None
    model_id: Union[str, None] = None
    path: Union[str, None] = None
