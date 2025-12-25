from fastapi import FastAPI

app = FastAPI(
    title="FlipSensei API",
    description="Backend service for FlipSensei listing analysis",
    version="0.1.0"
)


@app.get("/health")
def health_check():
    return {"status": "OK"}
