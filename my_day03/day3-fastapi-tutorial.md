# Day 3 FastAPI 学习教程

今天只抓一件事：**让接口学会接收输入**。

这一课主要看三种输入：

1. 路径参数：写在 URL 路径里，比如 `/products/1`
2. 查询参数：写在 `?` 后面，比如 `/products?q=鼠标`
3. 类型注解：让 FastAPI 自动帮你做类型转换和校验

---

## 1. 今天的目标

学完 Day 3，你应该能做到：

- 看懂路径参数和查询参数的区别
- 知道参数什么时候写在函数参数里，什么时候写在 URL 里
- 能写一个带筛选条件的商品列表接口
- 能写一个根据 `id` 查询详情的接口

---

## 2. 先看整体思路

这次的练习接口有两个：

- `GET /products`
- `GET /products/{product_id}`

前者负责“查列表”，后者负责“查详情”。

列表接口会接收这些筛选条件：

- `q`：关键字搜索
- `category`：按分类筛选
- `min_price`：最低价格
- `max_price`：最高价格
- `in_stock`：是否只看有库存商品
- `limit`：最多返回多少条

详情接口只接收一个值：

- `product_id`

---

## 3. 路径参数是什么

路径参数就是 URL 路径里的一部分。

比如：

```text
/products/1
/products/2
```

这里的 `1`、`2` 就是路径参数。

在 FastAPI 里，你只要这样写：

```python
@app.get("/products/{product_id}")
async def get_product(product_id: int):
    ...
```

FastAPI 会自动把 URL 中的 `1` 变成函数参数 `product_id=1`。

这里最重要的是：

- 路径参数通常表示“唯一资源”
- 例如商品 ID、用户 ID、订单 ID

---

## 4. 查询参数是什么

查询参数是 `?` 后面的内容。

例如：

```text
/products?q=鼠标&category=键鼠&in_stock=true
```

这里的 `q`、`category`、`in_stock` 就是查询参数。

它们适合做这些事情：

- 搜索
- 筛选
- 排序
- 分页

它们不属于资源本身，而是“怎么查”的条件。

---

## 5. 为什么要用类型注解

FastAPI 会根据类型注解自动做两件事：

1. 转换类型
2. 校验数据

例如：

```python
limit: int = 20
in_stock: Optional[bool] = None
min_price: float = 0
```

这意味着：

- `limit` 必须是整数
- `in_stock` 可以是 `true` / `false` / 不传
- `min_price` 会被当成数字处理

如果传错类型，FastAPI 会直接帮你拦住。

---

## 6. 代码逐段讲解

### 6.1 商品数据

我们先用一个内存字典模拟数据库：

```python
products = {
    1: {"id": 1, "name": "机械键盘", "category": "键鼠", "price": 399.0, "in_stock": True},
    2: {"id": 2, "name": "无线鼠标", "category": "键鼠", "price": 159.0, "in_stock": True},
}
```

这里的 key 是 `id`，value 是商品对象。

这样做的好处是：

- 查详情快
- 数据结构简单
- 适合学习阶段

### 6.2 列表接口

```python
@app.get("/products")
async def list_products(...):
```

这个接口返回一组商品。

其中最值得看的是参数写法：

```python
q: Optional[str] = None
category: Optional[str] = None
min_price: float = 0
max_price: float = 999999
in_stock: Optional[bool] = None
limit: int = 20
```

含义分别是：

- `Optional[str] = None`：可传可不传
- `float = 0`：默认值是 0
- `int = 20`：默认最多返回 20 条

### 6.3 `Annotated` + `Query`

你会看到我写成了：

```python
q: Annotated[Optional[str], Query(description="按商品名称关键字搜索")]
```

这表示：

- `Optional[str]`：类型是字符串或空
- `Query(...)`：这是查询参数
- `description`：会显示在 `/docs`

这比只写 `q: str = None` 更清楚，因为它把“类型”和“用途”都写明白了。

### 6.4 过滤逻辑

列表接口先把所有商品拿出来：

```python
result = list(products.values())
```

然后逐个条件过滤：

- 如果传了 `q`，就按名称关键字过滤
- 如果传了 `category`，就按分类过滤
- 如果传了 `in_stock`，就按库存状态过滤
- 最后再按价格区间过滤

这段逻辑的核心思想是：

> 先拿全量数据，再按条件缩小范围

学习阶段这样写最直观。

### 6.5 详情接口

```python
@app.get("/products/{product_id}")
async def get_product(product_id: Annotated[int, Path(gt=0, description="商品 ID，必须大于 0")]):
```

这里有两个重点：

- `int`：必须是整数
- `Path(gt=0)`：必须大于 0

然后通过 `products.get(product_id)` 取商品。

如果不存在，就返回：

```python
raise HTTPException(status_code=404, detail="商品不存在")
```

---

## 7. 你可以直接这样测试

### 查全部

```text
GET /products
```

预期：

- 返回所有商品
- `count` 是 4

### 按关键字查

```text
GET /products?q=鼠标
```

预期：

- 只返回名字里包含“鼠标”的商品

### 按分类查

```text
GET /products?category=键鼠
```

预期：

- 返回分类是“键鼠”的商品

### 按库存查

```text
GET /products?in_stock=true
```

预期：

- 只返回有库存的商品

### 查详情

```text
GET /products/1
```

预期：

- 返回 `id=1` 的商品

### 查不存在的商品

```text
GET /products/999
```

预期：

- 404
- `商品不存在`

---

## 8. 常见坑

### 坑 1：把路径参数和查询参数混了

错误理解：

- `product_id` 应该放在 `?product_id=1`

正确理解：

- 详情资源通常放路径里
- 搜索条件才放查询参数里

### 坑 2：以为 `bool` 只能写 `True` / `False`

FastAPI 接收查询参数时，`true`、`false`、`1`、`0` 都可能被解析。

### 坑 3：忘了设默认值

如果你想让参数可选，就要写默认值：

```python
q: Optional[str] = None
```

不然 FastAPI 会把它当成必填项。

### 坑 4：只会写接口，不会读接口

Day 3 最重要的不是“写出代码”，而是能说清楚：

- 这个值从哪里来
- 为什么放这里
- FastAPI 帮你做了什么

---

## 9. 课后练习

你可以继续加这几个小功能：

1. 增加 `sort_by`，支持按价格排序
2. 增加 `page` 和 `page_size`，做分页
3. 增加 `category` 为空时的默认提示
4. 给 `min_price > max_price` 加一个校验

---

## 10. 今天只要记住三句话

1. 路径参数是资源的一部分。
2. 查询参数是筛选条件。
3. 类型注解不只是提示，它会真的影响 FastAPI 的解析和校验。

