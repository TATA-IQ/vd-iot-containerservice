from fastapi import FastAPI
from pydantic import BaseModel
from typing import Union


class RequestModel(BaseModel):
    model_id: Union[int,str]
    action:str
    