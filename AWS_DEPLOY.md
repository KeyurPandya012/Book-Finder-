# AWS Deployment Guide: BookFinder

This guide explains how to host your BookFinder app on AWS using **AWS App Runner**. This is the easiest way to get a public URL for a Dockerized app.

## Step 1: Push your code to GitHub
AWS App Runner needs to "see" your code on GitHub to build the container.
1. Create a new repository on [GitHub](https://github.com).
2. Push your project folder to that repository:
   ```bash
   git init
   git add .
   git commit -m "initial commit"
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

## Step 2: Set up AWS App Runner
1. Log in to your [AWS Management Console](https://aws.amazon.com/console/).
2. In the search bar, type **"App Runner"** and click on the service.
3. Click **"Create service"**.
4. **Source**: Select "Source code repository".
5. **Connect to GitHub**: Click "Add new" to link your GitHub account. Select your `BookFinder` repository and the `main` branch.
6. **Deployment settings**: Select "Automatic" (so it redeploys whenever you push code).

## Step 3: Configure Build & Runtime
1. **Configuration file**: Select "Configure all settings here".
2. **Runtime**: Select `Python 3`.
3. **Build Command**: `pip install -r requirements.txt`
4. **Start Command**: `python -m uvicorn app.main:app --host 0.0.0.0 --port 8000`
5. **Port**: Enter `8000`.

*Alternatively, if you want to use the Dockerfile directly:*
1. **Source**: Select "Repository type: Image repository".
2. You would first need to push your image to **Amazon ECR** (Elastic Container Registry), but the GitHub method above is much simpler for beginners.

## Step 4: Configure Service (Compute)
1. **Service name**: `book-finder-api`
2. **CPU & Memory**: 
   - Select **1 vCPU** and **2 GB RAM**. 
   - *Note: We need 2 GB because the NLP models need a bit of breathing room.*
3. **Environment variables**: (Optional) Add any if needed, but not required for this basic setup.

## Step 5: Review and Create
1. Click **"Next"**, review your settings, and click **"Create & Deploy"**.
2. AWS will take 3-5 minutes to build your project.
3. Once the status turns **green (Running)**, you will see a **Default domain** (e.g., `https://random-id.aws-region.awsapprunner.com`). 

**That is your Public URL!** 🚀

---

## Alternative: AWS Lightsail (Cheaper)
If you want a fixed low cost ($7/month):
1. Go to **AWS Lightsail**.
2. Select "Containers".
3. Create a new container service.
4. Upload your project and Lightsail will build the `Dockerfile` for you.
5. It is slightly more manual but very cost-effective.
