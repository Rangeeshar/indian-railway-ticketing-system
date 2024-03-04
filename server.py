from fastapi import FastAPI, HTTPException, APIRouter
from service import ReservationSystem
from request_models import *

app = FastAPI()

prefix_router = APIRouter(prefix="/api/v1")
reservation_system = ReservationSystem()


@prefix_router.post("/train")
async def add_train(train: Train):
    reservation_system.add_train(train.train_number, train.name, train.total_seats)
    return {"message": f"Train {train.train_number} - {train.name} added successfully."}


@prefix_router.get("/train")
async def display_trains():
    return {"data": reservation_system.fetch_trains()}


@prefix_router.post("/train/reserve")
async def reserve_seat(reserve_train: ReserveTrain):
    result = reservation_system.reserve_seat(train_number=reserve_train.train_number, num_seats=reserve_train.seats)
    return {
        "data": result
    }


@prefix_router.put("/train/cancel")
async def cancel_reservation(pnr: str):
    result = reservation_system.cancel_reservation(pnr)
    return {
        "data": result
    }
app.include_router(prefix_router)
