import json
import math
import typing

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.routing import Route


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


async def predict(request: Request):
    values = (await request.json())["values"]
    probability = model.predict(values)
    payload = {
        "probability": probability,
    }
    return JSONResponse(content=payload)


async def health(_: Request):
    return PlainTextResponse(content="ok")


app = Starlette(
    routes=[
        Route("/", health),
        Route("/predict", predict, methods=["POST"]),
    ],
)
