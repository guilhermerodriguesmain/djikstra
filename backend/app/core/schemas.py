from pydantic import BaseModel

class DijkstraRequest(BaseModel):
    start: str
    end: str
    
class InsertRandomOut(BaseModel):
    __root__: dict[str, dict[str, dict[str, int]]]
