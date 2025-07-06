from fastapi import UploadFile, File, APIRouter
from finsight_app.rag_utils import process_and_embed_file

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    filename = file.filename
    try:
        process_and_embed_file(filename, content.decode())
        return {"status": "success", "message": f"{filename} processed and indexed."}
    except Exception as e:
        return {"status": "error", "message": str(e)} 