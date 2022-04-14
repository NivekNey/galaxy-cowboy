# galaxy-cowboy
Benchmark the serving of ML model in various languages and frameworks.

Simple model design like Logistic Regression is what's being used in production environment.
The repo is to provide proof-of-concepts that shows whether a language/framework/model is viable given some SLA like 30ms at p99.

The general setup principle is **4-workers server** and **8-concurrent client**.

<img src="https://cdn.openai.com/dall-e-2/demos/text2im/astronaut/horse/photo/0.jpg" width="300">

I like this [DALL·E 2](https://openai.com/dall-e-2/) generated image alot, 🧑‍🚀🐎.

## Benchmark Server

For simplicity and budgeting, I'm usin free-tier GCP instance for both server and client.

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
    --create-disk=auto-delete=yes,boot=yes,device-name=${instanct_name},image=projects/debian-cloud/global/images/debian-10-buster-v20220406,mode=rw,size=30,type=projects/${gcp_project}/zones/us-west1-b/diskTypes/pd-balanced \
    --no-shielded-secure-boot \
    --shielded-vtpm \
    --shielded-integrity-monitoring \
    --reservation-affinity=any

gcloud compute firewall-rules create \
    predict \
    --allow tcp:9001 \
    --source-tags=${instanct_name} \
    --source-ranges=0.0.0.0/0 \
    --description="for predict api"
```

## Example -- Run a benchmark

```bash
bash scripts/build_one.sh 34.127.79.153 python-flask
```

## Benchmark

| server       | p50 | p99 |
| ------------ | --- | --- |
| python-flask | 7   | 9   |
