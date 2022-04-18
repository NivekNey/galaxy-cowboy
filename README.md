# Galaxy Cowboy

*Benchmark the serving of ML model in various languages and frameworks.*

**The setup is currently less like stress test and more like PoC. Stress test is on the road map.**

<img src="https://cdn.openai.com/dall-e-2/demos/text2im/astronaut/horse/photo/0.jpg" width="300">

I like this [DALL·E 2](https://openai.com/dall-e-2/) generated image a lot, 🧑‍🚀🐎.

Simple model design like Logistic Regression is what's being used in production environment.
The repo is to provide proof-of-concepts that shows whether a language/framework/model is viable given some SLA like 30ms at p99.

## Candidate Selection

### Python

Data Science and modeling work are nowadays mostly on Python. If the serving of the designed model can also be served in Python, then the maintenance footprint would be smaller and can have 1 expert team for end-to-end.

### Java

Product servers are usually implemented in Java, therefore the production team may want to support a prediction server that's also implemented in the Java family.

### Rust

The new kid in the town. High expectation for it to be the "ultimate & most efficient" prediction server.

## Benchmark Server

Colima, `$ colima start --cpu 4 --memory 8`.

## Benchmark

```bash
bash scripts/build_all.sh
```


| name             | p50      | p99      | p100      |
| ---------------- | -------- | -------- | --------- |
| java-jooby       | 0.5581ms | 0.8988ms | 24.9898ms |
| pypy-falcon      | 0.5851ms | 1.2591ms | 28.0771ms |
| python-fastapi   | 1.1461ms | 1.4360ms | 4.7119ms  |
| python-flask     | 0.9270ms | 1.7140ms | 45.9280ms |
| python-starlette | 0.5851ms | 0.8290ms | 8.3513ms  |
| python-uvicorn   | 1.1473ms | 1.4849ms | 13.2899ms |
| rust-actix       | 0.6220ms | 0.8759ms | 14.7541ms |

## Road Map

* More realistic benchmarking environment -- separate server and client
* Turn the benchmarks into stress tests
* Log versions