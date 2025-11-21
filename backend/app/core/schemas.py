from pydantic import BaseModel

class MatrixInput(BaseModel):
    matrix_text: str

class RouteInput(BaseModel):
    start: str
    end: str