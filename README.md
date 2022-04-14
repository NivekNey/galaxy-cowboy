# Galaxy Cowboy

*Benchmark the serving of ML model in various languages and frameworks.*

**The setup is currently less like stress test and more like PoC. Stress test is on the road map.**

<img src="https://cdn.openai.com/dall-e-2/demos/text2im/astronaut/horse/photo/0.jpg" width="300">

I like this [DALL·E 2](https://openai.com/dall-e-2/) generated image a lot, 🧑‍🚀🐎.

Simple model design like Logistic Regression is what's being used in production environment.
The repo is to provide proof-of-concepts that shows whether a language/framework/model is viable given some SLA like 30ms at p99.

## Benchmark Server

For simplicity and budgeting, I'm using free-tier GCP instance for both server and client.

Example gcp scripts I use:

```bash
gcp_project=kevinyen
instanct_name=free

gcloud compute instances create \
    ${instanct_name} \
    --project=${gcp_project} \
    --zone=us-west1-b \
    --machine-type=e2-micro \
    --network-interface=network-tier=PREMIUM,subnet=default \
    --maintenance-policy=MIGRATE \
    --service-account=796049519015-compute@developer.gserviceaccount.com \
    --scopes=https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/trace.append \
    --create-disk=auto-delete=yes,boot=yes,device-name=${instanct_name},image=projects/debian-cloud/global/images/debian-11-bullseye-v20220406,mode=rw,size=30,type=projects/${gcp_project}/zones/us-west1-b/diskTypes/pd-balanced \
    --no-shielded-secure-boot \
    --shielded-vtpm \
    --shielded-integrity-monitoring \
    --reservation-affinity=any
```

## Example -- Run a benchmark

```bash
bash scripts/build_one.sh "${RUNNER_IP}" python-flask
```

## Benchmark

The unit is millisecond.

| server           | predict-p50 | predict-p99 |
| ---------------- | ----------- | ----------- |
| python-flask     | 2           | 2           |
| python-fastapi   | 2           | 3           |
| python-starlette | 1           | 2           |
| python-uvicorn   | 2           | 3           |
| java-jooby       | 1           | 5           |
| rust-actix       | 1           | 2           |
| pypy-falcon      | 1           | 5           |

## Road Map

* More realistic benchmarking environment -- separate server and client
* Turn the benchmarks into stress tests
* Replace Apache Bench
* Log versions