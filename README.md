# Galaxy Cowboy

*Benchmark the serving of ML model in various languages and frameworks.*

**The setup is currently less like stress test and more like PoC. Stress test is on the road map.**

<img src="https://cdn.openai.com/dall-e-2/demos/text2im/astronaut/horse/photo/0.jpg" width="300">

I like this [DALL·E 2](https://openai.com/dall-e-2/) generated image a lot, 🧑‍🚀🐎.

Simple model design like Logistic Regression is what's being used in production environment.
The repo is to provide proof-of-concepts that shows whether a language/framework/model is viable given some SLA like 30ms at p99.

## Benchmark Server

Colima, `$ colima start --cpu 4 --memory 8`.

## Benchmark

```bash
bash scripts/build_all.sh
```

With a duplication of 5.

| name             | p50      | p99      | p100      |
| ---------------- | -------- | -------- | --------- |
| java-jooby       | 0.5488ms | 0.9732ms | 11.4129ms |
| java-jooby       | 0.5629ms | 0.8559ms | 5.0180ms  |
| java-jooby       | 0.5541ms | 0.8199ms | 4.6322ms  |
| java-jooby       | 0.5491ms | 0.9060ms | 34.7307ms |
| java-jooby       | 0.5560ms | 0.8252ms | 5.2681ms  |
| pypy-falcon      | 0.6070ms | 1.6620ms | 20.5381ms |
| pypy-falcon      | 0.5879ms | 1.1880ms | 13.8819ms |
| pypy-falcon      | 0.5858ms | 1.1468ms | 21.2333ms |
| pypy-falcon      | 0.5863ms | 1.1389ms | 10.6239ms |
| pypy-falcon      | 0.5891ms | 1.1709ms | 17.2720ms |
| python-fastapi   | 1.1539ms | 1.3852ms | 3.0291ms  |
| python-fastapi   | 1.1561ms | 1.4949ms | 92.7560ms |
| python-fastapi   | 1.1518ms | 1.3890ms | 4.2481ms  |
| python-fastapi   | 1.1730ms | 1.9960ms | 30.4303ms |
| python-fastapi   | 1.1609ms | 1.7161ms | 5.0640ms  |
| python-flask     | 0.9370ms | 1.8361ms | 16.1982ms |
| python-flask     | 0.9329ms | 1.6987ms | 41.5151ms |
| python-flask     | 0.9353ms | 1.7197ms | 31.8708ms |
| python-flask     | 0.9344ms | 1.7049ms | 14.9503ms |
| python-flask     | 0.9542ms | 1.7161ms | 19.5830ms |
| python-starlette | 0.5898ms | 0.7751ms | 3.9260ms  |
| python-starlette | 0.5910ms | 0.8950ms | 14.5760ms |
| python-starlette | 0.5920ms | 0.8142ms | 4.1490ms  |
| python-starlette | 0.5929ms | 0.7770ms | 3.0329ms  |
| python-starlette | 0.5944ms | 0.9627ms | 10.9241ms |
| python-uvicorn   | 1.1730ms | 2.3599ms | 17.3390ms |
| python-uvicorn   | 1.1480ms | 1.6668ms | 10.5641ms |
| python-uvicorn   | 1.1477ms | 1.4689ms | 7.9138ms  |
| python-uvicorn   | 1.1580ms | 1.5929ms | 5.8408ms  |
| python-uvicorn   | 1.1411ms | 1.3719ms | 3.5529ms  |
| rust-actix       | 0.6320ms | 0.8540ms | 2.7022ms  |
| rust-actix       | 0.6332ms | 0.8938ms | 3.7699ms  |
| rust-actix       | 0.6299ms | 0.9522ms | 3.9210ms  |
| rust-actix       | 0.6289ms | 0.8640ms | 3.9349ms  |
| rust-actix       | 0.6320ms | 0.8702ms | 3.4230ms  |

## Road Map

* More realistic benchmarking environment -- separate server and client
* Turn the benchmarks into stress tests
* Log versions