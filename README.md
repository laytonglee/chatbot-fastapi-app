# 🤖 AUPP Chatbot – Deployment Guide

![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Render](https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

This project uses **FastAPI**, **Docker**, and **Render** for automatic deployment. Render monitors the `main` branch and redeploys on every push.

---

## 📁 Project Structure

```
chatbot-fastapi-app/
│── app/
│    ├── models/
│    │    ├── faq_with_embeddings.joblib
│    │    └── pipeline_svm.joblib
│    ├── chatbot.py
│    └── main.py
│── frontend/
│    └── index.html
│── Dockerfile
│── requirements.txt
│── README.md
```

---

## 🚀 Deployment (GitHub → Render)

### Step 1 — Push code to GitHub
Make sure `Dockerfile` and FastAPI app are in the root directory.

### Step 2 — Create a Render Web Service
1. Go to [Render.com](https://render.com) → **New Web Service**
2. Choose **"Build from GitHub Repo"**
3. Select your chatbot repository
4. Render auto-detects your `Dockerfile`
5. Set the environment:
   * **Environment:** Docker
   * **Branch:** `main`
   * **Auto Deploy:** Yes (Recommended)

Render will build and run:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

## 🌐 API Endpoint

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/`      | Go to Home Page |
| POST   | `/chat`  | Ask chatbot |

---


---

## ♻️ Automatic Redeploy

Every push to `main` triggers:
1. ✅ Build Docker image
2. ✅ Install dependencies
3. ✅ Start FastAPI server
4. ✅ Deploy new version


### 👥 Contributors
This is an academic project developed as part of ITM 454 course at AUPP.
