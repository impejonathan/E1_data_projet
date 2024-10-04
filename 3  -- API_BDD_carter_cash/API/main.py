from fastapi import FastAPI
from routers import search_router , auth_router

app = FastAPI()

app.include_router(search_router.router)
app.include_router(auth_router.router)


@app.get("/")
def read_root():
    return "Server is running."


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
