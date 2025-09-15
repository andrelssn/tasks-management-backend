from fastapi import FastAPI, Depends, HTTPException, status
from sqlmodel import Session
from .db import init_db, get_session
from .schemas import TaskCreate, TaskUpdate, TaskRead
from .crud import get_tasks, get_task, create_task, update_task, delete_task

app = FastAPI(title="Tasks API - FastAPI + SQLite")

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/tasks", response_model=list[TaskRead])
def list_tasks(session: Session = Depends(get_session)):
    return get_tasks(session)

@app.post("/tasks", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task_endpoint(payload: TaskCreate, session: Session = Depends(get_session)):
    task = create_task(session, title=payload.title, description=payload.description)
    return task

@app.get("/tasks/{task_id}", response_model=TaskRead)
def get_task_endpoint(task_id: int, session: Session = Depends(get_session)):
    task = get_task(session, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}", response_model=TaskRead)
def update_task_endpoint(task_id: int, payload: TaskUpdate, session: Session = Depends(get_session)):
    task = get_task(session, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    updated = update_task(session, task, payload.dict(exclude_unset=True))
    return updated

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task_endpoint(task_id: int, session: Session = Depends(get_session)):
    task = get_task(session, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    delete_task(session, task)
    return None
