#  Project Logbase: Development Prompt History
### DS-614 Big Data Engineering | Group Team_VK

This document tracks the evolution of the **BookFinder** project through the core prompts and objectives provided during its development. These prompts capture the logic and engineering requirements that shaped the final system.

---

##  Phase 1: Foundation & Data Preparation

### **Prompt 1: Project Initialization**
> *"I want to develop a complete and runnable 'BookFinder' project. Use the provided 'BookFinder.pdf' to understand the requirements. We need a robust data pipeline to extract, clean, and store book information from `RC_BOOK_ISBN.csv` into a SQLite database using FastAPI for the backend."*

### **Prompt 2: Data Sanitation**
> *"The raw CSV has duplicates and formatting issues. Create a cleaning script that deduplicates the ISBNs and prepares the data for high-concurrency ingestion. Ensure the database stores ISBN, Title, and Author safely."*

---

##  Phase 2: High-Concurrency Ingestion

### **Prompt 3: Aggressive Deep Fetching**
> *"Populate the application with over 32,000 books. Each book MUST have a valid description. Implement multi-threaded processing with aggressive API calls to Google Books and OpenLibrary. If the ISBN fails, search by Title and Author to find the data."*

### **Prompt 4: Performance Scaling**
> *"Increase the speed! Use 60 parallel threads for the ingestion. Implement a 'heartbeat' logging system so I can see the progress every 20 records. We need to reach the 32,400 book goal quickly and efficiently."*

---

##  Phase 3: Intelligence & Serving (Legacy Feature)

### **Prompt 5: Recommendation Engine (Implemented & Later Removed)**
> *"I want a recommendation system based on mood. Use scikit-learn to implement TF-IDF and Cosine Similarity so users can find books by describing how they feel. Mix the Title and Description for the best results."*

---

##  Phase 4: Project Refinement & Finalization

### **Prompt 6: Pure Data API Shift**
> *"The project is complete, but now I want to remove the UI and the recommendation system. I want a lean, professional FastAPI backend. Keep the core retrieval endpoints and the ingestion pipeline, but strip out the consumer-facing frontend and scikit-learn dependencies."*

### **Prompt 7: API Command Center**
> *"Update the root section of the API to show only useful developer information. I want a professional dashboard that links to the Swagger Docs (/docs) and allows me to trigger a data sync."*

### **Prompt 8: Ultimate Documentation**
> *"Make a fantastic and perfect README.md file. Include a technical glossary of every file in the project and the 'engineering knowledge' associated with each one. Also, provide this Logbase file of all the prompts used."*

---
