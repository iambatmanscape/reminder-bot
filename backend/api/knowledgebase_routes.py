from backend.utils.create_embeddings import process_auto, process_web, search_query, SearchParams, ProcessAutoInputs
from fastapi import APIRouter,Body,Path,HTTPException
from typing import Dict
import logging
logging.basicConfig(level=logging.INFO)

router = APIRouter()



@router.post('/add-data', status_code=200)
async def add_data(input_vars: ProcessAutoInputs = Body(..., description="The body of Input variable")):
    """
    Adds data to the knowledgebase using the process_auto utility.
    """
    try:
        result = await process_auto(input_vars)
        return {"success": True, "result": result}
    except Exception as e:
        logging.error(f"Error in add_data: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post('/add-web-data', status_code=200)
async def add_web_data(input_vars: Dict[str, str] = Body(..., description="The body of Input variable")):
    """
    Adds web data to the knowledgebase using the process_web utility.
    """
    try:
        result = await process_web(input_vars)
        return {"success": True, "result": result}
    except Exception as e:
        logging.error(f"Error in add_web_data: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get('/search', status_code=200)
async def search(
    search_params: SearchParams = Body(..., description="The body of Search parameters")
):
    """
    Searches the knowledgebase using the provided query and returns the top k results.
    """
    try:
        result = await search_query(search_params)
        return {"success": True, "result": result}
    except Exception as e:
        logging.error(f"Error in search: {e}")
        raise HTTPException(status_code=500, detail=str(e))
