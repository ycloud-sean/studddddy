# Day 7 FastAPI 学习教程

今天只抓一件事：**把第一周的 Todo API 做一次复盘和重构，让它更像一个可以交付的小项目**。

Day 1 到 Day 6 已经学过：

- 启动 FastAPI 应用
- 写不同 HTTP 方法的接口
- 使用路径参数和查询参数
- 使用 Pydantic 接收请求体
- 使用响应模型过滤输出字段
- 使用状态码和 `HTTPException`
- 完成内存版 Todo CRUD

Day 7 不急着学新语法，而是练习一个很重要的能力：**把能跑的代码整理成别人能读、能测、能维护的代码**。

---

## 1. 今天的目标

学完 Day 7，你应该能做到：

- 能复盘第一周学过的 FastAPI 基础能力
- 知道“重构”不是重写，而是在不改变核心功能的前提下整理代码
- 能给接口补充 `tags`、`summary`、`description`，让 `/docs` 更清楚
- 能写一个简单的项目 `README.md`
- 能写一份接口文档 `api-docs.md`
- 能用一组手动测试步骤检查 Todo API 是否完整

---

## 2. Day 7 做了什么

Day 6 已经完成了 Todo CRUD。

Day 7 在 Day 6 的基础上做了这些整理：

| 整理点 | 目的 |
| --- | --- |
| 增加应用标题、描述、版本号 | 让 `/docs` 首页更像一个真实 API |
| 增加 `tags_metadata` | 让接口按 `health`、`todos`、`review` 分组 |
| 给接口增加 `summary` 和 `description` | 让接口文档更容易读 |
| 抽出 `TodoBase` | 减少 `TodoCreate` 和 `TodoReplace` 的重复字段 |
| 抽出 `get_next_todo_id()` | 让创建 Todo 的代码意图更清楚 |
| 新增 `/health` | 提供健康检查接口 |
| 新增 `/todos/stats` | 用统计接口辅助复盘 |
| 新增 `README.md` 和 `api-docs.md` | 练习项目说明和接口文档 |

---

## 3. 什么是重构

重构不是“推倒重写”。

重构是：

> 在尽量不改变外部功能的前提下，让内部代码更清楚、更少重复、更容易维护。

比如 Day 6 里创建新 ID 的代码写在接口函数里：

```python
todo_id = max(todos.keys(), default=0) + 1
```

Day 7 把它抽成函数：

```python
def get_next_todo_id() -> int:
    return max(todos.keys(), default=0) + 1
```

这样创建接口里读起来更像业务步骤：

```python
todo_id = get_next_todo_id()
```

这就是很小但很实用的重构。

---

## 4. 给 `/docs` 加清楚的分组

FastAPI 的自动文档不是只能“自动生成”，也可以被我们主动整理。

Day 7 里先定义接口分组说明：

```python
tags_metadata = [
    {
        "name": "health",
        "description": "检查服务是否正常运行。",
    },
    {
        "name": "todos",
        "description": "内存版 Todo 的新增、查询、修改和删除接口。",
    },
    {
        "name": "review",
        "description": "第一周小项目的复盘辅助接口。",
    },
]
```

再传给 `FastAPI`：

```python
app = FastAPI(
    title="FastAPI Day 7 Todo API",
    description="第一周复盘项目：把 Day 6 的内存版 Todo CRUD 整理成更清楚的代码和接口文档。",
    version="1.0.0",
    openapi_tags=tags_metadata,
)
```

打开 `/docs` 时，接口就会按分组展示。

---

## 5. 给接口加 `summary` 和 `description`

Day 6 的接口能用，但文档信息还比较少。

Day 7 给接口加了更明确的说明：

```python
@app.get(
    "/todos",
    response_model=TodoListResponse,
    tags=["todos"],
    summary="查询 Todo 列表",
    description="支持按关键字、完成状态、最低优先级筛选，并限制返回数量。",
)
async def list_todos(...):
    ...
```

这几个参数都服务于 `/docs`：

- `tags`：接口分组
- `summary`：接口标题
- `description`：接口详细说明
- `responses`：补充错误响应说明

写项目时，文档清楚很重要。因为未来读接口的人，可能是前端同事，也可能是几周后的你自己。

---

## 6. 抽出 `TodoBase`

Day 6 里 `TodoCreate` 和 `TodoUpdate` 都有这些字段：

- `title`
- `description`
- `priority`

Day 7 把公共字段放进 `TodoBase`：

```python
class TodoBase(BaseModel):
    title: Annotated[
        str,
        Field(min_length=1, max_length=80, description="待办标题"),
    ]
    description: Annotated[
        Optional[str],
        Field(max_length=300, description="待办说明"),
    ] = None
    priority: Annotated[
        int,
        Field(ge=1, le=5, description="优先级，1 最低，5 最高"),
    ] = 3
```

然后新增模型可以继承它：

```python
class TodoCreate(TodoBase):
    ...
```

整体替换模型也可以继承它，再额外增加 `completed`：

```python
class TodoReplace(TodoBase):
    completed: bool = False
```

这样能减少重复，也能让模型关系更清楚。

---

## 7. 为什么 `TodoPatch` 没有继承 `TodoBase`

这是一个关键点。

`TodoPatch` 是局部更新模型，它里面所有字段都应该可选：

```python
class TodoPatch(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[int] = None
    completed: Optional[bool] = None
```

而 `TodoBase` 里的 `title` 是必填字段。

如果让 `TodoPatch` 继承 `TodoBase`，那 `PATCH /todos/1` 只传：

```json
{
  "completed": true
}
```

就会因为缺少 `title` 而校验失败。

所以 Day 7 保留了单独的 `TodoPatch`。

---

## 8. 新增健康检查接口

Day 7 新增了：

```python
@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["health"],
    summary="健康检查",
)
async def health_check():
    return {
        "status": "ok",
        "service": "day7-todo-api",
        "version": "1.0.0",
    }
```

健康检查接口常见于真实项目。

它的作用是快速告诉外部系统：

- 服务还活着
- 当前服务叫什么
- 当前版本是多少

后面学部署时，`/health` 会非常常见。

---

## 9. 新增统计接口

Day 7 还新增了：

```python
@app.get("/todos/stats", response_model=TodoStatsResponse)
async def get_todo_stats():
    return {"data": build_todo_stats()}
```

统计逻辑放在函数里：

```python
def build_todo_stats() -> TodoStats:
    total = len(todos)
    completed_count = sum(
        1
        for todo in todos.values()
        if todo["completed"]
    )
    high_priority_count = sum(
        1
        for todo in todos.values()
        if todo["priority"] >= 4
    )

    return TodoStats(
        total=total,
        completed=completed_count,
        active=total - completed_count,
        high_priority=high_priority_count,
    )
```

这也是一种小重构：接口函数只负责处理 HTTP 请求，具体统计逻辑放到普通 Python 函数里。

---

## 10. README 应该写什么

`README.md` 不需要一开始就写得很长。

对一个学习项目来说，先写清楚这些就很好：

- 项目是什么
- 怎么运行
- 有哪些接口
- 推荐怎么测试
- 当前限制是什么

Day 7 的 `README.md` 就围绕这些内容展开。

以后项目变大，README 可以继续补：

- 环境变量
- 数据库配置
- 测试命令
- 部署方式
- 常见问题

---

## 11. 接口文档应该写什么

接口文档最重要的是让别人知道：

- 请求方法是什么
- 路径是什么
- 请求参数有哪些
- 请求体长什么样
- 成功响应长什么样
- 常见错误是什么

比如新增 Todo：

```text
POST /todos
```

请求体：

```json
{
  "title": "完成第一周复盘",
  "description": "整理 Todo API 的接口文档和测试步骤",
  "priority": 4
}
```

成功响应：

```json
{
  "message": "Todo 创建成功",
  "data": {
    "id": 4,
    "title": "完成第一周复盘",
    "description": "整理 Todo API 的接口文档和测试步骤",
    "priority": 4,
    "completed": false
  }
}
```

这些内容已经整理在 `api-docs.md` 里。

---

## 12. 运行方式

在仓库根目录运行：

```bash
uvicorn my_day07.main:app --reload
```

或者：

```bash
fastapi dev my_day07/main.py
```

然后打开：

```text
http://127.0.0.1:8000/docs
```

---

## 13. 推荐验收顺序

建议按这个顺序检查 Day 7：

1. `GET /health`：确认服务正常。
2. `GET /todos`：查看 Todo 列表。
3. `GET /todos/stats`：查看统计数据。
4. `POST /todos`：新增一条 Todo。
5. `PATCH /todos/{todo_id}`：只修改 `completed`。
6. `PUT /todos/{todo_id}`：整体替换 Todo。
7. `DELETE /todos/{todo_id}`：删除 Todo。
8. `GET /todos/{todo_id}`：确认删除后返回 `404`。

---

## 14. 第一周复盘清单

请你用自己的话确认这些问题：

- `GET`、`POST`、`PUT`、`PATCH`、`DELETE` 分别适合什么场景？
- 路径参数和查询参数有什么区别？
- 请求体为什么适合放复杂对象？
- `response_model` 为什么能过滤内部字段？
- `HTTPException(status_code=404)` 适合什么时候用？
- `PATCH` 为什么要配合 `model_dump(exclude_unset=True)`？
- `204 No Content` 为什么不应该再返回 JSON？
- README 和接口文档分别解决什么问题？

---

## 15. 今天要记住的句子

能跑只是第一步。

Day 7 的目标是让代码更清楚，让接口文档更清楚，让未来的自己更容易继续开发。
