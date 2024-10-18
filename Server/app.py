from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import engine, get_db
from models import Base, User
from pydantic import BaseModel
from typing import List
import uvicorn

from typing import Optional
import httpx
import re

# Initialize FastAPI
app = FastAPI()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

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

# Helper function to recursively get .py and .js files from GitHub repository
async def fetch_files_recursively(client, owner, repo, path=""):
    files = []
    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    
    response = await client.get(api_url)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch repository contents.")
    
    content = response.json()
    for item in content:
        if item['type'] == 'file' and item['name'].endswith(('.py', '.js')):
            files.append(item['path'])
        elif item['type'] == 'dir':
            # Recursively fetch files in the subdirectory
            subdir_files = await fetch_files_recursively(client, owner, repo, item['path'])
            files.extend(subdir_files)
    
    return files

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
