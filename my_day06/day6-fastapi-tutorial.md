# Day 6 FastAPI 学习教程

今天只抓一件事：**把前 5 天学过的输入、输出、状态码和错误处理合起来，做一个内存版 Todo CRUD**。

前面几天已经分别学过：

- Day 3：路径参数、查询参数
- Day 4：请求体和 Pydantic 模型
- Day 5：响应模型、状态码、`HTTPException`

Day 6 要把这些组合成一组更像真实项目的接口。

---

## 1. 今天的目标

学完 Day 6，你应该能做到：

- 知道 CRUD 分别对应什么操作
- 能写出 Todo 的新增、查询、修改、删除接口
- 能区分 `POST`、`PUT`、`PATCH`、`DELETE` 的用途
- 能用 `model_dump(exclude_unset=True)` 做局部更新
- 能用内存字典模拟简单数据库
- 知道内存数据重启后会丢失

---

## 2. CRUD 是什么

CRUD 是后端接口里最常见的一组操作：

| 名称 | 含义 | 常见 HTTP 方法 | 例子 |
| --- | --- | --- | --- |
| Create | 新增 | `POST` | `POST /todos` |
| Read | 查询 | `GET` | `GET /todos`、`GET /todos/1` |
| Update | 修改 | `PUT`、`PATCH` | `PUT /todos/1`、`PATCH /todos/1` |
| Delete | 删除 | `DELETE` | `DELETE /todos/1` |

今天做的是“内存版 CRUD”。

所谓内存版，就是数据先放在 Python 字典里：

```python
todos = {
    1: {
        "id": 1,
        "title": "阅读 Day 6 教程",
        "description": "理解内存版 CRUD 的接口设计",
        "priority": 3,
        "completed": False,
    }
}
```

它的好处是简单，不需要先学数据库。

它的限制也很明显：应用一重启，运行过程中新增或修改的数据就会丢失。

---

## 3. 今天要完成的接口

代码里会实现这 6 个接口：

| 接口 | 作用 |
| --- | --- |
| `GET /todos` | 查询 Todo 列表 |
| `GET /todos/{todo_id}` | 查询 Todo 详情 |
| `POST /todos` | 新增 Todo |
| `PUT /todos/{todo_id}` | 整体替换 Todo |
| `PATCH /todos/{todo_id}` | 局部修改 Todo |
| `DELETE /todos/{todo_id}` | 删除 Todo |

这就是一个资源的完整 CRUD。

---

## 4. Todo 的模型拆分

真实项目里，不建议一个模型从头用到尾。

因为不同接口需要的字段不一样。

### 4.1 新增模型 `TodoCreate`

新增 Todo 时，客户端只需要传：

```python
class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: int = 3
```

注意没有 `id`，因为 `id` 应该由后端生成。

也没有 `completed`，因为新创建的 Todo 默认应该是未完成。

### 4.2 整体更新模型 `TodoUpdate`

整体更新表示“用这份新数据替换旧数据”。

所以 `TodoUpdate` 会包含完整可写字段：

```python
class TodoUpdate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: int = 3
    completed: bool = False
```

如果你用 `PUT /todos/1`，通常要传完整对象。

### 4.3 局部更新模型 `TodoPatch`

局部更新表示“只改传进来的字段”。

所以 `TodoPatch` 里的字段全部是可选的：

```python
class TodoPatch(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[int] = None
    completed: Optional[bool] = None
```

比如只想把 Todo 标记为完成，可以只传：

```json
{
  "completed": true
}
```

---

## 5. 查询列表：`GET /todos`

列表接口支持几个查询参数：

- `q`：按标题关键字搜索
- `completed`：按完成状态筛选
- `min_priority`：按最低优先级筛选
- `limit`：限制最多返回多少条

代码核心是先取出全部数据，再一层层筛选：

```python
result = list(todos.values())

if q:
    result = [
        todo
        for todo in result
        if q.lower() in todo["title"].lower()
    ]

if completed is not None:
    result = [
        todo
        for todo in result
        if todo["completed"] == completed
    ]
```

这里有一个细节：

```python
if completed is not None:
```

不要写成：

```python
if completed:
```

因为 `completed=false` 也是一个有效筛选条件。写成 `if completed:` 会把 `False` 当成没传。

---

## 6. 查询详情：`GET /todos/{todo_id}`

详情接口从路径里拿 `todo_id`：

```python
@app.get("/todos/{todo_id}", response_model=TodoDetailResponse)
async def get_todo(todo_id: int):
    return {"data": get_todo_or_404(todo_id)}
```

为了避免多个接口重复写“查不到就报 404”，代码里抽了一个小函数：

```python
def get_todo_or_404(todo_id: int) -> dict:
    todo = todos.get(todo_id)

    if todo is None:
        raise HTTPException(status_code=404, detail="Todo 不存在")

    return todo
```

后面更新和删除也会复用它。

---

## 7. 新增：`POST /todos`

新增接口做三件事：

1. 根据当前最大 `id` 生成新的 `todo_id`
2. 把请求体模型转成字典
3. 存进内存字典

```python
@app.post("/todos", status_code=status.HTTP_201_CREATED)
async def create_todo(todo: TodoCreate):
    todo_id = max(todos.keys(), default=0) + 1
    new_todo = {
        "id": todo_id,
        **todo.model_dump(),
        "completed": False,
    }

    todos[todo_id] = new_todo
    return {"message": "Todo 创建成功", "data": new_todo}
```

`status.HTTP_201_CREATED` 表示资源创建成功。

---

## 8. 整体更新：`PUT /todos/{todo_id}`

`PUT` 更像“整体替换”。

如果旧 Todo 是：

```json
{
  "title": "旧标题",
  "description": "旧说明",
  "priority": 2,
  "completed": false
}
```

你用 `PUT` 传：

```json
{
  "title": "新标题",
  "priority": 5,
  "completed": true
}
```

那么没有传的字段会使用模型默认值，比如 `description` 会变成 `null`。

代码里先确认资源存在，再替换整条数据：

```python
get_todo_or_404(todo_id)
updated_todo = {
    "id": todo_id,
    **todo.model_dump(),
}
todos[todo_id] = updated_todo
```

---

## 9. 局部更新：`PATCH /todos/{todo_id}`

`PATCH` 更像“只改一部分”。

它的重点是：

```python
update_data = todo.model_dump(exclude_unset=True)
```

`exclude_unset=True` 的意思是：只导出客户端真正传进来的字段。

比如请求体是：

```json
{
  "completed": true
}
```

那么 `update_data` 只会是：

```python
{"completed": True}
```

不会把没传的 `title`、`description`、`priority` 覆盖掉。

完整思路：

```python
stored_todo = get_todo_or_404(todo_id)
update_data = todo.model_dump(exclude_unset=True)
updated_todo = {
    **stored_todo,
    **update_data,
}
todos[todo_id] = updated_todo
```

后面的 `update_data` 会覆盖前面的同名字段。

---

## 10. 删除：`DELETE /todos/{todo_id}`

删除接口先确认 Todo 存在，再从字典里删掉：

```python
get_todo_or_404(todo_id)
del todos[todo_id]
return Response(status_code=status.HTTP_204_NO_CONTENT)
```

`204 No Content` 表示请求成功了，但响应体没有内容。

所以删除成功时，客户端只需要看状态码，不需要看 JSON。

---

## 11. 为什么响应里没有 `internal_note`

代码里的内存数据故意放了一个内部字段：

```python
"internal_note": "学习数据，不返回给客户端"
```

但响应模型 `TodoRead` 没有这个字段：

```python
class TodoRead(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    priority: int
    completed: bool
```

因为接口都设置了 `response_model`，FastAPI 会按照响应模型过滤返回字段。

这和 Day 5 的商品接口是同一个知识点。

---

## 12. 运行方式

在仓库根目录运行：

```bash
fastapi dev my_day06/main.py
```

或者：

```bash
uvicorn my_day06.main:app --reload
```

然后打开：

```text
http://127.0.0.1:8000/docs
```

建议按这个顺序测试：

1. `GET /todos` 看初始数据
2. `GET /todos/1` 查详情
3. `POST /todos` 新增一条
4. `PATCH /todos/1` 只把 `completed` 改成 `true`
5. `PUT /todos/2` 整体替换一条
6. `DELETE /todos/3` 删除一条
7. 再访问 `GET /todos/3`，确认会返回 `404`

---

## 13. 今日小练习

请你自己尝试完成这些练习：

1. 给 `GET /todos` 增加一个 `max_priority` 查询参数。
2. 给 `TodoCreate` 增加一个 `tag` 字段，表示 Todo 分类。
3. 试试看 `PATCH /todos/1` 传空 JSON `{}` 会发生什么。
4. 把 `DELETE /todos/{todo_id}` 改成返回 `{"message": "删除成功"}`，并思考它还能不能继续用 `204`。

---

## 14. 今天要记住的句子

CRUD 不是新语法，而是一组接口设计习惯。

`POST` 负责新增，`GET` 负责查询，`PUT/PATCH` 负责更新，`DELETE` 负责删除。

内存字典可以帮你练接口设计，但真正项目最终要换成数据库。
