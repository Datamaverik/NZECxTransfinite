from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import engine, get_db
from models import Base, User
from pydantic import BaseModel
from typing import List
import uvicorn
from dotenv import load_dotenv
from typing import Optional
import httpx
import re
import os
import base64

# Initialize FastAPI
app = FastAPI()

# Create database tables on startup
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Pydantic schema for User
class UserCreate(BaseModel):
    name: str
    email: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True

# Create User
@app.post("/users/", response_model=UserResponse)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    new_user = User(name=user.name, email=user.email)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

# Get all users
@app.get("/users/", response_model=List[UserResponse])
async def read_users(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).offset(skip).limit(limit))
    users = result.scalars().all()
    return users

# Get user by ID
@app.get("/users/{user_id}", response_model=UserResponse)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Update user
@app.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    db_user = result.scalar_one_or_none()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db_user.name = user.name
    db_user.email = user.email
    await db.commit()
    await db.refresh(db_user)
    return db_user

# Delete user
@app.delete("/users/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    await db.delete(user)
    await db.commit()
    return {"detail": "User deleted"}

# Your GitHub token
load_dotenv()
GITHUB_TOKEN=os.getenv("GITHUB_TOKEN")

# Helper function to recursively get .py and .js files from GitHub repository
async def fetch_files_recursively(client, owner, repo, path=""):
    files = []
    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = await client.get(api_url, headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch repository contents.")
    
    content = response.json()
    for item in content:
        if item['type'] == 'file' and item['name'].endswith(('.py', '.js', '.cpp')):
            files.append(item['path'])
        elif item['type'] == 'dir':
            # Recursively fetch files in the subdirectory
            subdir_files = await fetch_files_recursively(client, owner, repo, item['path'])
            files.extend(subdir_files)
    
    return files

# Fetch the content of a specific file
async def fetch_file_content(client, owner, repo, path):
    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = await client.get(api_url, headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=f"Failed to fetch content for {path}.")
    
    content = response.json()
    # Decode the content from base64 (GitHub's API returns file content encoded in base64)
    file_content = base64.b64decode(content['content']).decode('utf-8')
    
    return {
        "path": path,
        "content": file_content
    }

# Endpoint to get .py and .js files from a GitHub repository
@app.get("/get_repo_files")
async def get_repo_files(repo_link: str):
    match = re.match(r"https://github.com/([\w-]+)/([\w-]+)", repo_link)
    if not match:
        raise HTTPException(status_code=400, detail="Invalid GitHub repository link.")
    
    owner, repo = match.groups()
    
    async with httpx.AsyncClient() as client:
        files = await fetch_files_recursively(client, owner, repo)
    
    return {"files": files}

# Endpoint to get the content of .py and .js files in JSON format
@app.get("/get_repo_files_content")
async def get_repo_files_content(repo_link: str):
    match = re.match(r"https://github.com/([\w-]+)/([\w-]+)", repo_link)
    if not match:
        raise HTTPException(status_code=400, detail="Invalid GitHub repository link.")
    
    owner, repo = match.groups()
    
    async with httpx.AsyncClient() as client:
        # Fetch the paths of the .py and .js files
        files = await fetch_files_recursively(client, owner, repo)
        
        # Fetch content for each file
        files_content = []
        for file_path in files:
            content = await fetch_file_content(client, owner, repo, file_path)
            files_content.append(content)
    
    return {"files": files_content}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
