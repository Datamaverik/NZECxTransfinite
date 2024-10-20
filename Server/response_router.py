from fastapi import APIRouter
from pydantic import BaseModel

# Define the response model using Pydantic
class RepoResponse(BaseModel):
    status: str
    repo_url: str
    issues_found: int
    recommendations: list

# Create a router
response_router = APIRouter()

# Define a POST route that accepts a repo evaluation request
@response_router.post("/response")
async def post_response(response: RepoResponse):
    # Here, you can process or log the response if needed
    return {
        "message": "Response received successfully",
        "data": response.dict()
    }
