from typing import Annotated, Optional

from fastapi import FastAPI, HTTPException, Path, Query, status
from pydantic import BaseModel, ConfigDict, Field

app = FastAPI()


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


class ProductRead(BaseModel):
    id: int
    name: str
    category: str
    price: float
    in_stock: bool
    description: Optional[str] = None


class ProductListResponse(BaseModel):
    count: int
    items: list[ProductRead]


class ProductDetailResponse(BaseModel):
    data: ProductRead


class ProductCreateResponse(BaseModel):
    message: str
    data: ProductRead


products = {
    1: {
        "id": 1,
        "name": "机械键盘",
        "category": "键鼠",
        "price": 399.0,
        "in_stock": True,
        "description": "适合写代码和打字练习",
        "internal_note": "供应商 A，毛利率 22%",
    },
    2: {
        "id": 2,
        "name": "无线鼠标",
        "category": "键鼠",
        "price": 159.0,
        "in_stock": True,
        "description": "轻便办公鼠标",
        "internal_note": "供应商 B，促销库存",
    },
    3: {
        "id": 3,
        "name": "27 英寸显示器",
        "category": "显示器",
        "price": 1299.0,
        "in_stock": False,
        "description": "2K 分辨率显示器",
        "internal_note": "暂时缺货，等待补货",
    },
    4: {
        "id": 4,
        "name": "USB-C 集线器",
        "category": "配件",
        "price": 229.0,
        "in_stock": True,
        "description": "扩展 HDMI、USB 和网口",
        "internal_note": "配件类高频购买商品",
    },
}


@app.get("/")
async def root():
    return {"message": "FastAPI Day 5：Response Model、状态码、错误处理"}


@app.get("/products", response_model=ProductListResponse)
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


@app.get(
    "/products/{product_id}",
    response_model=ProductDetailResponse,
    responses={404: {"description": "商品不存在"}},
)
async def get_product(
    product_id: Annotated[
        int,
        Path(gt=0, description="商品 ID，必须大于 0"),
    ],
):
    product = products.get(product_id)

    if product is None:
        raise HTTPException(status_code=404, detail="商品不存在")

    return {"data": product}


@app.post(
    "/products",
    response_model=ProductCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_product(product: ProductCreate):
    product_id = max(products.keys(), default=0) + 1
    new_product = {
        "id": product_id,
        **product.model_dump(),
        "internal_note": "新创建商品，等待运营补充供应商信息",
    }

    products[product_id] = new_product

    return {
        "message": "商品创建成功",
        "data": new_product,
    }
