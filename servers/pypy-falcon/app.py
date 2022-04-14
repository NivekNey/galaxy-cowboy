import json
import math
import typing

import falcon


class Model:
    def __init__(self) -> None:
        self.map = {}
        with open("models/model.jsonlines") as f:
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


class Health:
    def on_get(self, req, resp):
        resp.content_type = falcon.MEDIA_TEXT
        resp.text = "ok"


class Predict:
    def on_post(self, req, resp):
        values = json.load(req.stream)["values"]
        probability = model.predict(values)
        payload = {
            "probability": probability,
        }
        resp.text = json.dumps(payload)


app = falcon.App()
app.add_route("/", Health())
app.add_route("/predict", Predict())
