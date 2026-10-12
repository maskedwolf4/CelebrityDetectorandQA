# Celebrity Detector + Q&A

A Flask web app that accepts an image, detects the largest face, and asks Groq's vision-capable Llama model to identify the person. After identification, you can ask a follow-up question about them.

## How it works

1. Upload an image in the web interface.
2. OpenCV's Haar cascade looks for faces and draws a box around the largest one.
3. The image is sent to Groq for a description and possible celebrity identification.
4. Ask a question, which is sent to Groq with the identified name as context.

Face detection is local; identification and Q&A require an internet connection and a Groq API key. Model responses may be incorrect, especially for poor-quality images or people who are not public figures.

## Requirements

- Python 3.14 or newer (as declared in `pyproject.toml`)
- [uv](https://docs.astral.sh/uv/)
- A Groq API key

## Run locally

Set the API key in your shell or in a `.env` file in the project root:

```dotenv
GROQ_API_KEY=your_groq_api_key
```

Install the locked dependencies and start the app:

```bash
uv sync --locked
uv run python app.py
```

Open [http://localhost:5000](http://localhost:5000). Upload an image, then use the question field beneath the result to ask about the person.

## Docker

Docker packages the app and its dependencies into a portable image, making it easier to run consistently across environments. The image can be used for local runs or as the deployment artifact pushed to Google Artifact Registry and deployed to GKE by CircleCI.

## Configuration

| Variable | Purpose |
| --- | --- |
| `GROQ_API_KEY` | Required for celebrity identification and Q&A requests. |
| `SECRET_KEY` | Optional Flask secret key; the app currently uses a development fallback if unset. |

## Project layout

```text
app.py                           Flask development entry point
app/routes.py                    Upload and question routes
app/utils/image_handler.py       Image decoding and face detection
app/utils/celebrity_detector.py  Groq image identification
app/utils/qa_engine.py           Groq follow-up question handling
templates/index.html             Web interface
static/style.css                 Interface styles
Dockerfile                       Container build
kubernetes-deployment.yaml      Kubernetes Deployment and Service example
```

## Kubernetes

`kubernetes-deployment.yaml` contains a Deployment and LoadBalancer Service example. It expects a Kubernetes Secret named `llmops-secrets` with a `GROQ_API_KEY` key, and the container image reference in the manifest must point to an image available to your cluster.

## GCP and CircleCI

The CircleCI workflow in `.circleci/config.yml` builds the Docker image, pushes it to Google Artifact Registry, then applies the Kubernetes manifest and restarts the `llmops-app` Deployment on Google Kubernetes Engine (GKE).

Configure these CircleCI environment variables for the pipeline:

- `GCLOUD_SERVICE_KEY`: base64-encoded Google Cloud service account key
- `GOOGLE_PROJECT_ID`: Google Cloud project ID
- `GOOGLE_COMPUTE_REGION`: GKE cluster region
- `GKE_CLUSTER`: GKE cluster name

The service account needs permission to push to Artifact Registry and deploy to the target GKE cluster. Create the `llmops-secrets` Kubernetes Secret with `GROQ_API_KEY` before deploying.
