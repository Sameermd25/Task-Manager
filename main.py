from fastapi import HTTPException
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import engine, SessionLocal
from models import Base, Task
from schemas import TaskCreate



Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"message": "Task Manager API"}


@app.post("/tasks")
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db)
):
    new_task = Task(
        title=task.title,
        description=task.description
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


@app.get("/tasks")
def get_tasks(
    db: Session = Depends(get_db)
):
    return db.query(Task).all()


@app.put("/tasks/{task_id}")
def update_task(
    task_id: int,
    task: TaskCreate,
    db: Session = Depends(get_db)
):
    db_task = db.query(Task).filter(
        Task.id == task_id
    ).first()

    if not db_task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    db_task.title = task.title
    db_task.description = task.description

    db.commit()
    db.refresh(db_task)

    return db_task


@app.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(
        Task.id == task_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    db.delete(task)
    db.commit()

    return {"message": "Task deleted"}






