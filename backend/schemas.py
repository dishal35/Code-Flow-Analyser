# backend/schemas.py
from pydantic import BaseModel
from typing import List, Dict

class NodeData(BaseModel):
    label: str
    code: str

class NodeModel(BaseModel):
    id: str
    data: NodeData
    position: dict

class EdgeModel(BaseModel):
    id: str
    source: str
    target: str

class GraphResponse(BaseModel):
    nodes: list[NodeModel]
    edges: list[EdgeModel]
