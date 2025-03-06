from fastapi import APIRouter, Depends
from fastapi.security.api_key import APIKeyHeader
# import auth
from crud.dentalstall_crud import scrape_data

from model.dentalstall_model import *

router = APIRouter(
    dependencies=[Depends(APIKeyHeader(name="token"))],
)

@router.post("/scrape")
async def scrape(page: int = 1,proxy: str = None,):
    # calling scrape_data helper function that performs scaping
    return await scrape_data(page,proxy)

