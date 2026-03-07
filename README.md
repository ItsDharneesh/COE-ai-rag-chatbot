# 🤖 COE AI Chatbot (RAG-Based)

A **Retrieval-Augmented Generation (RAG)** chatbot designed to answer questions related to **Operational Excellence topics** such as:

* **Lean Principles**
* **Six Sigma**
* **Business Excellence Frameworks**
* **KPI Tracking Best Practices**

The chatbot retrieves relevant information from **curated documents** and optionally **Wikipedia**, then uses an **OpenAI LLM** to generate a context-aware answer.

**Important note**: The confidence score is calculated only when the information is retrieved from the documents and not when web fallback occurs to provide the information, this webfallback was added as a secondary safety measure because the project only asked for documnet retrieval search engine this touch was added to make the search engine more dynamic. Under given time and with the additional of more than 5 documents the score can be improved. But due to the restriction of only 3 to 5 documents this method was used. 

*Now try the app and test it for yourself*.

---
## 🚀 Live App Link below

Try the app here:  
👉 https://coe-ai-rag-chatbot-kqcbu7wl6ps7gyfmsixercqc.streamlit.app/

---
# 🚀 Key Features

* **Document ingestion pipeline**
* **Smart chunking for better retrieval**
* **FAISS vector database**
* **Top-3 semantic retrieval**
* **Wikipedia fallback search**
* **LLM-based answer generation**
* **Confidence score estimation**
* **Interactive Streamlit UI**
* **Expandable context sources**

---

# 🧠 System Architecture

The chatbot follows a **Retrieval-Augmented Generation (RAG) pipeline**:

```
User Query
↓
Vector Embedding (OpenAI Embeddings)
↓
FAISS Similarity Search
↓
Top-3 Relevant Document Chunks
↓
Confidence Evaluation
↓
Wikipedia Retrieval (fallback if needed)
↓
LLM Context Injection
↓
Answer Generation
```
---
## Governance & Adoption Considerations

### 1. Data Privacy Risks in Enterprise AI

Enterprise AI systems often process sensitive organizational data such as operational documents, internal KPIs, and process documentation. When integrating Large Language Models, several privacy risks may arise:

- **Sensitive data exposure** if proprietary documents are sent to external APIs.
- **Unintended data leakage** through prompt logs or stored embeddings.
- **Improper access control**, allowing unauthorized users to query confidential information.

To mitigate these risks, organizations should implement:
- Data access controls and authentication layers
- Encryption for stored embeddings and document repositories
- Secure API handling and environment-based secret management

### 2. Hallucination Risks in Retrieval-Augmented Generation (RAG)

Although RAG systems reduce hallucinations by grounding responses in retrieved documents, they are not completely immune to inaccurate outputs.

Potential risks include:

- The model generating information **not present in retrieved documents**
- **Low-quality retrieval results** leading to incorrect answers
- Over-reliance on external sources such as Wikipedia

In this project, hallucination risk is partially mitigated through:
- Confidence scoring using similarity scores from the retriever
- Switching to Wikipedia only when document retrieval confidence is low
- Displaying retrieved context to improve transparency

### 3. Improving System Reliability

Several improvements could further increase the reliability of the system:

- **Re-ranking retrieved documents** using cross-encoder models to improve retrieval quality
- Implementing **answer grounding validation**, ensuring responses are based only on retrieved context
- Adding **feedback loops** where users can flag incorrect answers
- Using **multi-query retrieval techniques** to improve recall for complex queries
- Monitoring response quality through automated evaluation metrics

### 4. Adoption Metrics

To evaluate real-world adoption of the AI assistant, the following metrics could be tracked:

**a. Query Resolution Rate**
Percentage of user queries successfully answered without requiring external support.

**b. Usage Frequency**
Number of queries submitted per user per day or week, indicating how frequently the system is used.

**c. User Feedback / Accuracy Rating**
Users can rate responses as helpful or incorrect, allowing continuous monitoring of system accuracy.

Tracking these metrics helps assess both system performance and user adoption.

---
## Design Choices

Several design choices were made to balance simplicity, reliability, and demonstration value:

- **FAISS Vector Store** was used for efficient semantic search over document embeddings.
- **Retrieval-Augmented Generation (RAG)** was selected to reduce hallucinations and ground responses in enterprise knowledge.
- **Streamlit** was chosen for rapid prototyping of an interactive interface.
- **Wikipedia fallback retrieval** was implemented when document retrieval confidence is low, improving coverage for general questions.
---

# 🔄 Workflow

1. **User submits a query**
2. The query is converted into **vector embeddings**
3. The **FAISS vector store** retrieves the **top-3 relevant chunks**
4. A **confidence score** is calculated
5. If similarity is low → **Wikipedia fallback retrieval**
6. Retrieved context is passed to **OpenAI GPT-4o-mini**
7. The system returns:

   * **Generated answer**
   * **Source type (Documents/Wikipedia)**
   * **Confidence score**
   * **Retrieved context**

---

# 🗂 Project Structure

```plaintext
coe-ai-chatbot/
│
├── data/
│   ├── lean_principles.txt
│   ├── six_sigma.txt
│   ├── excellence_framework.txt
│   └── kpi_tracking.txt
│
├── rag/
│   ├── ingest.py
│   ├── retriever.py
│   ├── generator.py
│   └── wiki_retriever.py
│
├── vector_store/        # FAISS index (generated after ingestion)
│
├── app.py               # Streamlit UI
├── requirements.txt
├── README.md
└── .gitignore
```

---

# ⚙️ Tech Stack

**Programming Language**

* Python

**Frameworks & Libraries**

* Streamlit
* LangChain
* FAISS
* OpenAI API
* Wikipedia API

**Models**

* **OpenAI Embeddings**
* **GPT-4o-mini (LLM)**

---

# 📦 Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/coe-ai-rag-chatbot.git
cd coe-ai-rag-chatbot
```

Create virtual environment:

```bash
python -m venv coe_bot
```

Activate environment:

**Windows**

```bash
coe_bot\Scripts\activate
```

**Mac/Linux**

```bash
source coe_bot/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a **.env file** in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

⚠️ **Never commit `.env` files to GitHub.**

---

# 🧱 Build the Vector Database

Before running the chatbot, build the **FAISS vector store**:

```bash
python rag/ingest.py
```

This will:

* Load documents
* Chunk text
* Generate embeddings
* Store vectors in **FAISS**

---

# ▶️ Run the Chatbot

Start the Streamlit interface:

```bash
streamlit run app.py
```

---

# 💬 Example Queries

Try asking:

* **What are the principles of Lean manufacturing?**
* **Explain Six Sigma methodology**
* **How do companies track KPIs effectively?**
* **What are operational excellence frameworks?**

---

# 📊 Confidence Score

The chatbot computes a **confidence score based on vector similarity**:

* **Higher score → stronger document relevance**
* **Lower score → Wikipedia fallback triggered**

Displayed as:

* **Progress bar**
* **Numeric score**

---

# 🎨 User Interface Features

The Streamlit interface includes:

* **Chat-style interaction**
* **Animated loading spinner**
* **Expandable context sections**
* **Confidence visualization**
* **Source identification**

---

# 🧩 Future Improvements

Possible upgrades:

* Conversation memory
* Streaming responses
* Multi-document sources
* PDF ingestion
* Advanced reranking models

---

# 📌 Author

Developed by **Dharneesh S**

AI / ML Engineer | RAG Systems | NLP | LLM Applications

---

# 📜 License

This project is for **educational and demonstration purposes**.
