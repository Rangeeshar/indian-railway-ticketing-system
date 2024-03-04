import uuid
from utils import send_email


class Train:
    def __init__(self, train_number, name, total_seats):
        self.train_number = train_number
        self.name = name
        self.total_seats = total_seats
        self.available_seats = total_seats
        self.waiting_list = []
        self.current_seat = 1

    def display_train_info(self):
        return {"name": self.name, "seats": self.available_seats, "train_number": self.train_number}

    def reserve_seat(self, num_seats, pnr):
        if self.available_seats >= num_seats:
            reserved_seats = [f"Seat {i}" for i in range(self.current_seat, self.current_seat + num_seats)]
            self.available_seats -= num_seats
            self.current_seat += num_seats
            return {"train_name": self.name,
                    "seats": num_seats,
                    "type": "CNF",
                    "pnr": pnr,
                    "seat_details": reserved_seats,
                    "train_number": self.train_number}
        else:
            partial_fill = min(self.available_seats, num_seats)
            remaining_seats = num_seats - partial_fill
            self.available_seats -= partial_fill
            self.current_seat += partial_fill
            self.waiting_list.append({"pnr": pnr, "seats": remaining_seats})
            if partial_fill > 0:
                reserved_seats = [f"Seat {i}" for i in range(self.current_seat, self.current_seat + partial_fill)]
                return {"train_name": self.name,
                        "seats": num_seats,
                        "type": "PF",
                        "pnr": pnr,
                        "details": {
                            "confirmed": {"seats_filled": partial_fill,
                                          "seat_details": reserved_seats},
                            "waiting_list": remaining_seats
                        },
                        "train_number": self.train_number}
            return {
                "train_name": self.name, "seats": num_seats, "type": "WL", "pnr": pnr, "train_number": self.train_number
            }

    def cancel_reservation(self, num_seats, reservation_details):
        if num_seats <= self.total_seats - self.available_seats:
            self.available_seats += num_seats
            self.process_waiting_list(reservation_details)

    def process_waiting_list(self, reservation_details):
        if self.waiting_list:
            reservation = self.waiting_list.pop(0)
            self.available_seats -= reservation.get("seats")
            print(f"Waiting list processed! {reservation_details} seats allocated on {reservation.get('pnr')}.")
            send_email("Moved from waiting list to CNF")


class ReservationSystem:
    def __init__(self):
        self.trains = {}
        self.pnr = str(uuid.uuid4())
        self.reservation = {}

    def add_train(self, train_number, name, total_seats):
        train = Train(train_number, name, total_seats)
        self.trains[train_number] = train

    def fetch_trains(self):
        train_data = []
        for train, train_object in self.trains.items():
            train_data.append(train_object.display_train_info())
        return train_data

    def reserve_seat(self, train_number, num_seats):
        self.reservation[self.pnr] = self.trains[train_number].reserve_seat(num_seats, self.pnr)
        return {"details": self.reservation[self.pnr], "pnr": self.pnr}

    def cancel_reservation(self, pnr):
        dt = self.reservation[pnr]
        self.trains[dt.get("train_number")].cancel_reservation(dt.get("seats"),
                                                               reservation_details=dt.get("seat_details"))
