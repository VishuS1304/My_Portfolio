# 🧠 Vishwajit Singh — AI/ML Portfolio Website

Welcome to my professional AI portfolio — an interactive website showcasing my real-time AI projects, skills, and experience. It features an animated chatbot powered by NVIDIA LLaMA 3.3, a responsive UI, and light/dark themes.

🌐 **Live Site**: [vishus1304.github.io/My_Portfolio](https://vishus1304.github.io/My_Portfolio/)

---

## 📌 Features

- ✅ Modern, mobile-responsive design
- 🧠 AI chatbot (FastAPI + NVIDIA LLaMA 3.3)
- 📥 Resume viewer & downloader
- 🌙 Theme toggle (light/dark)
- 🎯 Real projects with live GitHub links
- ⬆️ Scroll-to-top & animated social icons
- 📬 Contact form with EmailJS

---

## 🗂 Project Structure

```bash
My_Portfolio/
├── backend
│     ├── chatbot.py         # FastAPI app for AI chatbot
│     ├── requirements.txt   # Python packages for backend
│     └── resume             # PDF resume used by chatbot
│        
├── index.html               # Main HTML file
├── styles.css               # Custom styles for entire site
├── scripts.js               # JS for chatbot, scroll, theme toggle
├── images/                  # Icons, screenshots, logos
├── LICENSE                  # MIT License
└── README.md                # This file
````

---

## 🧰 Tech Stack

| Category     | Tools & Frameworks                                   |
| ------------ | ---------------------------------------------------- |
| Frontend     | HTML, CSS, JavaScript                                |
| Backend      | Python, FastAPI, LangChain, PyPDF2                   |
| AI Model     | NVIDIA LLaMA 3.3 via `langchain_nvidia_ai_endpoints` |
| Deployment   | GitHub Pages (Frontend)                              |
| Chat API     | FastAPI on localhost or Render                       |
| Integrations | EmailJS, GitHub, LinkedIn                            |

---

## 🚀 Getting Started (Local Setup)

### 📦 Prerequisites

* Python 3.9+
* `pip` for installing dependencies

### 🔧 Backend Setup (Chatbot)

1. Clone the repo:

   ```bash
   git clone https://github.com/VishuS1304/My_Portfolio.git
   cd My_Portfolio
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up your `.env` file:

   ```env
   NVIDIA_API_KEY=nvapi-xxxxxxxxxxxxxxxxxxxx
   ```

4. Run the backend:

   ```bash
   uvicorn backend-chatbot:app --reload
   ```

Backend will run at `http://127.0.0.1:8000`.

---

## 🌐 Frontend Setup

1. Open `index.html` in your browser.
2. Ensure chatbot API in `scripts.js` matches backend:

   ```js
   const API_BASE = "http://127.0.0.1:8000";
   ```

---

## 🧠 How the AI Chatbot Works

* Loads your PDF resume from `resume/`
* Uses `langchain_nvidia_ai_endpoints` to query LLaMA 3.3
* Responds in real-time via Server-Sent Events (SSE)

---

## 📬 Contact

* ✉️ Email: [vishwajitsingh1304@gmail.com](mailto:vishwajitsingh1304@gmail.com)
* 💼 LinkedIn: [linkedin.com/in/vishwajit-singh-69175319b](https://linkedin.com/in/vishwajit-singh-69175319b)
* 👨‍💻 GitHub: [github.com/VishuS1304](https://github.com/VishuS1304)

---

## 📄 License

This project is licensed under the MIT License. See [`LICENSE`](LICENSE) for details.

---

> Built with ❤️ by Vishwajit Singh — AI Developer focused on real-time ML, autonomous agents & intelligent automation.

