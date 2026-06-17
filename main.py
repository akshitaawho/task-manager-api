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

@app.get("/tasks")
def get_tasks():
    return tasks


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    return {"error": "Task not found"}