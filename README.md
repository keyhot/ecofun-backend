### EcoFun Backend ♻️
## FastAPI + PostgreSQL Backend
This project is a backend application built with FastAPI, designed to provide a robust and scalable RESTful API with PostgreSQL as the database for the EcoFun project.
It was developed within 24 hours during the HackWarsaw event held by AngelHack on 15-16th of June, 2024.

## App Demo Video
https://www.youtube.com/shorts/P8XtMF8sVk8


## Requirements
Python ^3.12

Poetry ^1.7.1

## Installation
```
git clone https://github.com/keyhot/ecofun-backend.git
cd ecofun-backend
```
## Install Poetry
Follow the installation instructions from the [Poetry documentation](https://python-poetry.org/docs/).


## Install Dependencies
```
poetry shell
poetry install
```

## Configure Environment Variables
Create a .env file in the project root with the following content:
```
IS_PROD=False
PORT=8080
HOST=127.0.0.1
API_KEY=your_api_key
DATABASE_URL=postgresql://your-database-URI
```

## Running the Application
```
python -m main
```
