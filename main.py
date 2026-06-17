from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

tasks = []


class Task(BaseModel):
    title: str
    description: str
    completed: bool = False


@app.get("/")
def home():
    return {"message": "Task Manager API is running"}


@app.post("/tasks")
def create_task(task: Task):
    task_dict = task.model_dump()
    task_dict["id"] = len(tasks) + 1

    tasks.append(task_dict)

    return task_dict