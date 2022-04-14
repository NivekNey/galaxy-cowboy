"""Create model in JSON format and an example payload"""
import argparse
import json
import os.path
import random

SEED = 5566

parser = argparse.ArgumentParser()
parser.add_argument("--size", type=int, default=2**20)
parser.add_argument("--matches", type=int, default=10)

if __name__ == "__main__":
    args = parser.parse_args()

    if args.size < args.matches:
        raise ValueError(f"argument `size` should be greater or equal to `matches`")

    # write json model
    model_path = "models/model.jsonlines"
    if not os.path.exists(model_path):
        rnd = random.Random(SEED)
        with open(model_path, "w") as f:
            for i in range(args.size):
                line = {
                    "value": f"feature_{i}",
                    "weight": rnd.uniform(-1.0, 1.0),
                }
                json.dump(line, f)
                f.write("\n")
    else:
        print(f"{model_path} already exists, skip creation")

    # write json request payload
    request_path = "models/req.json"
    if not os.path.exists(request_path):
        rnd = random.Random(SEED)
        with open(request_path, "w") as f:
            population = list(range(args.size))
            rnd.shuffle(population)
            payload = {"values": [f"feature_{i}" for i in population[: args.matches]]}
            json.dump(payload, f)
    else:
        print(f"{request_path} already exists, skip creation")
