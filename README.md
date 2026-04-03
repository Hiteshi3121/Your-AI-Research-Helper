# 📄 AI Researcher (with Langgraph Agents & Tools)

An **agentic AI system for end-to-end research paper generation**, capable of:
- Discovering research papers from arXiv
- Reading and summarizing PDFs
- Ideating novel research directions
- Writing full academic research papers
- Compiling them into **LaTeX-generated PDFs**
- Providing an interactive **Streamlit UI**

This project demonstrates **real-world agent orchestration**, **tool usage**, **memory**, and **LLM-driven reasoning**, making it ideal for **AI Engineer / GenAI Engineer portfolios**.

<img width="1919" height="887" alt="image" src="https://github.com/user-attachments/assets/cad92efa-5d70-4121-90c6-35f0f31af415" />
<img width="1596" height="669" alt="image" src="https://github.com/user-attachments/assets/357ba76d-962f-4574-8317-ce9796a395da" />
<img width="1621" height="716" alt="image" src="https://github.com/user-attachments/assets/75dbd130-ca0f-47b8-afd1-b91b8a387836" />
<img width="1698" height="870" alt="image" src="https://github.com/user-attachments/assets/e811dbf9-cdf6-4885-874c-2ad7187d8f73" />

Scren recording link - https://drive.google.com/file/d/1GwQglKLT_sQru_W2eDOOrsvMh9Od703-/view?usp=sharing

---
## TOPIC COVERED : 
● AI Agents with Langgraph (Nodes & Edges)
● Agentic Workflow with Tools
● Agentic Web Scraping (LLM: Gemini 2.5-Pro)
● GenAI App development (langgraph, langchain, etc)
    ○ AI Agents
    ○ Agentic Workflow
    ○ Tools
● Streamlit (Frontend)
● Tools for AI Agent
    ○ Literature review with arXiv
    ○ Read & Scrape Papers
    ○ Ready-to-publish Research paper

## 🚀 Key Features

- 🔎 **arXiv Search Agent** – Finds recent research papers by topic
- 📚 **PDF Reader Tool** – Extracts and processes academic PDFs
- ✍️ **Research Writing Agent** – Generates structured academic papers
- 📄 **LaTeX → PDF Pipeline** – Uses Tectonic for deterministic PDF builds
- 🧠 **Agentic Reasoning (ReAct + LangGraph)** – Tool-aware decision making
- 💬 **Conversational Memory** – Maintains multi-turn research context
- 🖥️ **Streamlit UI** – Chat-based interface with PDF download support

---

## 🧠 Architecture Overview

User (Streamlit UI)
↓
LangGraph ReAct Agent
↓
┌──────────────────────────────┐
│ Tools │
│ • arxiv_search_tool │
│ • read_pdf │
│ • render_latex_pdf │
└──────────────────────────────┘
↓
LaTeX → Tectonic → PDF


---

## 🛠️ Tech Stack

**Core Technologies Used**
- **LLMs**: Gemini (primary), OpenAI / Anthropic (pluggable)
- **Agent Framework**: LangGraph + LangChain
- **Research Sources**: arXiv
- **PDF Processing**: PyPDF2, LaTeX, Tectonic
- **UI**: Streamlit
- **Language**: Python
---

## 📂 Project Structure

├── ai_researcher2.py # LangGraph-powered agent (used by UI)
├── arxiv_tool.py # arXiv search tool
├── read_pdf.py # PDF reader tool
├── write_pdf.py # LaTeX → PDF rendering tool
├── frontend.py # Streamlit UI
├── output/ # Generated PDFs
├── .env # API keys
├── requirements.txt
└── README.md

### 🔁 End-to-End Flow

1. **User Interaction (Streamlit UI)**
   - User provides a research topic or idea
   - Conversation is maintained across turns

2. **Agent Orchestration (LangGraph)**
   - A ReAct-style agent reasons about the task
   - Decides which tool to invoke at each step
   - Maintains context and intermediate reasoning

3. **LLM Reasoning Layer**
   - Gemini is used as the primary reasoning model
   - Prompt-enforced tool usage for PDF generation
   - Can be extended to OpenAI / Anthropic models

4. **Tooling Layer**
   - **arxiv_search_tool** → Finds relevant research papers
   - **read_pdf** → Extracts text from academic PDFs
   - **render_latex_pdf** → Compiles LaTeX into a PDF using Tectonic

5. **Artifact Generation**
   - Research paper is written in LaTeX
   - Sanitized and normalized for compilation safety
   - Final PDF is generated and stored locally

6. **Output Delivery**
   - Streamlit UI provides a **Download PDF** button
   - User receives a publication-ready research paper

---

## Install Dependencies
pip install -r requirements.txt

## Install Tectonic (Required for PDFs)
👉 https://tectonic-typesetting.github.io/en-US/install.html

## Running the Application
🖥️ Streamlit UI
>> streamlit run frontend.py

🧪 CLI Mode (Optional)
>> python ai_researcher.py
