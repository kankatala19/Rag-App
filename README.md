# 🚀 Cloud-Based RAG Application

A cloud-based **Retrieval-Augmented Generation (RAG)** application that allows users to upload documents and ask natural language questions. The application retrieves relevant document content using vector embeddings and generates accurate responses using OpenAI GPT models.

The project is fully containerized with **Docker**, orchestrated using **Docker Compose**, and automatically deployed to **AWS EC2** using **Ansible** with secure secret management through **Ansible Vault**.

---

## ✨ Features

- 📄 Upload PDF, DOCX, TXT, and Markdown files
- 🤖 Ask questions about uploaded documents
- 🔍 Semantic search using vector embeddings
- 🧠 AI-powered responses with OpenAI GPT-4.1 Mini
- 💾 Persistent vector database using ChromaDB
- 🖥️ Interactive Streamlit frontend
- ⚡ FastAPI backend with REST APIs
- 🐳 Dockerized backend and frontend
- ☁️ Automated deployment on AWS EC2 using Ansible
- 🔐 Secure API key management using Ansible Vault

---

# 🏗️ Architecture

```
                User
                  │
                  ▼
         Streamlit Frontend
                  │
          HTTP Requests
                  │
                  ▼
           FastAPI Backend
                  │
                  ▼
        LangChain RAG Pipeline
          ├───────────────┐
          │               │
          ▼               ▼
     OpenAI GPT      ChromaDB
                         │
                         ▼
                 Embedded Documents
```

---

# 🛠️ Tech Stack

### Frontend
- Streamlit

### Backend
- FastAPI
- Python

### AI & RAG
- LangChain
- OpenAI GPT-4.1 Mini
- OpenAI Embeddings
- ChromaDB

### Document Processing
- PyPDF
- Docx2txt
- Recursive Character Text Splitter

### DevOps & Cloud
- Docker
- Docker Compose
- AWS EC2
- Ansible
- Ansible Vault

### Version Control
- Git
- GitHub

---

# 📁 Project Structure

```
Rag-App/
│
├── app.py
├── streamlit_app.py
├── rag.py
├── vectorstore.py
├── config.py
│
├── uploads/
├── chroma_db/
│
├── Dockerfile
├── Dockerfile.streamlit
├── docker-compose.yml
│
├── requirements-backend.txt
├── requirements-frontend.txt
│
├── ansible/
│   ├── inventory.ini
│   ├── playbook.yml
│   ├── ansible.cfg
│   └── secrets.yml
│
└── README.md
```

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/<your-username>/Rag-App.git

cd Rag-App
```

---

## Create Environment File

Create a `.env` file.

```
OPENAI_API_KEY=YOUR_OPENAI_API_KEY
```

---

## Install Dependencies

### Backend

```bash
pip install -r requirements-backend.txt
```

### Frontend

```bash
pip install -r requirements-frontend.txt
```

---

# ▶️ Run Locally

### Start Backend

```bash
uvicorn app:app --reload
```

Runs on

```
http://127.0.0.1:8000
```

---

### Start Frontend

```bash
streamlit run streamlit_app.py
```

Runs on

```
http://localhost:8501
```

---

# 🐳 Docker Deployment

Build and start the application

```bash
docker compose up --build
```

Run in background

```bash
docker compose up -d
```

Stop containers

```bash
docker compose down
```

---

# ☁️ AWS Deployment using Ansible

Configure the inventory file

```ini
[aws]
<EC2_PUBLIC_IP> ansible_user=ubuntu ansible_ssh_private_key_file=/path/to/key.pem
```

Deploy

```bash
ansible-playbook -i inventory.ini playbook.yml --ask-vault-pass
```

The playbook automatically:

- Installs Docker
- Installs Git
- Clones the GitHub repository
- Creates the `.env` file
- Builds Docker images
- Starts the application using Docker Compose

---

# 📌 Supported File Types

- PDF (.pdf)
- Microsoft Word (.docx)
- Text (.txt)
- Markdown (.md)

---

# 🔄 Workflow

```
Upload Document
        │
        ▼
Document Loader
        │
        ▼
Text Chunking
        │
        ▼
OpenAI Embeddings
        │
        ▼
ChromaDB Vector Store
        │
        ▼
User Question
        │
        ▼
Similarity Search
        │
        ▼
GPT-4.1 Mini
        │
        ▼
Answer
```

---

# 🚀 Future Improvements

- Conversation Memory
- Multi-document search
- User Authentication
- CI/CD using GitHub Actions
- HTTPS with SSL
