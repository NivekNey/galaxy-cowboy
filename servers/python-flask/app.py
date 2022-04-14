from flask import Flask, request
import json
import typing
import math

app = Flask(__name__)


class Model:
    def __init__(self) -> None:
        self.map = {}
        counter = 0
        with open("models/model.jsonlines") as f:
            for line in f:
                counter += 1
                entry = json.loads(line)
                self.map[entry["value"]] = entry["weight"]
        print(f"Model loaded with {counter:,} entries")

    def predict(self, values: typing.Sequence[str]) -> float:
        logit = 0.0
        for value in values:
            logit += self.map.get(value, 0.0)
        probability = 1 / (1 + math.exp(-logit))
        return probability


model = Model()


@app.route("/predict", methods=["POST"])
def predict():
    values = request.json["values"]
    probability = model.predict(values)
    payload = {
        "probability": probability,
    }
    return payload
