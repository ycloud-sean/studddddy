from typing import Annotated, Optional

from fastapi import FastAPI, HTTPException, Path, Query, Response, status
from pydantic import BaseModel, ConfigDict, Field

app = FastAPI(
    title="FastAPI Day 6 Todo API",
    description="内存版 Todo CRUD 练习",
)


class TodoCreate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "复习 FastAPI CRUD",
                "description": "把新增、查询、修改、删除接口都跑一遍",
                "priority": 2,
            }
        }
    )

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


class TodoUpdate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "完成 Todo API",
                "description": "整体替换这个待办",
                "priority": 4,
                "completed": True,
            }
        }
    )

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


class TodoRead(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    priority: int
    completed: bool


class TodoListResponse(BaseModel):
    count: int
    items: list[TodoRead]


class TodoDetailResponse(BaseModel):
    data: TodoRead


class TodoCreateResponse(BaseModel):
    message: str
    data: TodoRead


class TodoUpdateResponse(BaseModel):
    message: str
    data: TodoRead


todos = {
    1: {
        "id": 1,
        "title": "阅读 Day 6 教程",
        "description": "理解内存版 CRUD 的接口设计",
        "priority": 3,
        "completed": False,
        "internal_note": "学习数据，不返回给客户端",
    },
    2: {
        "id": 2,
        "title": "完成 Todo API 练习",
        "description": "在 /docs 里依次测试 CRUD 接口",
        "priority": 5,
        "completed": False,
        "internal_note": "重点练习 PUT、PATCH、DELETE",
    },
    3: {
        "id": 3,
        "title": "整理今天的问题",
        "description": None,
        "priority": 2,
        "completed": True,
        "internal_note": "可作为筛选 completed=true 的示例",
    },
}


def get_todo_or_404(todo_id: int) -> dict:
    todo = todos.get(todo_id)

    if todo is None:
        raise HTTPException(status_code=404, detail="Todo 不存在")

    return todo


@app.get("/")
async def root():
    return {"message": "FastAPI Day 6：内存版 Todo CRUD"}


@app.get("/todos", response_model=TodoListResponse)
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

    return {
        "count": len(result),
        "items": result[:limit],
    }


@app.get(
    "/todos/{todo_id}",
    response_model=TodoDetailResponse,
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
    response_model=TodoCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_todo(todo: TodoCreate):
    todo_id = max(todos.keys(), default=0) + 1
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
    response_model=TodoUpdateResponse,
    responses={404: {"description": "Todo 不存在"}},
)
async def replace_todo(
    todo_id: Annotated[
        int,
        Path(gt=0, description="Todo ID，必须大于 0"),
    ],
    todo: TodoUpdate,
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
    response_model=TodoUpdateResponse,
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
