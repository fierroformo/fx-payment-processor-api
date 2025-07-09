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
