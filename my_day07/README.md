# Day 7 Todo API

这是第一周 FastAPI 学习的小项目复盘版：一个使用内存字典保存数据的 Todo API。

本项目用于练习：

- FastAPI 应用启动
- 路径参数和查询参数
- Pydantic 请求模型和响应模型
- CRUD 接口设计
- 状态码和错误处理
- `/docs` 自动文档整理
- README 和接口文档编写

## 运行方式

在仓库根目录运行：

```bash
uvicorn my_day07.main:app --reload
```

或者：

```bash
fastapi dev my_day07/main.py
```

打开接口文档：

```text
http://127.0.0.1:8000/docs
```

## 接口列表

| 方法 | 路径 | 作用 |
| --- | --- | --- |
| `GET` | `/` | 查看欢迎信息 |
| `GET` | `/health` | 健康检查 |
| `GET` | `/todos` | 查询 Todo 列表 |
| `GET` | `/todos/stats` | 查看 Todo 统计 |
| `GET` | `/todos/{todo_id}` | 查询 Todo 详情 |
| `POST` | `/todos` | 新增 Todo |
| `PUT` | `/todos/{todo_id}` | 整体替换 Todo |
| `PATCH` | `/todos/{todo_id}` | 局部修改 Todo |
| `DELETE` | `/todos/{todo_id}` | 删除 Todo |

## 推荐测试顺序

1. 打开 `/docs`。
2. 执行 `GET /health`，确认服务正常。
3. 执行 `GET /todos`，查看初始 Todo。
4. 执行 `POST /todos`，新增 Todo。
5. 执行 `PATCH /todos/{todo_id}`，只修改 `completed`。
6. 执行 `PUT /todos/{todo_id}`，整体替换 Todo。
7. 执行 `DELETE /todos/{todo_id}`，删除 Todo。
8. 再执行 `GET /todos/{todo_id}`，确认返回 `404`。

## 当前限制

- 数据保存在内存字典里，服务重启后运行期间新增或修改的数据会丢失。
- 当前还没有数据库、用户登录、权限控制和自动化测试。
- 这是第一周学习项目，重点是理解接口设计和 FastAPI 基础能力。
