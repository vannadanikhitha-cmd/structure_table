from fastapi import FastAPI
from api.table_router import router
app = FastAPI(
    title="PDF Table Extraction API",
    version="1.0.0"
)
app.include_router(router)
# @app.get("/")
# def home():
#     return {
#         "message": "PDF Table Extraction API Running Successfully"
#     }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )