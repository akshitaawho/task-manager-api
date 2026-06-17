from fastapi import FastAPI
from pydantic import BaseModel

# we create the fastapi application object
app = FastAPI()

# initially, this is empty, created tasks can be stored here in JSON
tasks = []

# structure of all tasks, predefined false because its a to do/ task manager type of thing, so if you dont put anything, its just default false
class Task(BaseModel):
    title: str
    description: str
    completed: bool = False

# this is for PATCH requests, here all fields arent needed.
class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None


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


@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: Task):
    for task in tasks:
        if task["id"] == task_id:

            task["title"] = updated_task.title
            task["description"] = updated_task.description
            task["completed"] = updated_task.completed

            return task

    return {"error": "Task not found"}


@app.patch("/tasks/{task_id}")
def patch_task(task_id: int, task_update: TaskUpdate):
    for task in tasks:
        if task["id"] == task_id:

            updates = task_update.model_dump(exclude_unset=True)

            task.update(updates)

            return task

    return {"error": "Task not found"}


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:

            tasks.remove(task)

            return {"message": "Task deleted successfully"}

    return {"error": "Task not found"}