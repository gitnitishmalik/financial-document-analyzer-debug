# Financial Document Analyzer – Debug Challenge  

## Overview  

The **Financial Document Analyzer** is an AI-powered system that processes corporate financial documents, including reports, statements, and investment updates. It generates **investment recommendations**, **risk assessments** and **market insights** using specialized AI agents.  

This project was originally provided with multiple bugs and incomplete implementations. The following document highlights the **debugging process, solutions implemented and instructions to run the system**.  

---

## Bugs Found and Fixed  

- **File:** `agents.py`  
  - **Original Issue:** `llm = llm` uninitialized  
  - **Modification / Fix:** Initialized `LLM(model="ollama/llama3", timeout=300)`  
  - **Impact:** LLM is now properly defined; avoids runtime errors  

- **File:** `agents.py`  
  - **Original Issue:** `max_iter=1` for agents  
  - **Modification / Fix:** Increased to `max_iter=3`  
  - **Impact:** Agents can now use tools, analyze data, and respond fully  

- **File:** `agents.py`  
  - **Original Issue:** `FinancialDocumentTool.read_data_tool` import incorrect  
  - **Modification / Fix:** Updated to `tools=[read_data_tool]`  
  - **Impact:** Tools work correctly within agents  

- **File:** `agents.py`  
  - **Original Issue:** Duplicate `risk_assessor` definition  
  - **Modification / Fix:** Removed duplicate  
  - **Impact:** Prevents overwriting and runtime errors  

- **File:** `tasks.py`  
  - **Original Issue:** Tasks referencing incorrect tools  
  - **Modification / Fix:** Updated to use `read_data_tool`  
  - **Impact:** Tasks now process PDF data correctly  

- **File:** `tasks.py`  
  - **Original Issue:** Async execution mismatch  
  - **Modification / Fix:** Handled async safely using `asyncio.to_thread`  
  - **Impact:** API non-blocking; supports large PDFs  

- **File:** `tools.py`  
  - **Original Issue:** PDF reading lacked error handling  
  - **Modification / Fix:** Added path checks, file existence verification, and try/except  
  - **Impact:** Prevents crashes for missing or corrupted PDFs  

- **File:** `tools.py`  
  - **Original Issue:** Output formatting inconsistent  
  - **Modification / Fix:** Removed extra spaces, cleaned text  
  - **Impact:** Clean input for agent analysis  

- **File:** `main.py`  
  - **Original Issue:** File saving in `data/` directory caused overwrite  
  - **Modification / Fix:** Created `temp_uploads` folder, unique filenames with UUID  
  - **Impact:** Supports concurrent uploads safely  

- **File:** `main.py`  
  - **Original Issue:** Synchronous `crew.kickoff` caused blocking  
  - **Modification / Fix:** Used `asyncio.to_thread` for kickoff  
  - **Impact:** Non-blocking API, supports large PDF processing  

- **File:** `main.py`  
  - **Original Issue:** Response model not structured  
  - **Modification / Fix:** Added `AnalysisResult` Pydantic model  
  - **Impact:** Clean, validated API responses  

- **File:** `main.py`  
  - **Original Issue:** File cleanup inconsistent  
  - **Modification / Fix:** Added `finally` block to remove uploaded files  
  - **Impact:** Prevents storage bloat  

- **File:** `requirements.txt`  
  - **Original Issue:** Library version conflicts  
  - **Modification / Fix:** Updated click and confirmed compatibility of crewai, crewai-tools, FastAPI, PyPDFLoader  
  - **Impact:** Avoids runtime dependency errors  

---

## Key Features  

- **Local PDF Uploads**: Handles multiple financial documents securely  
- **AI Agent Analysis**:  
  - Senior Financial Analyst: Investment insights  
  - Investment Advisor: Product recommendations  
  - Risk Assessor: Extreme risk assessment  
  - Verifier: Document verification  
- **Market Insights**: Generates detailed recommendations with creative URLs for demonstration  
- **Robust File Handling**: Unique filenames, temporary uploads, auto-cleanup  
- **Async-Friendly API**: Efficiently handles large documents without blocking  
- **Professional & Scalable**: Ready for future queue and database integrations  

---

## Explanation of Design Choices  

- **LLM Initialization:** Properly initialized with timeout to handle large PDFs reliably.  
- **max_iter Increased to 3:** Allows agents to use tools, analyze data, and generate responses fully.  
- **Tool Fixes:** `read_data_tool` added path validation, existence checks, exception handling for robust PDF reading.  
- **Async Execution:** Wrapped `crew.kickoff` in `asyncio.to_thread` for non-blocking processing.  
- **File Handling:** Temporary upload folder, unique UUID filenames, and auto-cleanup prevent overwrite and storage bloat.  
- **Structured API Response:** Added Pydantic model for clean, validated outputs.  
- **Requirements:** Updated versions ensure compatibility and avoid runtime errors.  
- **Professional Documentation:** Clear instructions, sample requests/responses, and scalability notes.  

---

⚙️ Setup & Installation

1️⃣ Clone the Repository
----  git clone <your-repo-link>
----  cd financial-document-analyzer

2️⃣ Create a Virtual Environment

# Windows
---  python -m venv venv
---  venv\Scripts\activate


3️⃣ Install Dependencies

---  pip install -r requirements.txt

4️⃣ Run the Application

---- uvicorn main:app --reload

The server will start at http://127.0.0.1:8000. You can access the interactive Swagger docs at /docs.
---

# 📸 System Demonstration

This section showcases the complete working flow of the Financial Document Analyzer — from API testing to backend execution and final AI-generated investment insights.

---

## 🔹 1️⃣ Swagger API – PDF Upload & Analysis Request

<p align="center">
  <img src="./assets/swagger_output.png" width="90%" alt="Swagger API Testing Interface">
</p>

### ✅ What This Demonstrates

- FastAPI interactive documentation (`/docs`)
- Successful PDF upload via multipart/form-data
- Custom investment query submission
- Structured JSON API response
- HTTP 200 success status

This confirms that:
- The API endpoint is correctly configured  
- File handling works properly  
- The response model validation is functioning  

---

## 🔹 2️⃣ Backend Execution – Multi-Agent Workflow (CrewAI)

<p align="center">
  <img src="./assets/terminal_logs.png" width="90%" alt="Backend Execution Logs">
</p>

### ✅ What This Demonstrates

- Uvicorn server startup
- Async FastAPI execution
- CrewAI multi-agent orchestration
- Tool usage (`read_data_tool`)
- Successful `/analyze` POST request
- Non-blocking execution using `asyncio.to_thread`

This validates:
- Proper LLM initialization
- Agent collaboration working correctly
- System stability during processing

---

## 🔹 3️⃣ Generated Investment Analysis (Final Output)

<p align="center">
  <img src="./assets/analysis_result.png" width="90%" alt="Investment Analysis Output">
</p>

### ✅ What This Demonstrates

- Structured JSON response format
- AI-generated market insights
- Risk identification summary
- Investment recommendations
- Clean formatted output

This confirms:
- PDF parsing is successful  
- Agent reasoning pipeline works  
- Final structured response model is applied  

---

# 🏗️ System Architecture Overview

flowchart LR
    A[Upload Financial PDF] --> B[FastAPI Endpoint]
    B --> C[Temporary File Storage]
    C --> D[CrewAI Multi-Agent System]
    D --> E[LLM - Llama3 via Ollama]
    E --> F[Investment & Risk Analysis]
    F --> G[Structured JSON Response]


🧪 Testing the API
You can test the endpoint using the following curl command:

Bash
curl -X 'POST' \
  'http://127.0.0.1:8000/analyze' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@TSLA-Q2-2025.pdf;type=application/pdf' \
  -F 'query=Analyze for investment insights'
