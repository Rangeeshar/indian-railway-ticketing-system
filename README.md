# indian-railway-ticketing-system
Indian Railway Ticket System Basic

## Run the app using following command

- sudo docker build -t fastapi-app .
- docker run -p 8080:8080 fastapi-app

## Use the following commands to interact with the API.

- add Train:
```commandline
curl --location 'http://127.0.0.1:8080/api/v1/train' \
--header 'Content-Type: application/json' \
--data '{
    "train_number": 10,
    "name": "swathi express",
    "total_seats": 10
}'
```
- Fetch train
```commandline
curl --location 'http://127.0.0.1:8000/api/v1/train'
```
- Reserver Train
```commandline
curl --location 'http://127.0.0.1:8000/api/v1/train/reserve' \
--header 'Content-Type: application/json' \
--data '{
    "train_number": 10,
    "seats": 4
}'
```
Cancel Train
```commandline
curl --location --request PUT 'http://127.0.0.1:8000/api/v1/train/cancel?pnr=0b1889f1-1a1d-4a38-86a9-de438290d107'
```
