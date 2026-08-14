from fastapi import FastAPI

app = FastAPI(title="CodeVerity API")

@app.get("/")
def read_root():
    return {"message": "CodeVerity API is running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}