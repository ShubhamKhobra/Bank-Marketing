from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np 
import pandas as pd 
import pickle
from sklearn.ensemble import RandomForestClassifier

class Person(BaseModel):
    age: int
    marital: str
    default: str
    balance: int
    housing: str
    loan: str
    day_of_week: int
    month: str
    duration: int
    campaign: int
    pdays: int
    previous: int


app = FastAPI()


@app.post("/person/")
async def predict_term_deposite(person: Person):
    
    X = {'age': [person.age],
        'default': [0],
        'balance': [person.balance],
        'housing': [0],
        'loan': [0],
        'day': [person.day_of_week],
        'duration': [person.duration],
        'campaign': [person.campaign],
        'pdays': [person.pdays],
        'previous': [person.previous],
        'divorced': [False],
        'married': [False],
        'single': [False],
        'apr': [False],
        'aug': [False],
        'dec': [False],
        'feb': [False],
        'jan': [False],
        'jul': [False],
        'jun': [False],
        'mar': [False],
        'may': [False],
        'nov': [False],
        'oct': [False],
        'sep': [False]}
    
    if person.default == 'yes':
        X.update({'default': [1]})

    if person.housing == 'yes':
        X.update({'housing': [1]})

    if person.loan == 'yes':
        X.update({'loan': [1]})
    

    if person.marital == 'divorced':
        X.update({'divorced': [True]})
    elif person.marital == 'married':
        X.update({'married': [True]})
    else:
        X.update({'single': [True]})


    def month(dict, key):
        if key in dict:
            dict.update({key: [True]})

    month(X, person.month)

    df_test = pd.DataFrame.from_dict(X)
    lr_model = pickle.load(open('lr_model.sav', 'rb'))
    prediction = lr_model.predict(df_test)
    
    return str(prediction)