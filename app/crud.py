from sqlmodel import select
from sqlmodel import Session
from .models import Task
from datetime import datetime
from typing import List, Optional

def get_tasks(session: Session) -> List[Task]:
    return session.exec(select(Task).order_by(Task.created_at)).all()

def get_task(session: Session, task_id: int) -> Optional[Task]:
    return session.get(Task, task_id)

def create_task(session: Session, title: str, description: Optional[str] = None) -> Task:
    task = Task(title=title, description=description)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

def update_task(session: Session, task: Task, data: dict) -> Task:
    for k, v in data.items():
        setattr(task, k, v)
    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

def delete_task(session: Session, task: Task) -> None:
    session.delete(task)
    session.commit()
