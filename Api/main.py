from fastapi import FastAPI, UploadFile,File
from fastapi import BaseAPI

app = FastAPI()

# greeting the user

@app.get("/home")
def greet_user():
    return {"Message":"Hi Potential Seller, which car would you like to sell today"}

@app.post("/predict")
def predict_price():
    return 