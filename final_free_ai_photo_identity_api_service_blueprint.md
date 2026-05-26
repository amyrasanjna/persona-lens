# Final Free AI Photo Identity + Semantic Recognition API Service Blueprint

# Project Goal

Build a completely free, open-source, API-first AI image intelligence service capable of:

- Face recognition
- Unknown person clustering
- Incremental identity learning
- Named and unnamed uploads
- Multi-image uploads
- Semantic image understanding
- Natural language search
- Image caption generation
- Title generation
- Alt text generation
- Deep image descriptions
- Confidence scoring
- JSON API responses
- Minimal frontend only for testing

The system should:

- work with free cloud infrastructure
- use lightweight models
- avoid paid GPU services initially
- scale later if needed
- run mostly using Hugging Face Spaces and free tiers

---

# Real Product Behavior

The system should support all of the following workflows.

---

# Workflow 1: Upload Images Without Name

User uploads:

```text
2 images
No name provided
```

System should:

- detect faces
- generate face embeddings
- compare with existing identities
- check for similar people
- create unknown cluster if no confident match exists

Example:

```json
{
  "cluster_id": "unknown_44",
  "status": "new_unknown_identity"
}
```

---

# Workflow 2: Upload Same Person Later With Name

Later user uploads:

```text
5 images
Name = Rahul
```

System should:

- generate embeddings
- compare with all previous clusters
- find matching unknown cluster
- suggest merge
- attach images to same identity

Example:

```json
{
  "possible_match": "unknown_44",
  "confidence": 0.91,
  "suggestion": "merge_with_existing_identity"
}
```

---

# Workflow 3: Upload Same Person Again Later

User uploads another image.

System should:

- recognize person
- return confidence score
- attach image automatically if confidence is high

Example:

```json
{
  "person": "Rahul",
  "confidence": 0.94
}
```

---

# Workflow 4: Multiple Images Upload

User uploads:

```text
5-6 images at once
Some same people
Some different people
Some named
Some unnamed
```

System should:

- process all images
- cluster identities correctly
- merge same identities
- create unknown clusters
- maintain confidence scores

---

# Workflow 5: Semantic Search

User searches:

```text
Rahul at beach
night city photos
birthday party
woman in red dress
```

System should:

- use semantic embeddings
- retrieve matching images
- combine person + scene understanding

---

# Workflow 6: Image Metadata Generation

When image uploads:

System should generate:

- title
- caption
- alt text
- detailed description
- tags

Example:

```json
{
  "title": "Young man standing near beach during sunset",
  "caption": "Relaxed evening portrait during golden hour.",
  "alt_text": "A young man standing near the shoreline.",
  "description": "The image shows a young man standing near the beach during sunset.",
  "tags": ["beach", "sunset", "vacation"]
}
```

---

# Final Technology Stack

# Backend API

Use:

- FastAPI

Official:

- https://fastapi.tiangolo.com/

Purpose:

- REST APIs
- upload handling
- image processing orchestration
- search APIs
- recognition APIs

---

# Face Recognition Model

Use:

- InsightFace

Official:

- https://github.com/deepinsight/insightface

Purpose:

- face detection
- face embeddings
- similarity matching
- identity recognition

Model Recommendation:

```text
buffalo_l
```

Why:

- lightweight
- highly accurate
- free
- fast inference
- no training needed

---

# Semantic Embedding Model

Use:

- OpenCLIP

Official:

- https://github.com/mlfoundations/open_clip

Purpose:

- semantic image understanding
- semantic search
- image-text similarity
- contextual retrieval

Recommended Model:

```text
ViT-B-32
```

Why:

- lightweight
- fast
- free-tier friendly

---

# Caption + Metadata Model

Use:

- BLIP Base

Official:

- https://github.com/salesforce/BLIP

Purpose:

- image captions
- alt text
- descriptions
- tags

Why:

- lightweight
- suitable for free GPUs
- faster than large vision models

---

# Vector Database

Use:

- Qdrant Cloud Free Tier

Official:

- https://qdrant.tech/cloud/

Purpose:

- vector similarity search
- face embedding storage
- semantic embedding storage

---

# Main Database

Use:

- Supabase PostgreSQL Free Tier

Official:

- https://supabase.com/

Purpose:

- metadata storage
- identity storage
- image records
- API data

---

# Redis Queue

Use:

- Upstash Redis Free Tier

Official:

- https://upstash.com/

Purpose:

- background jobs
- queues
- async processing

---

# API Hosting

Use:

- Render Free Tier

Official:

- https://render.com/

Purpose:

- FastAPI hosting
- REST API deployment

---

# AI Inference Hosting

Use:

- Hugging Face Spaces

Official:

- https://huggingface.co/spaces

Purpose:

- host AI inference APIs
- run lightweight AI models
- free GPU experimentation

---

# Frontend Hosting

Use:

- Vercel

Official:

- https://vercel.com/

Purpose:

- minimal testing UI
- upload testing
- search testing

---

# Final Architecture

```text
Client
   ↓
Minimal Frontend UI (Vercel)
   ↓
FastAPI Backend (Render)
   ↓
Async Queue (Redis)
   ↓
AI Processing Service (HuggingFace Space)
   ├── InsightFace
   ├── OpenCLIP
   └── BLIP
   ↓
Supabase + Qdrant
```

---

# Step-by-Step Development Plan

# STEP 1: Create GitHub Repository

Create repository.

Example:

```text
ai-photo-identity-api
```

---

# STEP 2: Setup Backend

Install:

```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary
```

Create:

```text
backend/
```

Add:

- upload APIs
- recognition APIs
- search APIs

---

# STEP 3: Setup Supabase

Go to:

- https://supabase.com/

Create:

- free project
- PostgreSQL database

Store:

- DATABASE_URL

---

# STEP 4: Setup Qdrant

Go to:

- https://qdrant.tech/cloud/

Create:

- free cluster

Store:

- QDRANT_URL
- QDRANT_API_KEY

---

# STEP 5: Setup Upstash Redis

Go to:

- https://upstash.com/

Create:

- Redis database

Store:

- REDIS_URL

---

# STEP 6: Create Hugging Face Account

Go to:

- https://huggingface.co/

Create:

- account
- new Space

Recommended:

```text
Docker Space
```

---

# STEP 7: Setup AI Models

Inside Hugging Face Space install:

```bash
pip install insightface
pip install open_clip_torch
pip install transformers
pip install torch
```

---

# STEP 8: Load Models

## InsightFace

```python
from insightface.app import FaceAnalysis
```

---

## OpenCLIP

```python
import open_clip
```

---

## BLIP

```python
from transformers import BlipProcessor, BlipForConditionalGeneration
```

---

# STEP 9: Build Face Embedding API

Input:

```text
image
```

Output:

```json
{
  "embedding": [],
  "faces_detected": 1
}
```

---

# STEP 10: Build Similarity Search

Store embeddings in Qdrant.

Search nearest identities.

---

# STEP 11: Build Clustering Logic

Logic:

| Similarity | Action |
|---|---|
| > 0.80 | Auto attach |
| 0.65-0.80 | Suggest merge |
| < 0.65 | Create new cluster |

---

# STEP 12: Build Metadata Generation

Generate:

- title
- caption
- alt text
- description
- tags

Using BLIP.

---

# STEP 13: Build Semantic Search

Use OpenCLIP embeddings.

Query example:

```text
beach sunset
```

Convert text into embedding.

Search nearest semantic vectors.

---

# STEP 14: Build Minimal Frontend

Frontend should support:

- upload image
- view recognition results
- search
- cluster suggestions
- metadata display

Minimal only.

---

# API Endpoints

# Upload Image

```http
POST /upload
```

Input:

```multipart
file=image.jpg
name=Rahul
```

Name optional.

---

# Recognize Person

```http
POST /recognize
```

Response:

```json
{
  "matches": [
    {
      "person": "Rahul",
      "confidence": 0.91
    }
  ]
}
```

---

# Semantic Search

```http
GET /search?q=beach+sunset
```

---

# Image Metadata

```http
GET /image/:id
```

---

# Cluster Suggestions

```http
GET /cluster/suggestions
```

---

# Folder Structure

```text
backend/
  api/
  database/
  workers/
  services/
  vector/
  models/
  utils/

frontend/
  demo/

storage/
  originals/
  faces/
  thumbnails/
```

---

# Database Schema

# persons

```sql
CREATE TABLE persons (
  id UUID PRIMARY KEY,
  name TEXT,
  created_at TIMESTAMP
);
```

---

# images

```sql
CREATE TABLE images (
  id UUID PRIMARY KEY,
  path TEXT,
  title TEXT,
  caption TEXT,
  alt_text TEXT,
  description TEXT,
  metadata JSONB
);
```

---

# face_embeddings

```sql
CREATE TABLE face_embeddings (
  id UUID PRIMARY KEY,
  person_id UUID,
  image_id UUID,
  confidence FLOAT,
  embedding VECTOR(512)
);
```

---

# semantic_embeddings

```sql
CREATE TABLE semantic_embeddings (
  id UUID PRIMARY KEY,
  image_id UUID,
  embedding VECTOR(768)
);
```

---

# Recognition Flow

```text
Upload Image
    ↓
Detect Faces
    ↓
Generate Embeddings
    ↓
Search Similar Identities
    ↓
Auto Attach / Suggest / Create Cluster
    ↓
Generate Metadata
    ↓
Store Results
```

---

# Semantic Search Flow

```text
User Query
    ↓
OpenCLIP Text Embedding
    ↓
Qdrant Similarity Search
    ↓
Matching Images
```

---

# Important Optimization Rules

# Rule 1

Do NOT retrain models initially.

---

# Rule 2

Store embeddings permanently.

Never recompute unnecessarily.

---

# Rule 3

Process uploads asynchronously.

Never block uploads.

---

# Rule 4

Keep models lightweight.

Avoid huge VLMs initially.

---

# Rule 5

Always support human confirmation.

Do not blindly auto-merge identities.

---

# Limitations of Free Hosting

You must expect:

- cold starts
- sleeping servers
- slower inference
- GPU availability issues
- request limits

This is acceptable for MVP and testing.

---

# Recommended Future Upgrades

Later you can upgrade:

| Current | Future |
|---|---|
| BLIP | Florence-2 |
| HuggingFace Spaces | RunPod |
| Free CPU | Dedicated GPU |
| Single worker | Distributed workers |

---

# Final Copilot / Cursor AI Prompt

```text
Create a production-ready AI-powered photo identity and semantic image recognition API service.

Architecture Requirements:

- API-first backend
- minimal frontend for testing only
- scalable modular architecture
- async processing
- Docker-ready
- free-tier friendly
- open-source models only

Backend Stack:

- FastAPI
- PostgreSQL
- SQLAlchemy
- Redis
- Celery
- Qdrant

AI Models:

1. InsightFace (buffalo_l)
   - face detection
   - face embeddings
   - identity matching

2. OpenCLIP ViT-B-32
   - semantic image embeddings
   - text-image similarity
   - semantic search

3. BLIP Base
   - image captions
   - alt text
   - image descriptions
   - tags

Required Features:

- upload images with optional person name
- upload multiple images
- support unnamed identities
- automatic unknown person clustering
- incremental identity learning
- confidence-based recognition
- merge suggestions
- semantic image search
- metadata generation
- vector similarity search
- JSON API responses

Identity Logic:

- if same person uploaded later with name, match previous unknown cluster
- allow same person uploads over time
- support named and unnamed uploads
- support multiple faces per image
- return confidence scores

API Endpoints:

- POST /upload
- POST /recognize
- GET /search
- GET /image/:id
- GET /cluster/suggestions

Folder Structure:

backend/
  api/
  database/
  workers/
  services/
  vector/
  models/
  utils/

frontend/
  demo/

storage/
  originals/
  faces/
  thumbnails/

Requirements:

- clean architecture
- repository pattern
- async background jobs
- vector search integration
- Hugging Face Space inference integration
- Supabase integration
- Qdrant integration
- type-safe Pydantic schemas
- environment variables
- logging
- error handling
- CPU fallback support
- Docker support

Generate complete starter implementation.
```

---

# Final Architecture Philosophy

This system is NOT a traditional classifier.

It is:

- an embedding system
- a retrieval system
- a clustering engine
- a semantic memory layer
- an evolving identity graph

The intelligence comes from:

- embeddings
- similarity search
- semantic understanding
- retrieval
- clustering
- user feedback

rather than expensive retraining.

