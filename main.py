from fastapi import FastAPI
from typing import List, Union
import numpy as np
from pydantic import BaseModel, Field
from predict import preprocess_data, predict

app = FastAPI()

class PredictionRequest(BaseModel):
    temperature: Union[float, int]
    humidity: Union[float, int]
    pm2_5: Union[float, int] = Field(..., alias="pm2.5")
    no2: Union[float, int]
    so2: Union[float, int]
    co: Union[float, int]
    proximity_to_industrial_areas: Union[float, int]
    population_density: Union[float, int]

    class Config:
        populate_by_name = True


@app.post("/predict")
def predict_endpoint(data: PredictionRequest):
    data_dict = data.model_dump()
    predictions = predict(data_dict)
    return {"prediction": predictions}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)