# fx-payment-processor-api
Prototype for a simplified FX Payment Processor

## 🛠️ Tech Stack
- Languaje: Python 3.12
- Framework: Flask

## Setup and Installation

### Clone the public repository
git clone git@github.com:fierroformo/fx-payment-processor-api.git
cd fx-payment-processor-api

### Build docker image
docker build -t fx-payment-processor-api .


### Run docker container
docker run -p 5000:5000 fx-payment-processor-api

### Test the flask app
Open browser and visit [http://localhost:5000](http://localhost:5000)

## Run tests
docker run fx-payment-processor-api pytest

## Endpoints

### Add funds
POST http://localhost:5000/wallets/<user_id>/fund

Request
```
{
    "currency": "USD",
    "amount": 14
}
```

Response HTTP_201_CREATED
```
Success
```

### Convert
POST http://localhost:5000/wallets/<user_id>/convert

Request
```
{
    "from_currency": "USD",
    "to_currency: "MXN",
    "amount": 14
}
```

Response HTTP_200_OK
```
{
  "amount": 0.742,
  "currency": "USD"
}
```

### Withdraw
POST http://localhost:5000/wallets/<user_id>/withdraw

Request
```
{
    "currency": "USD",
    "amount": 14
}
```

Response HTTP_201_CREATED
```
Success
```

### Balances
GET http://localhost:5000/wallets/<user_id>/balances

Response HTTP_200_OK
```
{
  "MXN": 145.67,
  "USD": 423.60
}
```

## Sample using Rest Client
[Visual Studio Extension](https://marketplace.visualstudio.com/items?itemName=humao.rest-client)

