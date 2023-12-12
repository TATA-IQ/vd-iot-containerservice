from fastapi import FastAPI
from pydantic import BaseModel
from typing import Union


class PortModel(BaseModel):
    model_id: Union[int, None] = None
    port_number: Union[int, None] = None