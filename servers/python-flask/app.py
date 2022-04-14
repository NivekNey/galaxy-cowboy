import json
import math
import typing

from flask import Flask, request

app = Flask(__name__)


class Model:
    def __init__(self) -> None:
        self.map = {}
        with open("/app/models/model.jsonlines") as f:
            for line in f:
                entry = json.loads(line)
                self.map[entry["value"]] = entry["weight"]

    def predict(self, values: typing.Sequence[str]) -> float:
        logit = 0.0
        for value in values:
            logit += self.map.get(value, 0.0)
        probability = 1 / (1 + math.exp(-logit))
        return probability


model = Model()


@app.post("/predict")
def predict():
    values = request.json["values"]
    probability = model.predict(values)
    payload = {
        "probability": probability,
    }
    return payload


@app.get("/")
def health():
    return "ok"
