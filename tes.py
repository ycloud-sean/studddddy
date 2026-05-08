
todos = {
    1: {"id": 1, "title": "学习 FastAPI Day 2", "done": False},
    2: {"id": 2, "title": "练习 GET", "done": False},
}

todo_list = list(todos.values())

print(todo_list[0]["id"])
print(todo_list[1]["id"])


first_todo = next(iter(todos.values()))

print(todos.keys())


