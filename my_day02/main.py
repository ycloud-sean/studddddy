from fastapi import FastAPI, HTTPException, Response, status

app = FastAPI()

todos = {
    1: {"id": 1, "title": "学习 FastAPI Day 2", "done": False}
}


@app.get("/")
async def root():
    return {"message": "Hello FastAPI"}


@app.get("/todos")
async def get_todos():
    return {"data": list(todos.values())}


@app.get("/todos/{todo_id}")
async def get_todo(todo_id: int):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")

    return todos[todo_id]


@app.post("/todos", status_code=status.HTTP_201_CREATED)
async def create_todo(title: str):
    todo_id = max(todos.keys()) + 1

    todos[todo_id] = {
        "id": todo_id,
        "title": title,
        "done": False,
    }

    return todos[todo_id]


@app.put("/todos/{todo_id}")
async def update_todo(todo_id: int, title: str, done: bool = False):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")

    todos[todo_id] = {
        "id": todo_id,
        "title": title,
        "done": done,
    }

    return todos[todo_id]


@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: int):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")

    del todos[todo_id]

    return Response(status_code=status.HTTP_204_NO_CONTENT)
