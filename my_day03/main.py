from typing import Annotated, Optional

from fastapi import FastAPI, HTTPException, Path, Query

app = FastAPI()

products = {
    1: {
        "id": 1,
        "name": "机械键盘",
        "category": "键鼠",
        "price": 399.0,
        "in_stock": True,
    },
    2: {
        "id": 2,
        "name": "无线鼠标",
        "category": "键鼠",
        "price": 159.0,
        "in_stock": True,
    },
    3: {
        "id": 3,
        "name": "27 英寸显示器",
        "category": "显示器",
        "price": 1299.0,
        "in_stock": False,
    },
    4: {
        "id": 4,
        "name": "USB-C 集线器",
        "category": "配件",
        "price": 229.0,
        "in_stock": True,
    },
}


@app.get("/")
async def root():
    return {"message": "FastAPI Day 3：路径参数、查询参数、类型注解"}


@app.get("/products")
async def list_products(
    q: Annotated[
        Optional[str],
        Query(description="按商品名称关键字搜索"),
    ] = None,
    category: Annotated[
        Optional[str],
        Query(description="按商品分类筛选"),
    ] = None,
    min_price: Annotated[
        float,
        Query(ge=0, description="最低价格，必须大于或等于 0"),
    ] = 0,
    max_price: Annotated[
        float,
        Query(ge=0, description="最高价格，必须大于或等于 0"),
    ] = 999999,
    in_stock: Annotated[
        Optional[bool],
        Query(description="是否只筛选有库存商品"),
    ] = None,
    limit: Annotated[
        int,
        Query(ge=1, le=20, description="最多返回多少条商品"),
    ] = 20,
):
    result = list(products.values())

    if q:
        result = [
            product
            for product in result
            if q.lower() in product["name"].lower()
        ]

    if category:
        result = [
            product
            for product in result
            if product["category"] == category
        ]

    if in_stock is not None:
        result = [
            product
            for product in result
            if product["in_stock"] == in_stock
        ]

    result = [
        product
        for product in result
        if min_price <= product["price"] <= max_price
    ]

    return {
        "count": len(result),
        "items": result[:limit],
    }


@app.get("/products/{product_id}")
async def get_product(
    product_id: Annotated[
        int,
        Path(gt=0, description="商品 ID，必须大于 0"),
    ],
):
    print(type(product_id))
    product = products.get(product_id)

    if product is None:
        raise HTTPException(status_code=404, detail="商品不存在")

    return {"data": product}
