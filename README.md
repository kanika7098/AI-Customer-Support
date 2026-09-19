\# AI-Powered E-Commerce Customer Support \& Ticketing System



An AI-powered customer support platform for e-commerce applications that combines a locally hosted Large Language Model (LLM), Retrieval-Augmented Generation (RAG), order lookup, and automated human escalation.



The system is designed to answer customer questions using company-specific policies while reducing unsupported or fabricated responses. It also provides an admin dashboard for managing support tickets.



\## 🚀 Key Features



\* 🤖 AI-powered customer support using Qwen2.5

\* 🔒 Fully local AI inference using Ollama

\* 💰 No paid API keys required

\* 📚 Retrieval-Augmented Generation (RAG)

\* 🔎 FAISS-based semantic search

\* 🧠 Sentence Transformers embeddings

\* 📦 SQLite-based order lookup

\* 🎫 Automatic support ticket creation

\* 👤 Human-agent escalation for unresolved issues

\* 🛡️ Policy-grounded responses to reduce hallucinations

\* 📊 Admin dashboard for ticket management and analytics

\* 💻 Streamlit web interface

\* ⚡ Runs locally on CPU



\---



\## 🏗️ System Architecture



```text

&#x20;                   ┌──────────────────────┐

&#x20;                   │      Customer        │

&#x20;                   │   Web Interface      │

&#x20;                   └──────────┬───────────┘

&#x20;                              │

&#x20;                              ▼

&#x20;                   ┌──────────────────────┐

&#x20;                   │      Streamlit       │

&#x20;                   │     Customer App     │

&#x20;                   └──────────┬───────────┘

&#x20;                              │

&#x20;                              ▼

&#x20;                   ┌──────────────────────┐

&#x20;                   │    Support Agent     │

&#x20;                   │ Intent \& Rule Logic  │

&#x20;                   └──────────┬───────────┘

&#x20;                              │

&#x20;             ┌────────────────┼────────────────┐

&#x20;             │                │                │

&#x20;             ▼                ▼                ▼

&#x20;      ┌─────────────┐  ┌─────────────┐  ┌─────────────┐

&#x20;      │ Order Lookup│  │ RAG Search  │  │ Escalation  │

&#x20;      │   SQLite    │  │    FAISS    │  │   Tickets   │

&#x20;      └─────────────┘  └──────┬──────┘  └──────┬──────┘

&#x20;                              │                 │

&#x20;                              ▼                 ▼

&#x20;                      ┌─────────────┐     ┌─────────────┐

&#x20;                      │ Qwen2.5 LLM │     │   SQLite    │

&#x20;                      │   Ollama    │     │   Tickets   │

&#x20;                      └──────┬──────┘     └─────────────┘

&#x20;                             │

&#x20;                             ▼

&#x20;                      ┌─────────────┐

&#x20;                      │   Response  │

&#x20;                      │  to Customer│

&#x20;                      └─────────────┘





&#x20;                   ┌──────────────────────┐

&#x20;                   │    Admin Dashboard   │

&#x20;                   │      Streamlit       │

&#x20;                   └──────────┬───────────┘

&#x20;                              │

&#x20;                              ▼

&#x20;                   ┌──────────────────────┐

&#x20;                   │ Ticket Management \&  │

&#x20;                   │      Analytics       │

&#x20;                   └──────────────────────┘

```



\---



\## 🧠 How the AI System Works



The system combines deterministic business rules with a local LLM and RAG.



\### 1. Customer asks a question



Example:



```text

Where is my order ORD1001?

```



\### 2. Intent and rule processing



The support agent determines whether the request is related to:



\* Order tracking

\* Returns

\* Refunds

\* Delivery

\* Cancellation

\* Damaged products

\* General policy questions

\* Human support escalation



\### 3. Order lookup



For order-related questions, the system queries the SQLite database.



Example:



```text

ORD1001

↓

Wireless Headphones

↓

Status: Shipped

↓

Expected Delivery: 2026-09-22

↓

Tracking: TRK1001001

```



\### 4. RAG retrieval



For policy questions, the system searches the company knowledge base using:



\* Sentence Transformers

\* FAISS

\* Semantic similarity search



Relevant policy information is retrieved before generating the answer.



\### 5. Local LLM generation



The retrieved information is provided to:



```text

Qwen2.5 3B

&#x20;    ↓

Ollama

&#x20;    ↓

Local CPU inference

```



This allows the project to run without a paid cloud LLM API.



\### 6. Human escalation



If the system cannot confidently answer a question or the customer reports an issue requiring human review, a support ticket is created in SQLite.



\---



\## 🛡️ Hallucination Prevention



The system is designed to avoid inventing information.



For example, if the company policy does not mention compensation for delayed delivery, the AI does not promise compensation.



Instead, it explains that the available company policy does not specify compensation and recommends contacting customer support.



Similarly, the system does not invent:



\* Order status

\* Tracking numbers

\* Refund status

\* Delivery status

\* Compensation

\* Unsupported company policies



\---



\## 📦 Example Customer Queries



\### Return Policy



```text

What is your return policy?

```



The system retrieves the company return policy and explains the eligibility requirements.



\### Refund Policy



```text

What is your refund policy?

```



The system explains the refund process and expected processing time.



\### Order Tracking



```text

Where is my order ORD1001?

```



Example response:



```text

Order: Wireless Headphones

Status: Shipped

Expected Delivery: 2026-09-22

Tracking Number: TRK1001001

```



\### Unknown Order



```text

Where is my order ORD9999?

```



If the order does not exist, the system does not fabricate an order status. Instead, it creates a support ticket for human assistance.



\### Damaged Product



```text

My product arrived damaged.

```



The system escalates the issue and creates a support ticket.



\---



\## 📊 Admin Dashboard



The project includes a separate administrative dashboard.



Administrators can:



\* View total tickets

\* View open tickets

\* View tickets in progress

\* View closed tickets

\* Filter tickets by status

\* Filter tickets by priority

\* Search tickets

\* View ticket details

\* Update ticket status

\* Delete tickets

\* View priority statistics

\* View ticket analytics

\* Monitor escalations



\---



\## 🛠️ Technology Stack



| Technology            | Purpose                             |

| --------------------- | ----------------------------------- |

| Python                | Core programming language           |

| Streamlit             | Web application and dashboard       |

| Ollama                | Local LLM runtime                   |

| Qwen2.5 3B            | Local language model                |

| Sentence Transformers | Text embeddings                     |

| FAISS                 | Vector similarity search            |

| PyTorch               | Machine learning backend            |

| SQLite                | Orders and support tickets database |



\---



\## 📁 Project Structure



```text

AI-Customer-Support/

│

├── app.py

├── admin\_dashboard.py

├── support\_agent.py

├── rag\_chat.py

├── order\_lookup.py

├── ticket\_manager.py

│

├── build\_knowledge\_base.py

├── create\_database.py

├── create\_tickets.py

│

├── view\_tickets.py

├── test\_ollama.py

├── test\_rag.py

│

├── requirements.txt

├── .gitignore

├── README.md

│

├── data/

│   ├── database/

│   │   └── orders.db

│   │

│   ├── documents/

│   │   └── company\_policy.txt

│   │

│   └── index/

│       ├── company\_policy.index

│       └── chunks.txt

│

└── static/

&#x20;   └── style.css

```



\---



\## ⚙️ Installation



\### 1. Clone the repository



```bash

git clone <YOUR\_GITHUB\_REPOSITORY\_URL>

cd AI-Customer-Support

```



\### 2. Create a virtual environment



```bash

python -m venv venv

```



\### 3. Activate the virtual environment



Windows:



```bash

venv\\Scripts\\activate

```



\### 4. Install dependencies



```bash

pip install -r requirements.txt

```



\### 5. Install Ollama



Install Ollama from its official website:



https://ollama.com/



\### 6. Download the Qwen2.5 model



```bash

ollama pull qwen2.5:3b

```



\### 7. Verify Ollama



```bash

ollama list

```



You should see:



```text

qwen2.5:3b

```



\---



\## ▶️ Running the Customer Support Application



Start the customer application:



```bash

python -m streamlit run app.py

```



The application will open in your browser.



\---



\## 📊 Running the Admin Dashboard



Open another terminal, activate the virtual environment, and run:



```bash

python -m streamlit run admin\_dashboard.py

```



\---



\## 🔧 Rebuilding the Knowledge Base



If the company policy document is changed, rebuild the RAG knowledge base:



```bash

python build\_knowledge\_base.py

```



This generates the FAISS index and text chunks used by the retrieval system.



\---



\## 🗄️ Database



The project uses SQLite for local data storage.



The database contains:



\### Orders



\* Order ID

\* Customer name

\* Product

\* Order status

\* Order date

\* Expected delivery

\* Tracking number



\### Support Tickets



\* Ticket ID

\* Customer name

\* Order ID

\* Issue

\* Priority

\* Status

\* Creation time



\---



\## 🔐 Privacy \& Cost



This project is designed around local execution.



Customer questions are processed using a locally hosted LLM through Ollama rather than a paid cloud AI API.



Benefits include:



\* No OpenAI API key required

\* No paid LLM API required

\* No per-request API cost

\* Local model inference

\* Local SQLite database

\* Local FAISS knowledge base



\---



\## 🎯 Project Goals



This project demonstrates practical implementation of:



\* Large Language Models

\* Retrieval-Augmented Generation

\* Semantic search

\* Vector databases

\* Prompt engineering

\* Rule-based AI systems

\* Database integration

\* Customer support automation

\* Human-in-the-loop escalation

\* Web application development

\* AI safety and hallucination prevention



\---



\## 🚀 Future Improvements



Possible future extensions include:



\* Customer authentication

\* Real e-commerce API integration

\* Email support integration

\* Multilingual customer support

\* Voice-based support

\* Product recommendation system

\* Advanced analytics

\* Conversation history stored per customer

\* Role-based admin authentication

\* Deployment using Docker

\* Cloud deployment



\---



\## 👩‍💻 Author



\*\*Kanika Gaikwad\*\*



AI / Machine Learning Project

Python • LLM • RAG • FAISS • Streamlit • SQLite



