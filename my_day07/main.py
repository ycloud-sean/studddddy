from typing import Annotated, Optional

from fastapi import FastAPI, HTTPException, Path, Query, Response, status
from pydantic import BaseModel, ConfigDict, Field

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

app = FastAPI(
    title="FastAPI Day 7 Todo API",
    description=(
        "第一周复盘项目：把 Day 6 的内存版 Todo CRUD "
        "整理成更清楚的代码和接口文档。"
    ),
    version="1.0.0",
    openapi_tags=tags_metadata,
)


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


class TodoCreate(TodoBase):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "完成第一周复盘",
                "description": "整理 Todo API 的接口文档和测试步骤",
                "priority": 4,
            }
        }
    )


class TodoReplace(TodoBase):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "重构 Todo API",
                "description": "整体替换 Todo 内容",
                "priority": 5,
                "completed": True,
            }
        }
    )

    completed: Annotated[
        bool,
        Field(description="是否完成"),
    ] = False


class TodoPatch(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "completed": True,
            }
        }
    )

    title: Annotated[
        Optional[str],
        Field(min_length=1, max_length=80, description="待办标题"),
    ] = None
    description: Annotated[
        Optional[str],
        Field(max_length=300, description="待办说明"),
    ] = None
    priority: Annotated[
        Optional[int],
        Field(ge=1, le=5, description="优先级，1 最低，5 最高"),
    ] = None
    completed: Annotated[
        Optional[bool],
        Field(description="是否完成"),
    ] = None


class TodoRead(TodoBase):
    id: int
    completed: bool


class TodoListResponse(BaseModel):
    count: int
    items: list[TodoRead]


class TodoDetailResponse(BaseModel):
    data: TodoRead


class TodoWriteResponse(BaseModel):
    message: str
    data: TodoRead


class TodoStats(BaseModel):
    total: int
    completed: int
    active: int
    high_priority: int


class TodoStatsResponse(BaseModel):
    data: TodoStats


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str


todos = {
    1: {
        "id": 1,
        "title": "复盘路径参数和查询参数",
        "description": "确认自己能解释 /todos/1 和 /todos?completed=false 的区别",
        "priority": 3,
        "completed": True,
        "internal_note": "Day 3 知识点",
    },
    2: {
        "id": 2,
        "title": "复盘请求体和 Pydantic",
        "description": "确认自己能写 TodoCreate、TodoPatch 和 TodoRead",
        "priority": 4,
        "completed": False,
        "internal_note": "Day 4 和 Day 6 知识点",
    },
    3: {
        "id": 3,
        "title": "整理 Todo API 文档",
        "description": "补充 README 和接口表格",
        "priority": 5,
        "completed": False,
        "internal_note": "Day 7 交付物",
    },
}


def get_next_todo_id() -> int:
    return max(todos.keys(), default=0) + 1


def get_todo_or_404(todo_id: int) -> dict:
    todo = todos.get(todo_id)

    if todo is None:
        raise HTTPException(status_code=404, detail="Todo 不存在")

    return todo


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


@app.get(
    "/",
    tags=["health"],
    summary="查看项目欢迎信息",
)
async def root():
    return {
        "message": "FastAPI Day 7：第一周复盘和 Todo API 重构",
        "docs": "/docs",
        "health": "/health",
    }


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


@app.get(
    "/todos",
    response_model=TodoListResponse,
    tags=["todos"],
    summary="查询 Todo 列表",
    description="支持按关键字、完成状态、最低优先级筛选，并限制返回数量。",
)
async def list_todos(
    q: Annotated[
        Optional[str],
        Query(description="按标题关键字搜索"),
    ] = None,
    completed: Annotated[
        Optional[bool],
        Query(description="按完成状态筛选"),
    ] = None,
    min_priority: Annotated[
        int,
        Query(ge=1, le=5, description="最低优先级"),
    ] = 1,
    limit: Annotated[
        int,
        Query(ge=1, le=50, description="最多返回多少条 Todo"),
    ] = 50,
):
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

    result = [
        todo
        for todo in result
        if todo["priority"] >= min_priority
    ]
    result.sort(key=lambda todo: (-todo["priority"], todo["id"]))

    return {
        "count": len(result),
        "items": result[:limit],
    }


@app.get(
    "/todos/stats",
    response_model=TodoStatsResponse,
    tags=["review"],
    summary="查看 Todo 统计信息",
    description="用于复盘当前内存数据里的总数、完成数、未完成数和高优先级数量。",
)
async def get_todo_stats():
    return {"data": build_todo_stats()}


@app.get(
    "/todos/{todo_id}",
    response_model=TodoDetailResponse,
    tags=["todos"],
    summary="查询 Todo 详情",
    responses={404: {"description": "Todo 不存在"}},
)
async def get_todo(
    todo_id: Annotated[
        int,
        Path(gt=0, description="Todo ID，必须大于 0"),
    ],
):
    return {"data": get_todo_or_404(todo_id)}


@app.post(
    "/todos",
    response_model=TodoWriteResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["todos"],
    summary="新增 Todo",
)
async def create_todo(todo: TodoCreate):
    todo_id = get_next_todo_id()
    new_todo = {
        "id": todo_id,
        **todo.model_dump(),
        "completed": False,
        "internal_note": "新创建 Todo，暂时只保存在内存里",
    }

    todos[todo_id] = new_todo

    return {
        "message": "Todo 创建成功",
        "data": new_todo,
    }


@app.put(
    "/todos/{todo_id}",
    response_model=TodoWriteResponse,
    tags=["todos"],
    summary="整体替换 Todo",
    description="用请求体里的完整 Todo 数据替换已有 Todo。",
    responses={404: {"description": "Todo 不存在"}},
)
async def replace_todo(
    todo_id: Annotated[
        int,
        Path(gt=0, description="Todo ID，必须大于 0"),
    ],
    todo: TodoReplace,
):
    get_todo_or_404(todo_id)
    updated_todo = {
        "id": todo_id,
        **todo.model_dump(),
        "internal_note": "整体替换后的 Todo",
    }
    todos[todo_id] = updated_todo

    return {
        "message": "Todo 整体更新成功",
        "data": updated_todo,
    }


@app.patch(
    "/todos/{todo_id}",
    response_model=TodoWriteResponse,
    tags=["todos"],
    summary="局部修改 Todo",
    description="只修改请求体里实际传入的字段。",
    responses={404: {"description": "Todo 不存在"}},
)
async def update_todo(
    todo_id: Annotated[
        int,
        Path(gt=0, description="Todo ID，必须大于 0"),
    ],
    todo: TodoPatch,
):
    stored_todo = get_todo_or_404(todo_id)
    update_data = todo.model_dump(exclude_unset=True)
    updated_todo = {
        **stored_todo,
        **update_data,
    }
    todos[todo_id] = updated_todo

    return {
        "message": "Todo 局部更新成功",
        "data": updated_todo,
    }


@app.delete(
    "/todos/{todo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["todos"],
    summary="删除 Todo",
    responses={404: {"description": "Todo 不存在"}},
)
async def delete_todo(
    todo_id: Annotated[
        int,
        Path(gt=0, description="Todo ID，必须大于 0"),
    ],
):
    get_todo_or_404(todo_id)
    del todos[todo_id]

    return Response(status_code=status.HTTP_204_NO_CONTENT)
