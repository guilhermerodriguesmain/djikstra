# backend/app/core/schemas.py
from pydantic import BaseModel
from typing import List, Dict, Optional


# Responses classes

class GraphRandomResponse(BaseModel): # Define response rondom graph
    u: str
    v: str
    weight: int


    
    
# Requests classes
class RandomGraphRequest(BaseModel): # Define request rondom graph
    n_edges: Optional[int] = None

class AddEdgeRequest(BaseModel):
    u: str
    v: str
    weight: int

class PathRequest(BaseModel):
    source: str
    target: str

class EdgeOut(BaseModel):
    u: str
    v: str
    w: int



class PathResponse(BaseModel):
    source: str
    target: str
    distance: float
    path: List[str]
