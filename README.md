#  BookFinder: Ultimate Technical Dossier
### DS-614 Big Data Engineering Project | Team_VK

**BookFinder** is a state-of-the-art Big Data ecosystem designed to ingest, clean, enrich, and serve a massive dataset of 32,400+ books. This project represents a complete data engineering lifecycle—from raw, noisy CSV files to a high-concurrency, professional-grade REST API.

---

##  Comprehensive Project Knowledge & File Glossary

Below is the exhaustive map of every file in the project, including its technical purpose and the engineering "knowledge" it contains.

###  1. Root Directory (Core Infrastructure)

| File Name | Functional Description & Technical Knowledge |
| :--- | :--- |
| **[BookFinder.pdf]** | **Requirements Source**: The foundation of the project. It defines the technical scope, mandatory features (like Google Books integration), and academic goals for the DS-614 course. |
| **[RC_BOOK_ISBN.csv]** | **Raw Data Source**: 6.1MB of raw, unformatted book records. This is the "noisy" starting point that requires cleaning and deduplication. |
| **[books.db]** | **Production Database**: A SQLite 3 database file. It contains the final, enriched table with indexed ISBNs, titles, authors, and fetched descriptions. This is the "Source of Truth" for the API. |
| **[cleaned_books.csv]** | **Sanitized Dataset**: The output of `clean_csv.py`. It is a 5.4MB CSV with all duplicate ISBNs removed and invalid characters repaired, serving as the input for the ingestion engine. |
| **[run.py]** | **API Launcher**: A Python entry point that programmatically starts the `uvicorn` server at `localhost:8000`. It ensures the `app/` package is correctly loaded into the system path. |
| **[run.bat]** | **Automation Shortcut**: A Windows Batch file that allows a user to start the entire API server with a single double-click, ensuring all environment variables are correctly set. |
| **[requirements.txt]** | **Dependency Manifest**: Defines the exact Python environment needed. Key libraries include `fastapi` for the API, `pandas` for data logic, and `requests` for external API communication. |

---

###  2. The Data Pipeline (`scripts/`)

| File Name | Engineering Intelligence & Usage |
| :--- | :--- |
| **[clean_csv.py]** | **Knowledge**: Uses Pandas vectorization to handle large-scale data cleaning. It deletes 3,000+ duplicate rows and repairs corrupted ISBN strings to prevent database primary-key violations. |
| **[ingest.py]** | **The "Master Engine"**: The most complex file. It uses `ThreadPoolExecutor` with **60 parallel threads** to multi-task. It features "Deep Search" logic: if ISBN fails, it searches Google by Title, then OpenLibrary by Work ID. It handles API rate-limits and retries automatically. |
| **[dump_db.py]** | **Knowledge**: A terminal-based data viewer. It uses SQL queries to fetch and format the top records into a table, allowing for instant verification of the data ingestion progress. |
| **[seed_test_data.py]** | **Knowledge**: A "seeder" script. It injects a small set of "Golden Records" into the database for testing the API logic before the full 32,000-book ingestion begins. |

---

###  3. The Backend API Service (`app/`)

| File Name | Architectural Role & Implementation Details |
| :--- | :--- |
| **[main.py]** | **API Orchestrator**: Manages the life-cycle of the FastAPI server. It defines the `/books` and `/sync` endpoints and handles global exception catching. |
| **[crud.py]** | **Data Access Layer**: Contains the "Create, Read, Update, Delete" logic. Optimized to use paginated SQL (`LIMIT` and `OFFSET`) so the API remains fast even as the database grows to 30,000+ rows. |
| **[database.py]** | **Engine Config**: Configures the SQLite engine. Critically, it enables **WAL Mode (Write-Ahead Logging)**, which allows the ingestion script to write data while the API is simultaneously reading it. |
| **[schemas.py]** | **Data Contracts**: Uses Pydantic to define the "Shape" of a book. This ensures consistency between the database columns and the JSON response seen by users. |

---

##  Technical Workflow (How it all connects)

1.  **Cleaning**: `scripts/clean_csv.py` reads `RC_BOOK_ISBN.csv` and creates `cleaned_books.csv`.
2.  **Ingestion**: `scripts/ingest.py` reads the cleaned CSV and launches 60 threads to fetch descriptions from Google Books/OpenLibrary, saving them to `books.db`.
3.  **Serving**: `run.py` starts the FastAPI server (`app/main.py`).
4.  **Retrieval**: The API (`crud.py`) fetches books from `books.db` and returns them as JSON validated by `schemas.py`.

---

##  How to Execute the Project

### 1. Set Up Environment
```bash
pip install -r requirements.txt
```

### 2. Process Data
```bash
python scripts/clean_csv.py
python scripts/ingest.py --threads 60
```

---

##  Phase 2: AI Discovery & Intelligence (The Recommender)

The second phase transformed the project from a static API into a **Bibliotherapy Dashboard**, featuring a premium glassmorphism UI.

###  1. Discovery Ecosystem
| Feature | Technical Implementation |
| :--- | :--- |
| **Mood Search** | Uses **TF-IDF (Term Frequency-Inverse Document Frequency)** to analyze natural language queries. It matches the "emotional context" of your mood to book descriptions. |
| **Author Discovery** | A specialized filter that performs lightning-fast substring matching across 29,000+ records to find every work by a specific creator. |
| **ISBN Finder** | A direct-lookup tool for precise retrieval. It acts as the entry point for deep-diving into individual book analytics. |
| **Similarity Explorer** | Found within the "View Details" modal. It calculates **Cosine Similarity** on-the-fly to suggest "Kindred Books" based on content overlap. |

###  2. UI/UX Architecture (`app/static/`)
- **[index.html]**: A single-page application (SPA) built with vanilla JS and CSS.
- **Glassmorphism**: Uses `backdrop-filter: blur` and radial gradients for a modern, "premium" feel.
- **Staggered Animations**: CSS `@keyframes` and dynamic delay logic ensure books "float" into view.

---

##  Data Engineering Statistics (The Results)

The pipeline successfully processed and enriched the 36k record dataset with the following results:

| Stage | Metric | Count |
| :--- | :--- | :--- |
| **Raw Ingestion** | Total records in `RC_BOOK_ISBN.csv` | **36,360** |
| **Data Cleaning** | Valid unique books after deduplication | **31,477** |
| **AI Enrichment** | Books with descriptions fetched & verified | **29,256** |
| **API Readiness** | Total enriched records in `books.db` | **29,256** |

> [!NOTE]
> 100% of the books serveed via the API now contain enriched metadata and descriptions, compared to 0% in the original raw file.

---

##  Premium Deployment & Infrastructure

###  1. Dockerization
The project is fully containerized for "One-Click" deployment.
- **[Dockerfile]**: A multi-stage build that keeps the image size small.
- **[docker-compose.yml]**: Orchestrates the FastAPI web service and ensures the SQLite database is persisted.
- **Usage**: `docker-compose up --build`

###  2. Cloud Hosting (Render.com - 100% Free)
Detailed instructions for hosting on a public URL via **Render** are provided in **[RENDER_DEPLOY.md]**. 
- **Efficiency**: The recommender uses an optimized "on-the-fly" similarity calculation to run smoothly on Render's free tier.
- **Auto-Sync**: Connects directly to your GitHub for automatic deployments.

---

##  Master Documentation Links
- **[DOCKER.md]**: Local container setup and troubleshooting.
- **[RENDER_DEPLOY.md]**: Step-by-step guide for hosting for free on the cloud.

---
*Created for the DS-614 Big Data Engineering Course | Final Submission.*
