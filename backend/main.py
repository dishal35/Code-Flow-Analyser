import logging
import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

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
    logger.info(f"Uploading file: {file.filename}")
    try:
        if not file.filename.endswith(".py"):
            logger.warning(f"Unsupported file type: {file.filename}")
            raise HTTPException(status_code=400, detail="Only .py files allowed")

        contents = await file.read()
        file_size = len(contents)
        file_content = contents.decode("utf-8")  # Reserved for AST parsing tomorrow

        # Save file to uploads/
        UPLOAD_DIR = "uploads"
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        with open(file_path, "wb") as f:
            f.write(contents)

        logger.info(f"File saved to {file_path} ({file_size} bytes)")

        return {
            "nodes": [{"id": "main"}],
            "edges": [{"source": "main", "target": "helper"}],
            "code": {"main": "def main():\n  helper()"}
        }

    except Exception as e:
        logger.error(f"Error uploading file: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")



if __name__ == "__main__":
    import uvicorn
    logger.info("Starting the API server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)