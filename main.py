import uvicorn

from app import constants

if __name__ == "__main__":
    uvicorn.run("app.api:app", port=constants.PORT, host=constants.HOST, reload=True)
