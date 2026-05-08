from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello FastAPI"}


@app.get("/hello")
async def hello():
    return {"message": "你好，FastAPI"}

@app.get("/me")
async def me():
    return {"name":"liangxin", "content":"fastapi"}
