from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="StarUB Hub API", version="0.1.0", openapi_url="/api/v1/openapi.json")

# Restrict origins through environment-specific configuration before deployment.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type", "Idempotency-Key"],
)

@app.get("/health", tags=["operations"])
def health():
    return {"status": "ok", "service": "starub-api"}

@app.get("/api/v1/ready", tags=["operations"])
def ready():
    # Database and identity-provider checks will be added with configured infrastructure.
    return {"status": "degraded", "checks": {"database": "not_configured", "identity": "not_configured"}}
