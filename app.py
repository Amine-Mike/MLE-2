import random
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mlflow
import numpy as np

mlflow.set_tracking_uri(uri="http://mlflow:8080")

MODEL_NAME = "iris_model"
curr_model = mlflow.pyfunc.load_model(f"models:/{MODEL_NAME}/latest")
next_model = curr_model

app = FastAPI()


class Params(BaseModel):
    sep_len: float
    sep_wdt: float
    pet_len: float
    pet_wdt: float

class ModelUpdate(BaseModel):
    version: int


@app.post("/predict")
def predict(params: Params):
    model_to_use = curr_model if random.random() < 0.8 else next_model
    return {
        "ypred": model_to_use.predict(
            np.array(
                [params.sep_len, params.sep_wdt, params.pet_len, params.pet_wdt]
            ).reshape(1, -1)
        )[0].item()
    }


@app.post("/update-model")
def update_model(model_update: ModelUpdate):
    try:
        global next_model
        next_model = mlflow.pyfunc.load_model(f"models:/{MODEL_NAME}/{model_update.version}")
        return {}
    except mlflow.MlflowException as excep:
        raise HTTPException(
            status_code=404, detail="Model version does not exist."
        ) from excep

@app.post("/accept-next-model")
def accept_next_model():
    global curr_model
    curr_model = next_model
    return {}
