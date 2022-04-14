import json
import math
import typing


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


async def read_body(receive):
    """
    Read and return the entire body from an incoming ASGI message.
    """
    body = b""
    more_body = True

    while more_body:
        message = await receive()
        body += message.get("body", b"")
        more_body = message.get("more_body", False)

    return body


async def app(scope, receive, send):
    assert scope["type"] == "http"

    method = scope["method"]
    path = scope["path"]

    if (method, path) == ("GET", "/"):
        await send(
            {
                "type": "http.response.start",
                "status": 200,
                "headers": [
                    [b"content-type", b"text/plain"],
                ],
            }
        )
        await send(
            {
                "type": "http.response.body",
                "body": b"ok",
            }
        )
    elif (method, path) == ("POST", "/predict"):
        body = await read_body(receive)
        values = json.loads(body)["values"]
        probability = model.predict(values)
        payload = {
            "probability": probability,
        }
        await send(
            {
                "type": "http.response.start",
                "status": 200,
                "headers": [
                    [b"content-type", b"application/json"],
                ],
            }
        )
        await send(
            {
                "type": "http.response.body",
                "body": json.dumps(payload).encode(),
            }
        )
    else:
        await send(
            {
                "type": "http.response.start",
                "status": 404,
                "headers": [
                    [b"content-type", b"text/plain"],
                ],
            }
        )
        await send(
            {
                "type": "http.response.body",
                "body": f"unknown path {method =} {path =}".encode(),
            }
        )
