from fastapi import APIRouter
from app.api.flight_routes import router as flight_router
from app.api.list_routes import router as list_router

# Create main router
router = APIRouter()

# Include sub-routers
router.include_router(flight_router, tags=["Flights"])
router.include_router(list_router, tags=["Flight Lists"])
