import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        app="src.main:app",
        host="localhost",
        port=8000,
        log_level="info",
        reload=True,
    )
