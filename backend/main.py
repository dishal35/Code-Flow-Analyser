import logging
import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from parser import extract_functions_and_calls
from mock_data import generate_mock_graph
from schemas import GraphResponse

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("app.log"),
    ]
)

logger = logging.getLogger(__name__)

app = FastAPI(title="Code Flow Analyser API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    logger.info("Code Flow Analyser API is running")
    return {"message": "Code Flow Analyser API is running"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    logger.info(f"File upload received: {file.filename}")
    try:
        if not file.filename.endswith('.py'):
            logger.warning(f"Invalid file type: {file.filename}")
            return {"error": "Only .py files are allowed"}
        content = await file.read()
        file_content = content.decode('utf-8')
        logger.info(f"File {file.filename} uploaded successfully")
        graph_data = extract_functions_and_calls(file_content)
        # Build nodes with required structure
        nodes = []
        x, y = 0, 100
        dx, dy = 200, 150
        for idx, func_name in enumerate(graph_data["functions"]):
            nodes.append({
                "id": func_name,
                "data": {
                    "label": func_name,
                    "code": graph_data["code"].get(func_name, "")
                },
                "position": {"x": x + (idx % 2) * dx, "y": y + (idx // 2) * dy}
            })
        # Build edges with required structure
        edges = []
        for idx, call in enumerate(graph_data["calls"]):
            edges.append({
                "id": f"e{idx}",
                "source": call["caller"],
                "target": call["callee"]
            })
        result = {
            "nodes": nodes,
            "edges": edges
        }
        logger.info(f"Generated graph with {len(nodes)} nodes and {len(edges)} edges")
        return result
    except Exception as e:
        logger.error(f"Error processing file {file.filename}: {str(e)}")
        raise
@app.get("/graph-preview", response_model=GraphResponse)
async def get_graph_preview():
    logger.info("Serving mock graph preview")
    return generate_mock_graph()



if __name__ == "__main__":
    import uvicorn
    logger.info("Starting the API server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)