# backend/app/api/router.py
from fastapi import APIRouter, Depends, Request, HTTPException
from ..core.graph import Graph
from ..core import schemas

router = APIRouter(prefix="/api", tags=["graph"])

def get_graph(request: Request) -> Graph:
    return request.app.state.Graph


@router.get("/graph/random", response_model=schemas.GraphRandomResponse)
def random_graph():
    graph = Graph()
    graph.random_edges()
    for u, v, data in graph.G.edges(data=True): 
        edge_list = {"u": u, "v": v, "weight": data.get("weight")}
    return {edge_list}

@router.post("/graph/add-edge", response_model=schemas.GraphRandomResponse)
def add_edge(req: schemas.AddEdgeRequest, graph: Graph = Depends(get_graph)):
    graph.add_edge(req.u, req.v, req.weight)
    return {"nodes": graph.get_nodes(), "edges": graph.get_edges()}

@router.post("/graph/shortest/{source}/{target}", response_model=schemas.PathResponse)
def shortest(req: schemas.PathRequest, graph: Graph = Depends(get_graph)):
    try:
        path, dist = graph.shortest_path(req.source, req.target)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    return {"source": req.source, "target": req.target, "distance": dist, "path": path}

@router.get("/graph", response_model=schemas.GraphRandomResponse)
def get_graph_full(graph:Graph = Depends(get_graph)):
    return {"nodes": graph.get_nodes(), "edges": graph.get_edges()}
