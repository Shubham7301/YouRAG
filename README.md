# 🎬 YouRAG — YouTube RAG App using LangChain & Streamlit

**YouRAG** is a simple but powerful Retrieval-Augmented Generation (RAG) app that allows you to ask questions about any YouTube video using its transcript. It extracts the transcript, indexes it using FAISS, and uses OpenAI's GPT model to generate accurate answers based on video content.

---

## 🚀 Features

- 🔍 **Transcript Retrieval** using `youtube-transcript-api`
- 🧠 **LangChain-powered RAG pipeline**
- ⚡ **FAISS** vector store for efficient similarity search
- 🗣️ **Natural language Q&A** with OpenAI's GPT-4o model
- 🖥️ **Streamlit UI** — fast, clean, and interactive

---

## 📸 Demo

> 📌 Paste a YouTube video URL or ID, type your question, and click **"Run RAG Pipeline"** — the app will fetch the transcript, build a vector store, retrieve relevant chunks, and answer your question.

<img width="1469" height="868" alt="Screenshot 2025-07-13 at 4 26 03 PM" src="https://github.com/user-attachments/assets/c967257a-5125-4246-b0c7-b2cadd34bfc9" />
<!-- Add screenshot or Streamlit Cloud link here -->

---

## 🛠️ Tech Stack

- **Python**
- **Streamlit**
- **LangChain**
- **OpenAI API**
- **FAISS**
- **YouTube Transcript API**
- **dotenv**




## 📦 Installation

Clone the repository and set up your environment:

```bash
git clone https://github.com/Shubham7301/YouRAG.git
cd botube

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt
