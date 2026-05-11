# Day 5 FastAPI 学习教程

今天只抓一件事：**让接口返回更规范、更可控的数据**。

Day 3 学的是接口怎么从 URL 接收输入：

- 路径参数：`/products/1`
- 查询参数：`/products?q=鼠标`

Day 4 学的是接口怎么从 JSON 请求体接收输入：

- 请求体：`{"name": "人体工学椅", "price": 899}`

Day 5 学的是接口怎么规范输出：

- Response Model：规定接口返回什么字段
- 状态码：说明这次请求的结果
- 错误处理：资源不存在时返回清楚的错误

---

## 1. 今天的目标

学完 Day 5，你应该能做到：

- 知道 `response_model` 是用来约束响应结构的
- 能定义商品返回模型 `ProductRead`
- 能写商品详情接口并处理 `404`
- 知道 `201`、`404`、`422` 分别代表什么
- 知道为什么请求模型和响应模型通常要分开写

---

## 2. 先看整体思路

今天继续沿用商品 API。

我们会保留这几个接口：

- `GET /products`：查询商品列表
- `GET /products/{product_id}`：查询商品详情
- `POST /products`：创建商品

Day 5 新增的重点不是接口数量，而是给接口加上响应模型：

```python
@app.get("/products", response_model=ProductListResponse)
```

这表示：

> 这个接口最终返回给客户端的数据，必须符合 `ProductListResponse` 的结构。

---

## 3. Response Model 是什么

Request Body 管的是“客户端传进来的数据”。

Response Model 管的是“接口返回出去的数据”。

对比一下：

| 模型 | 控制方向 | 例子 |
| --- | --- | --- |
| `ProductCreate` | 请求体，请求进来 | 创建商品时客户端传 `name`、`price` |
| `ProductRead` | 响应体，响应出去 | 返回商品时带上 `id`、`name`、`price` |

所以 Day 4 的重点是：

```python
async def create_product(product: ProductCreate):
```

Day 5 的重点是：

```python
@app.get("/products/{product_id}", response_model=ProductDetailResponse)
```

---

## 4. 为什么请求模型和响应模型要分开

创建商品时，客户端不应该传 `id`。

因为 `id` 应该由后端生成。

所以请求模型 `ProductCreate` 没有 `id`：

```python
class ProductCreate(BaseModel):
    name: str
    category: str
    price: float
    in_stock: bool = True
    description: Optional[str] = None
```

但返回商品时，客户端需要知道这个商品的 `id`。

所以响应模型 `ProductRead` 有 `id`：

```python
class ProductRead(BaseModel):
    id: int
    name: str
    category: str
    price: float
    in_stock: bool
    description: Optional[str] = None
```

一句话：

> 请求模型描述“别人要给我什么”，响应模型描述“我要返回给别人什么”。

---

## 5. Day 5 的响应模型

这次代码里有三个响应模型。

### 5.1 商品列表响应

```python
class ProductListResponse(BaseModel):
    count: int
    items: list[ProductRead]
```

它表示列表接口返回：

```json
{
  "count": 4,
  "items": [
    {
      "id": 1,
      "name": "机械键盘",
      "category": "键鼠",
      "price": 399.0,
      "in_stock": true,
      "description": "适合写代码和打字练习"
    }
  ]
}
```

### 5.2 商品详情响应

```python
class ProductDetailResponse(BaseModel):
    data: ProductRead
```

它表示详情接口返回：

```json
{
  "data": {
    "id": 1,
    "name": "机械键盘",
    "category": "键鼠",
    "price": 399.0,
    "in_stock": true,
    "description": "适合写代码和打字练习"
  }
}
```

### 5.3 创建商品响应

```python
class ProductCreateResponse(BaseModel):
    message: str
    data: ProductRead
```

它表示创建成功后返回：

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

## 6. `response_model` 怎么用

列表接口：

```python
@app.get("/products", response_model=ProductListResponse)
async def list_products(...):
    return {
        "count": len(result),
        "items": result[:limit],
    }
```

详情接口：

```python
@app.get(
    "/products/{product_id}",
    response_model=ProductDetailResponse,
    responses={404: {"description": "商品不存在"}},
)
async def get_product(product_id: int):
    ...
```

创建接口：

```python
@app.post(
    "/products",
    response_model=ProductCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_product(product: ProductCreate):
    ...
```

注意：

- `response_model` 控制成功响应的数据结构
- `status_code` 控制成功响应的状态码
- `responses` 可以补充错误响应在 `/docs` 里的说明

---

## 7. Response Model 会过滤字段

Day 5 的代码里，内存数据故意多放了一个字段：

```python
"internal_note": "供应商 A，毛利率 22%"
```

这个字段是内部备注，不应该返回给客户端。

但是 `ProductRead` 里没有 `internal_note`：

```python
class ProductRead(BaseModel):
    id: int
    name: str
    category: str
    price: float
    in_stock: bool
    description: Optional[str] = None
```

所以接口返回时，FastAPI 会按照 `response_model` 输出，自动过滤掉 `internal_note`。

这就是响应模型很重要的原因：

> 它不只是生成文档，还能保护接口输出，避免把内部字段暴露出去。

---

## 8. 商品不存在怎么处理

详情接口里先按 `product_id` 查商品：

```python
product = products.get(product_id)
```

如果查不到，就抛出异常：

```python
if product is None:
    raise HTTPException(status_code=404, detail="商品不存在")
```

这里的 `404` 表示：

> 请求的资源不存在。

例如：

```text
GET /products/999
```

返回：

```json
{
  "detail": "商品不存在"
}
```

---

## 9. 状态码怎么理解

今天重点看三个状态码。

| 状态码 | 含义 | Day 5 例子 |
| --- | --- | --- |
| `200 OK` | 请求成功 | 查询列表、查询详情成功 |
| `201 Created` | 创建成功 | `POST /products` 创建商品成功 |
| `404 Not Found` | 资源不存在 | `GET /products/999` |
| `422 Unprocessable Entity` | 请求数据没通过校验 | `price=0` 或 `product_id=0` |

容易混的是 `404` 和 `422`：

- `/products/999` 是 `404`，因为参数格式正确，只是商品不存在
- `/products/0` 是 `422`，因为 `Path(gt=0)` 要求 `product_id` 必须大于 0

---

## 10. 可以这样测试

启动服务：

```bash
python3 -m uvicorn my_day05.main:app --reload --port 8005
```

打开接口文档：

```text
http://127.0.0.1:8005/docs
```

### 10.1 查询详情成功

```text
GET /products/1
```

预期：

- 状态码是 `200`
- 返回 `data`
- 返回内容里没有 `internal_note`

### 10.2 查询不存在商品

```text
GET /products/999
```

预期：

- 状态码是 `404`
- 返回 `{"detail": "商品不存在"}`

### 10.3 创建商品成功

```text
POST /products
```

请求体：

```json
{
  "name": "人体工学椅",
  "category": "办公",
  "price": 899.0,
  "in_stock": true,
  "description": "适合长时间学习和办公"
}
```

预期：

- 状态码是 `201`
- 返回 `message`
- 返回新商品的 `data`
- 返回内容里没有 `internal_note`

### 10.4 创建商品失败

请求体：

```json
{
  "name": "人体工学椅",
  "category": "办公",
  "price": 0
}
```

预期：

- 状态码是 `422`
- 因为 `price` 必须大于 0

---

## 11. Day 5 常见坑

### 坑 1：以为 `response_model` 只是文档

不是。

`response_model` 会真的参与响应处理，包括字段过滤和响应校验。

### 坑 2：请求模型和响应模型混用

`ProductCreate` 给请求体用。

`ProductRead` 给响应体用。

不要为了省事把一个模型硬用到底，否则很容易出现：

- 创建时要求客户端传 `id`
- 返回时缺少客户端需要的 `id`
- 内部字段意外暴露

### 坑 3：所有错误都返回 404

不是所有错误都是 404。

- 找不到资源：`404`
- 参数或请求体不合法：`422`
- 创建成功：`201`
- 查询成功：`200`

### 坑 4：返回结构不稳定

今天开始，接口返回结构尽量稳定。

例如详情接口固定返回：

```json
{
  "data": {}
}
```

列表接口固定返回：

```json
{
  "count": 0,
  "items": []
}
```

稳定结构会让前端或调用方更容易使用你的接口。

---

## 12. 课后练习

你可以继续加这几个小功能：

1. 给错误响应也定义统一结构，例如 `{"message": "商品不存在"}`。
2. 给 `POST /products` 增加商品名称重复检查，重复时返回 `400`。
3. 增加 `PUT /products/{product_id}`，练习请求体和响应模型一起使用。
4. 给 `/products` 增加 `response_model_exclude_none=True`，观察 `description=None` 时是否返回。

---

## 13. 今天只要记住四句话

1. `response_model` 管接口返回什么。
2. 请求模型和响应模型通常要分开写。
3. `HTTPException(status_code=404)` 用来表达资源不存在。
4. 状态码是接口结果的简短说明，数据结构是接口结果的具体内容。
