# FastAPI Image Processing Application

This application is a FastAPI-based service for image processing tasks, including image upload, manipulation, histogram generation, and segmentation.

![system](/documentation/system.png)

## Prerequisites

- Docker
- Docker Compose

## Setup Instructions

### Using Docker

1. **Build the Docker Image**

   To build the Docker image for the FastAPI application, run the following command in the root directory of your project:

   ```bash
   docker-compose build --no-cache
   ```

   This command builds the Docker image without using the cache, ensuring that all changes are applied.

2. **Run the Docker Containers**

   Start the FastAPI application and the PostgreSQL database using Docker Compose:

   ```bash
   docker-compose up
   ```

   This command will start the services defined in your `docker-compose.yml` file.

3. **Access the Application**

   - Access the automatically generated API documentation at `http://127.0.0.1:8000/docs`.

### Features

- **Image Upload**: Upload images for processing with support for batch uploads.
- **Image Manipulation**: Resize, crop, and convert image formats.
- **Histogram Generation**: Retrieve color histograms for uploaded images.
- **Segmentation**: Retrieve segmentation masks for uploaded images.

## Environment Configuration

The application uses a `.env.docker` file to manage environment-specific configurations. Ensure this file is present in the root directory with the following content:
```
# Database configuration
DATABASE_URL=postgresql+asyncpg://fastapi:fastapi@db:5432/fastapi

# Directory paths
TEMP_IMAGE_DIR=temp_images
TEMP_JSON_DIR=temp_jsons
```


## Additional Information

- **Docker**: Ensure Docker and Docker Compose are installed on your system. You can download them from [Docker's official website](https://www.docker.com/).
- **Environment Variables**: The `.env.docker` file is used to configure environment variables for the Docker environment.

## Further Work

### Add Users and Authorization

To ensure our application is secure, we should implement user management and authorization for jobs and processes. This will help control access and ensure that only authorized users can perform certain actions.

### Background Image Processing with Celery and RabbitMQ

Enhance the application by offloading image processing tasks to the background using Celery and RabbitMQ. This setup allows for asynchronous task processing, improving the responsiveness and *scalability* of the application.

To handle security between microservices, consider using a token-based east-west approach to secure Celery workers.

### Enhance User Interactions

- Add progress tracking for each process so users can monitor the status of their tasks.
- Implement email notifications to inform users when processes are complete, sending results as soon as they are available.