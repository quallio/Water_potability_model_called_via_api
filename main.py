from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel

import pickle
import pandas as pd
from fastapi.encoders import jsonable_encoder


app = FastAPI()

MODEL_PATH = "rf.pkl"
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

COLUMNS_PATH = "categories_ohe.pickle"
with open(COLUMNS_PATH, "rb") as handle:
    ohe_tr = pickle.load(handle)


class Answer(BaseModel):
    ph: float
    Hardness: float
    Solids: float
    Chloramines: float
    Sulfate: float
    Conductivity: float
    Organic_carbon: float
    Trihalomethanes: float
    Turbidity: float


@app.get("/")
async def root():
    return {"message": "Proyecto para Bootcamp de EDVAI"}


@app.post("/prediccion")
def predict_water_potability(answer: Answer):

    answer_dict = jsonable_encoder(answer)
    
    for key, value in answer_dict.items():
        answer_dict[key] = [value]
    
    single_instance = pd.DataFrame.from_dict(answer_dict)

    # Reformat columns
    single_instance_ohe = pd.get_dummies(single_instance).reindex(columns = ohe_tr).fillna(0)
    print("...........")
    print("Single instance")
    print(single_instance)
    print("...........")
    
    print("...........")
    print("Single instance ohe")
    print(single_instance_ohe)
    print("...........")
    
    prediction = model.predict(single_instance_ohe)

    # Cast numpy.int64 to just a int
    score = int(prediction[0])
    
    response = {"score": score}
    
    return response


# Corre en http://127.0.0.1:8000 o http://0.0.0.0:8000
if __name__ == '__main__':

    # 0.0.0.0 o 127.0.0.1
    uvicorn.run(app, host='127.0.0.1', port=8000)
