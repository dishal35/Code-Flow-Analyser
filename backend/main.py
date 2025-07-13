import logging
import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from parser import extract_functions_and_calls

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
    # Log the file name received
    logger.info(f"File upload received: {file.filename}")
    
    try:
        # Validate file extension
        if not file.filename.endswith('.py'):
            logger.warning(f"Invalid file type: {file.filename}")
            return {"error": "Only .py files are allowed"}
        
        # Read file content
        content = await file.read()
        file_content = content.decode('utf-8')
        
        logger.info(f"File {file.filename} uploaded successfully")
        
        # Parse the code and extract graph data
        graph_data = extract_functions_and_calls(file_content)
        
        # Transform the parser output into the expected format
        nodes = [{"id": func_name} for func_name in graph_data["functions"]]
        edges = graph_data["calls"]
        
        result = {
            "nodes": nodes,
            "edges": edges,
            "code": graph_data["code"]
        }
        
        logger.info(f"Generated graph with {len(nodes)} nodes and {len(edges)} edges")
        return result
        
    except Exception as e:
        logger.error(f"Error processing file {file.filename}: {str(e)}")
        raise



if __name__ == "__main__":
    import uvicorn
    logger.info("Starting the API server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)