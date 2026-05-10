from fastapi import FastAPI

app = FastAPI(
    title="ImagenAI",
    description="AI Image Generation App",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "Welcome to ImagenAI"}