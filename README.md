# My Portfolio

Welcome to my portfolio website! This repository contains the source code and configuration for both the frontend static site and the backend AI-powered chatbot API.

---

## 🚀 Live Demo

* **Frontend**: https\://\<your-frontend-domain>
* **Backend API**: https\://\<your-backend-domain>/chat/stream

*(Replace `<your-frontend-domain>` and `<your-backend-domain>` with your actual custom or Render URLs.)*

---

## 📂 Repository Structure

```
My_Portfolio/          # Static portfolio site (HTML/CSS/JS or framework source)
├── index.html
├── styles/
├── scripts/
├── backend/             # FastAPI chatbot backend
│   ├── chatbot.py       # Main FastAPI application
│   ├── requirements.txt # Python dependencies
│   ├── Procfile         # Render start command
│   ├── .env.example     # Environment variable template
│   └── ...
├── README.md            # This file
└── .gitignore
```

---

## 🛠️ Frontend Setup & Deployment

### Prerequisites

* Node.js (v16+)
* npm or yarn

### Local Development

1. Navigate to the frontend directory:

   ```bash
   cd frontend
   ```
2. Install dependencies (if using a framework):

   ```bash
   npm install
   # or
   yarn install
   ```
3. Start a local development server:

   * **Static HTML**: open `index.html` in your browser.
   * **React/Vue/Svelte**:

     ```bash
     npm run dev
     # or
     yarn dev
     ```
4. Build for production:

   ```bash
   npm run build
   # or
   yarn build
   ```
5. Preview the build locally (optional):

   ```bash
   npx serve build
   ```

### Deploy to GitHub Pages

1. Ensure your build output is in a folder named `docs` or root.
2. In `package.json`, add:

   ```json
   "homepage": "https://<username>.github.io/<repo>/"
   ```
3. Push to GitHub and configure Pages:

   * Go to **Settings → Pages**
   * Source: `main` branch → `/root` or `/docs`

---

## ⚙️ Backend Setup & Deployment

### Prerequisites

* Python 3.8+
* pip

### Local Development

1. Navigate to the backend directory:

   ```bash
   cd backend
   ```
2. Create & activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/macOS
   venv\Scripts\activate    # Windows
   ```
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
4. Copy & configure environment variables:

   ```bash
   cp .env.example .env
   ```

   * Fill in your `NVIDIA_API_KEY` and `ALLOWED_ORIGINS` values in `.env`.
5. Run the FastAPI server:

   ```bash
   uvicorn chatbot:app --reload
   ```
6. Test the health endpoint:

   ```bash
   curl http://127.0.0.1:8000/health
   ```

### Deploy to Render

1. Push `main` branch to GitHub.
2. In [Render Dashboard](https://dashboard.render.com/):

   * **New → Web Service**
   * Connect your repo and select branch `main`.
   * **Root Directory**: `backend`
   * **Build Command**: `pip install -r requirements.txt`
   * **Start Command**: `uvicorn chatbot:app --host 0.0.0.0 --port $PORT`
   * **Environment Variables**: add `NVIDIA_API_KEY`, `ALLOWED_ORIGINS`, etc.
3. Click **Create Web Service** and wait for deployment.
4. Note the generated URL: `https://<your-backend>.onrender.com`

---

## 🔧 Configuration

* **Environment Variables** (backend):

  * `NVIDIA_API_KEY` – API key for NVIDIA LLM service.
  * `ALLOWED_ORIGINS` – Comma-separated list of allowed CORS origins.

* **CORS**: Ensure `ALLOWED_ORIGINS` matches your frontend deployment URL(s).

---

## 📞 Contact & Contributions

Feel free to open issues or submit pull requests. For questions or feedback, reach out:

* Email: [vishwajitsingh1304@gmail.com](mailto:vishwajitsingh1304@gmail.com)
* GitHub: [https://github.com/VishuS1304](https://github.com/VishuS1304)

---

© 2025 Vishwajit Singh. All rights reserved.
