from fastapi import FastAPI, status


app = FastAPI()


@app.get("/health")
def check_health():
    return {status: 200}
