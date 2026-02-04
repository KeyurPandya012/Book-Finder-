# Docker Deployment Guide

This project is fully containerized for easy setup and deployment.

## Prerequisites
- [Docker](https://www.docker.com/get-started) installed on your machine.
- [Docker Compose](https://docs.docker.com/compose/install/) (usually included with Docker Desktop).

## Quick Start (Locally)

1. **Build and Run**:
   Open your terminal in the project root and run:
   ```bash
   docker-compose up --build
   ```

2. **Access the App**:
   Once the build is complete, open your browser and go to:
   `http://localhost:8000`

3. **Stop the App**:
   Press `Ctrl+C` or run:
   ```bash
   docker-compose down
   ```

## Production Hosting
To host the recommender on a public URL (e.g., DigitalOcean, AWS, or Render):

1. **Push to GitHub**: Upload your code to a repository.
2. **Deploy Container**: Most cloud providers allow you to "Deploy from Repo."
3. **Configuration**: Point the service to the `Dockerfile` and expose port `8000`.

## Notes
- The SQLite database (`books.db`) is persisted in the container via a volume.
- Ensure your `requirements.txt` is updated if you add new libraries before building.
