# Day 4 FastAPI 学习教程

今天只抓一件事：**让接口接收 JSON 请求体**。

Day 3 学的是：

- 路径参数：从 URL 路径里来，比如 `/products/1`
- 查询参数：从 `?` 后面来，比如 `/products?q=鼠标`

Day 4 学的是第三种输入：

- 请求体：从 HTTP body 里的 JSON 来，比如创建商品时传一整个商品对象

---

## 1. 今天的目标

学完 Day 4，你应该能做到：

- 知道 Request Body 和查询参数的区别
- 能用 Pydantic 定义一个请求体模型
- 能写一个创建商品的 `POST /products` 接口
- 能看懂 FastAPI 自动校验请求体的错误提示
- 知道 `model_dump()` 是把 Pydantic 模型转成字典

---

## 2. 先看整体思路

今天继续沿用 Day 3 的商品接口。

Day 3 已经有：

- `GET /products`：查询商品列表
- `GET /products/{product_id}`：查询商品详情

Day 4 新增：

- `POST /products`：创建商品

创建商品时，客户端要传这样的 JSON：

```json
{
  "name": "人体工学椅",
  "category": "办公",
  "price": 899.0,
  "in_stock": true,
  "description": "适合长时间学习和办公"
}
```

这段 JSON 不适合放在 URL 里，因为它是一整个对象，所以应该放进请求体。

---

## 3. Request Body 是什么

Request Body 就是 HTTP 请求里专门放复杂数据的地方。

查询参数适合这样的小条件：

```text
/products?q=鼠标&limit=2
```

请求体适合这样的一整个对象：

```json
{
  "name": "人体工学椅",
  "category": "办公",
  "price": 899.0
}
```

最常见的使用场景：

- 新增数据：`POST`
- 整体更新数据：`PUT`
- 局部更新数据：`PATCH`

---

## 4. Pydantic 模型是什么

Pydantic 模型可以理解成“请求体的数据说明书”。

它告诉 FastAPI：

- 请求体里应该有哪些字段
- 每个字段是什么类型
- 哪些字段必填，哪些字段可选
- 字段长度、数字范围等校验规则

代码里这样定义：

```python
from typing import Annotated, Optional

from pydantic import BaseModel, ConfigDict, Field


class ProductCreate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "人体工学椅",
                "category": "办公",
                "price": 899.0,
                "in_stock": True,
                "description": "适合长时间学习和办公",
            }
        }
    )

    name: Annotated[
        str,
        Field(min_length=1, max_length=50, description="商品名称"),
    ]
    category: Annotated[
        str,
        Field(min_length=1, max_length=30, description="商品分类"),
    ]
    price: Annotated[
        float,
        Field(gt=0, description="商品价格，必须大于 0"),
    ]
    in_stock: Annotated[
        bool,
        Field(description="是否有库存"),
    ] = True
    description: Annotated[
        Optional[str],
        Field(max_length=200, description="商品描述"),
    ] = None
```

---

## 5. 字段怎么判断必填和可选

看有没有默认值。

```python
name: str
price: float
```

没有默认值，所以是必填。

```python
in_stock: bool = True
description: Optional[str] = None
```

有默认值，所以可以不传。

区别是：

- `in_stock` 不传时默认是 `True`
- `description` 不传时默认是 `None`

---

## 6. `Field` 是什么

`Field` 是 Pydantic 用来描述字段规则的工具。

例如：

```python
name: Annotated[
    str,
    Field(min_length=1, max_length=50, description="商品名称"),
]
```

表示：

- `name` 必须是字符串
- 最短 1 个字符
- 最长 50 个字符
- 在 `/docs` 里显示“商品名称”

再比如：

```python
price: Annotated[
    float,
    Field(gt=0, description="商品价格，必须大于 0"),
]
```

表示：

- `price` 必须是数字
- 必须大于 0

---

## 7. 创建商品接口

接口代码：

```python
@app.post("/products", status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate):
    product_id = max(products.keys(), default=0) + 1
    new_product = {
        "id": product_id,
        **product.model_dump(),
    }

    products[product_id] = new_product

    return {
        "message": "商品创建成功",
        "data": new_product,
    }
```

这里最关键的是这一行：

```python
async def create_product(product: ProductCreate):
```

`product` 的类型是 `ProductCreate`，FastAPI 看到它是 Pydantic 模型，就会自动从请求体读取 JSON。

---

## 8. `model_dump()` 是什么

`product` 不是普通字典，而是一个 Pydantic 模型对象。

所以不能直接把它当字典用。

Pydantic v2 里推荐使用：

```python
product.model_dump()
```

它会把模型转成字典：

```python
{
    "name": "人体工学椅",
    "category": "办公",
    "price": 899.0,
    "in_stock": True,
    "description": "适合长时间学习和办公",
}
```

然后我们再加上系统生成的 `id`：

```python
new_product = {
    "id": product_id,
    **product.model_dump(),
}
```

---

## 9. `**` 是什么

这里的 `**product.model_dump()` 是字典解包。

可以理解成把一个字典里的键值对展开到另一个字典里。

```python
product_data = {
    "name": "人体工学椅",
    "price": 899.0,
}

new_product = {
    "id": 5,
    **product_data,
}
```

结果是：

```python
{
    "id": 5,
    "name": "人体工学椅",
    "price": 899.0,
}
```

---

## 10. 为什么创建成功用 201

Day 2 里学过状态码。

创建资源成功时，比起默认的 `200 OK`，更准确的是：

```text
201 Created
```

所以代码里写：

```python
@app.post("/products", status_code=status.HTTP_201_CREATED)
```

它表示这个接口成功时默认返回 201。

---

## 11. 你可以这样测试

启动：

```bash
python3 -m uvicorn my_day04.main:app --reload --port 8004
```

然后打开：

```text
http://127.0.0.1:8004/docs
```

找到：

```text
POST /products
```

点开后点击 `Try it out`，填入：

```json
{
  "name": "人体工学椅",
  "category": "办公",
  "price": 899.0,
  "in_stock": true,
  "description": "适合长时间学习和办公"
}
```

预期返回：

```json
{
  "message": "商品创建成功",
  "data": {
    "id": 5,
    "name": "人体工学椅",
    "category": "办公",
    "price": 899.0,
    "in_stock": true,
    "description": "适合长时间学习和办公"
  }
}
```

---

## 12. 故意传错看看

### 少传必填字段

请求体：

```json
{
  "name": "人体工学椅",
  "price": 899.0
}
```

少了 `category`，FastAPI 会返回 422。

### 价格小于等于 0

请求体：

```json
{
  "name": "人体工学椅",
  "category": "办公",
  "price": 0
}
```

因为 `price` 写了 `Field(gt=0)`，所以 FastAPI 会返回 422。

### 名称太长

如果 `name` 超过 50 个字符，也会返回 422。

---

## 13. Day 3 和 Day 4 的区别

| 类型 | 从哪里来 | 适合放什么 | 例子 |
| --- | --- | --- | --- |
| 路径参数 | URL 路径 | 唯一资源 ID | `/products/1` |
| 查询参数 | `?` 后面 | 筛选条件 | `/products?q=鼠标` |
| 请求体 | HTTP body | 复杂对象 | `{"name": "人体工学椅"}` |

---

## 14. 常见坑

### 坑 1：把复杂对象塞进查询参数

不推荐：

```text
/products?name=人体工学椅&category=办公&price=899
```

创建商品更推荐用 JSON 请求体。

### 坑 2：以为 Pydantic 只是写文档

不是。

Pydantic 会真的帮你校验数据。

字段缺失、类型错误、价格不合法，都会在进入业务逻辑前被 FastAPI 拦住。

### 坑 3：忘记 `model_dump()`

如果要把 Pydantic 模型保存到字典里，先转成普通字典：

```python
product.model_dump()
```

### 坑 4：分不清 `Query`、`Path`、`Field`

记忆版：

- `Path`：描述路径参数
- `Query`：描述查询参数
- `Field`：描述 Pydantic 模型字段

---

## 15. 课后练习

你可以继续加这几个小功能：

1. 创建商品时，如果商品名称重复，返回错误。
2. 增加 `tags: list[str] = []` 字段，练习列表类型。
3. 增加 `rating: Optional[float]`，限制评分在 0 到 5 之间。
4. 写一个 `PUT /products/{product_id}`，用请求体更新商品。

---

## 16. 今天只要记住四句话

1. 请求体适合放复杂对象。
2. Pydantic 模型负责描述请求体结构。
3. `Field` 负责给模型字段加校验和文档说明。
4. `product.model_dump()` 可以把模型转成普通字典。
