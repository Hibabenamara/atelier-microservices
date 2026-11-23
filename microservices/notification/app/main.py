"""Notification microservice - entry point.

Run:  python -m app.main
"""
import os
from contextlib import asynccontextmanager

import py_eureka_client.eureka_client as eureka_client
from fastapi import FastAPI

from app.routers import notification

PORT = int(os.getenv("PORT", "8084"))
EUREKA_SERVER = os.getenv("EUREKA_SERVER", "http://localhost:8761/eureka")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Démarrage : enregistrement dans Eureka
    await eureka_client.init_async(
        eureka_server=EUREKA_SERVER,
        app_name="notification",
        instance_ip="127.0.0.1",
        instance_port=PORT,
        health_check_url=f"http://127.0.0.1:{PORT}/health",
        status_page_url=f"http://127.0.0.1:{PORT}/info",
    )
    yield
    # Arrêt : désinscription d'Eureka
    await eureka_client.stop_async()


app = FastAPI(
    lifespan=lifespan,
    title="Notification Microservice API",
    version="1.0.0",
    description=(
        "Notification microservice (Python / FastAPI, no database). "
        "Only the hello endpoint is implemented; the notification logic is to be developed by students."
    ),
    contact={"name": "Badia Abouhdid"},
    servers=[{"url": f"http://localhost:{PORT}", "description": "Local"}],
    docs_url="/swagger-ui",
    openapi_url="/v3/api-docs",
    redoc_url="/redoc",
)

app.include_router(notification.router)
@app.get("/health", tags=["Actuator"], summary="Health check")
def health():
    return {"status": "UP"}


@app.get("/info", tags=["Actuator"], summary="Service info")
def info():
    return {
        "name": "notification",
        "version": "1.0.0",
        "description": "Notification microservice (Python / FastAPI)",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=PORT, reload=True)