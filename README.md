## Setup
1. Install Docker and Docker Compose
2. Open terminal and run docker compose up --build or (docker-compose up --build)

## Current Design
<img src="https://i.postimg.cc/kMRZPPwT/Monolith-Design-drawio.png" alt="diagram" />

## How can we improve further with minor changes?
Our Django server holds the logic for everything including a ML model which checks for toxicity in a text and this can easily become a bottleneck in our system as the number of requests increases.
- We can solve this issue by increasing the resoruces of our server vertically but there's always a max resource limit.
- As our server is stateless we can solve it by scaling it horizontally but other features like which are rarely getting any requests will scale as well.


## A Slightly Improved Design
<img src="https://i.postimg.cc/yxGNKFsr/Slightly-Improved-Design.png" alt="improved-diagram">

- Here we've scaled it horizontally but our main server is running on very light weight machines and we've moved our Detoxify ML model to better machines.
- Now we can easily service more requests but there is another bottleneck the requests are synchronous as its bound to the time taken by a Detoxify Model to respond.
- We can fix it using asynchronous approach by introducing a message broker like RabbitMQ and the requests will resolve extremely fast.