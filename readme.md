## Environment Variables

Before running the project, make sure to set up the required environment variables. Create a `.env` file in the project root directory and define variables as in .env_example

#### Note!
DATABASE_HOST, REDIS_HOST vars should be set as container names, you can get names from docker-compose.yml.
## Running
To run the project execute below command
<code> $ docker compose up --build </code>
## Check API docs
Web services are available at http://0.0.0.0, port=8001 - bet-maker, port=8002 - line-provider.
Go to http://0.0.0.0:{port}/docs#/ to see docs.
