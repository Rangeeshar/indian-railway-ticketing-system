from pydantic import BaseModel


class Train(BaseModel):
    train_number: int
    name: str
    total_seats: int


class ReserveTrain(BaseModel):
    train_number: int
    seats: int
