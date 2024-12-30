# FastAPI Image Processing Application

This application is a FastAPI-based service for image processing tasks, including image upload, manipulation, histogram generation, and segmentation.

## Prerequisites

- Python 3.8+
- `uv` (for managing dependencies and environment)
- `uvicorn` (ASGI server for running FastAPI)

## Setup Instructions

### 1. Install `uv`

If you haven't installed `uv` yet, you can do so by following the instructions on the [uv GitHub repository](https://github.com/astral-sh/uv).

### 2. Initialize the Project

If you haven't already initialized your project with `uv`, run the following command in your project directory:

```bash
uv init
```

### 3. Install Dependencies

Install the dependencies from the `requirements.txt` file:

```bash
uv add -r requirements.txt
```

### 4. Create and Activate a Virtual Environment

Create a virtual environment and activate it:

```bash
uv venv
source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
```

### 5. Run the Application

Use `uvicorn` to run the FastAPI application:

```bash
uv run uvicorn app.main:app --reload
```

- `app.main:app` specifies the module and application instance to run.
- `--reload` enables auto-reloading, which is useful during development as it automatically reloads the server when you make changes to your code.

### 6. Access the Application

- Open your web browser and go to `http://127.0.0.1:8000` to see your FastAPI application running.
- Access the automatically generated API documentation at `http://127.0.0.1:8000/docs`.

## Features

- **Image Upload**: Upload images for processing with support for batch uploads.
- **Image Manipulation**: Resize, crop, and convert image formats.
- **Histogram Generation**: Retrieve color histograms for uploaded images.
- **Segmentation**: Retrieve segmentation masks for uploaded images.
