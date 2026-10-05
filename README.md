# CASMI26 Natural Product Panel Benchmark

This project is a small machine learning web app for predicting whether a candidate natural product is a true hit based on a trained scikit-learn model. It combines a FastAPI backend and a lightweight static frontend to provide an easy prediction interface.

## Overview

The app loads a serialized model from `model.pkl` and exposes a REST API endpoint that accepts candidate feature values and responds with:

- `is_truth`: whether the model predicts the candidate is true (`0` or `1`)
- `confidence`: predicted probability for the positive class, when available

The frontend in the `static/` folder provides a form where users can enter candidate metadata and submit a prediction.

## Project Structure

- `main.py` – FastAPI application, model loader, and prediction endpoint
- `static/index.html` – HTML form for entering feature values
- `static/script.js` – frontend logic that sends requests to the API
- `static/style.css` – styling for the page
- `model.pkl` – trained machine learning pipeline
- `Ml_Train.ipynb` – training notebook used to build and evaluate the model

## Model Features

The trained model expects the following numeric input features:

- `rank`
- `ranker_score`
- `pool_row`
- `popularity`
- `pool_source`
- `lib_max`

These are the fields the backend uses to construct a DataFrame before calling the model.

## API

### `POST /predict`

Request body example:

```json
{
  "rank": 5,
  "ranker_score": -1.57,
  "pool_row": -0.92,
  "popularity": 3.13,
  "pool_source": 2,
  "lib_max": 1.0
}
```

Response example:

```json
{
  "is_truth": 1,
  "confidence": 0.87
}
```

## Local Setup

### 1. Create and activate a virtual environment

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

Or, if using the project metadata:

```bash
pip install -e .
```

### 3. Run the app

```bash
python main.py
```

The app runs by default on:

```text
http://0.0.0.0:8001
```

You can override the host and port with environment variables:

```bash
$env:HOST="127.0.0.1"
$env:PORT="8002"
python main.py
```

## Notes

- The app uses a serialized machine learning pipeline stored in `model.pkl`.
- The frontend is served from the `static/` directory.
- If the model cannot be loaded, the app will return a 500 error when predicting.

## License

This project is provided for research and benchmarking purposes.
