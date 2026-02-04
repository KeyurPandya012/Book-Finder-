# Render Deployment Guide: BookFinder (100% Free)

This guide explains how to host your BookFinder app on **Render.com** for free. Render is very easy to use and doesn't require complex identity verification to start.

## Step 1: Push your code to GitHub
If you haven't already:
1. Create a repository on [GitHub](https://github.com).
2. Push your code:
   ```bash
   git init
   git add .
   git commit -m "deploy to render"
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

## Step 2: Create a Web Service on Render
1. Go to [Render.com](https://render.com) and log in using your **GitHub** account.
2. Click the **"New +"** button and select **"Web Service"**.
3. Select the repository you just pushed.
4. **Configuration**:
   - **Name**: `bookfinder-team-vk`
   - **Region**: Choose the one closest to you (e.g., Singapore or Frankfurt).
   - **Branch**: `main`
   - **Runtime**: Render will automatically detect your `Dockerfile`. (If it asks, select **Docker**).

## Step 3: Choose the Free Plan
1. Scroll down to the **"Instance Type"** section.
2. Select the **"Free"** plan ($0/month).

## Step 4: Environment & Build
1. Click **"Create Web Service"**.
2. Render will start building your Docker image. This usually takes 3-5 minutes.
3. Once the build is finished, you will see a link at the top (e.g., `https://bookfinder-team-vk.onrender.com`).

**That's it! Your app is now live.** 🚀

---

## Important Info about Render Free Tier:
- **Auto-Sleep**: If no one visits the site for 15 minutes, the app "goes to sleep." The next person to visit will wait about 30 seconds for it to wake up.
- **SQLite Database**: In the free tier, the `books.db` file will reset every time the app restarts. For a student project, this is usually fine as long as the data is pushed with the code.
- **Memory**: The free tier provides 512MB RAM. I have optimized the code to fit within this limit!
