# Day 7 Todo API 接口文档

基础地址：

```text
http://127.0.0.1:8000
```

交互式文档：

```text
http://127.0.0.1:8000/docs
```

## 1. 健康检查

```text
GET /health
```

成功响应：

```json
{
  "status": "ok",
  "service": "day7-todo-api",
  "version": "1.0.0"
}
```

## 2. 查询 Todo 列表

```text
GET /todos
```

查询参数：

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `q` | `string` | 否 | 按标题关键字搜索 |
| `completed` | `boolean` | 否 | 按完成状态筛选 |
| `min_priority` | `integer` | 否 | 最低优先级，范围 `1` 到 `5` |
| `limit` | `integer` | 否 | 最多返回多少条，范围 `1` 到 `50` |

示例：

```text
GET /todos?completed=false&min_priority=4
```

成功响应：

```json
{
  "count": 2,
  "items": [
    {
      "id": 3,
      "title": "整理 Todo API 文档",
      "description": "补充 README 和接口表格",
      "priority": 5,
      "completed": false
    }
  ]
}
```

## 3. 查看 Todo 统计

```text
GET /todos/stats
```

成功响应：

```json
{
  "data": {
    "total": 3,
    "completed": 1,
    "active": 2,
    "high_priority": 2
  }
}
```

## 4. 查询 Todo 详情

```text
GET /todos/{todo_id}
```

路径参数：

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `todo_id` | `integer` | 是 | Todo ID，必须大于 `0` |

成功响应：

```json
{
  "data": {
    "id": 1,
    "title": "复盘路径参数和查询参数",
    "description": "确认自己能解释 /todos/1 和 /todos?completed=false 的区别",
    "priority": 3,
    "completed": true
  }
}
```

错误响应：

```json
{
  "detail": "Todo 不存在"
}
```

## 5. 新增 Todo

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

成功状态码：

```text
201 Created
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

## 6. 整体替换 Todo

```text
PUT /todos/{todo_id}
```

请求体：

```json
{
  "title": "重构 Todo API",
  "description": "整体替换 Todo 内容",
  "priority": 5,
  "completed": true
}
```

说明：

- `PUT` 更适合整体替换。
- 请求体应该表达一份完整的新 Todo。

成功响应：

```json
{
  "message": "Todo 整体更新成功",
  "data": {
    "id": 2,
    "title": "重构 Todo API",
    "description": "整体替换 Todo 内容",
    "priority": 5,
    "completed": true
  }
}
```

## 7. 局部修改 Todo

```text
PATCH /todos/{todo_id}
```

请求体示例：

```json
{
  "completed": true
}
```

说明：

- `PATCH` 只修改请求体里传入的字段。
- 代码中使用 `model_dump(exclude_unset=True)` 避免没传的字段被覆盖成 `None`。

成功响应：

```json
{
  "message": "Todo 局部更新成功",
  "data": {
    "id": 3,
    "title": "整理 Todo API 文档",
    "description": "补充 README 和接口表格",
    "priority": 5,
    "completed": true
  }
}
```

## 8. 删除 Todo

```text
DELETE /todos/{todo_id}
```

成功状态码：

```text
204 No Content
```

说明：

- `204` 表示请求成功，但没有响应体。
- 删除成功后不返回 JSON。

错误响应：

```json
{
  "detail": "Todo 不存在"
}
```

## 9. 常见状态码

| 状态码 | 含义 | 本项目里的场景 |
| --- | --- | --- |
| `200` | 请求成功 | 查询、更新成功 |
| `201` | 创建成功 | 新增 Todo |
| `204` | 成功但无响应体 | 删除 Todo |
| `404` | 资源不存在 | 查询、更新、删除不存在的 Todo |
| `422` | 请求参数校验失败 | `todo_id <= 0`、`priority` 超出范围、缺少必填字段 |
