# 🛡️ SecurCode: Containerized SAST & DevSecOps API

> A production-ready, containerized Static Application Security Testing (SAST) microservice designed to enforce Shift-Left security principles.

## 📌 Project Overview
SecurCode is an advanced, lightweight API engine built to analyze Python source code for critical security vulnerabilities prior to deployment. Instead of relying purely on rudimentary string matching, it leverages Python's **Abstract Syntax Tree (AST)** for structural code analysis, ensuring high precision in detecting Remote Code Execution (RCE) vectors and hardcoded credentials. 

This project emphasizes **DevSecOps best practices**, featuring strict data validation, automated vulnerability categorization, and a hardened Docker environment.

## 🚀 Key Security Features
* **AST-Based RCE Detection:** Structurally identifies the invocation of high-risk functions (e.g., `eval`, `exec`, `os.system`) to prevent command injection and RCE.
* **Hardcoded Secret Discovery:** Utilizes compiled Regular Expressions to instantly flag embedded API keys, passwords, and tokens in plaintext.
* **Strict Payload Validation:** Implements `Pydantic` models to enforce rigid type checking and payload sanitization at the API gateway.
* **Hardened Containerization:** The Docker environment operates strictly under the **Least Privilege** principle. It utilizes a lightweight `python:3.10-slim` base image and executes the API via a restricted, non-root user (`securuser`) to mitigate privilege escalation attacks.

## 📂 Repository Structure
This microservice is a component of a broader secure infrastructure architecture:
```text
week3-docker-java-backend/
├── securcode-python-sast/
│   ├── core/
│   │   └── scanner.py          # AST and Regex detection logic
│   ├── main.py                 # FastAPI endpoints and Pydantic schemas
│   ├── requirements.txt        # Pinned dependencies
│   ├── Dockerfile              # Hardened, non-root container configuration
│   ├── docker-compose.yml      # Orchestration with security opts
│   └── README.md               # Project documentation
🛠️ Technology Stack
Core Framework: Python 3.10+, FastAPI, Uvicorn (ASGI)
Security & Analysis: ast (Abstract Syntax Trees), re (Regex Engine)
Data Validation: Pydantic (v2)
Infrastructure: Docker, Docker Compose (Security Opts enabled)
API Documentation: OpenAPI (Swagger UI)
🐳 Deployment (Dockerized)
Deploying the engine locally is streamlined via Docker Compose. The configuration automatically prevents new privileges and isolates the service.

Bash
# 1. Navigate to the project directory
cd securcode-python-sast

# 2. Build and run the hardened container in detached mode
docker-compose up -d --build

# 3. Verify the container status
docker ps
📡 API Usage & Interactive Documentation
Once the container is operational, the OpenAPI specification and interactive Swagger UI are accessible at:
👉 http://127.0.0.1:8000/docs

Endpoint: POST /api/v1/scan
Submit raw Python code to receive an immediate JSON report detailing identified vulnerabilities, severity levels, and specific line numbers.

Sample Request Payload:

JSON
{
  "language": "python",
  "source_code": "import os\ndef system_manager():\n    api_key = 'sk_live_987654321'\n    os.system('ls -la')"
}
Sample Automated Security Report (Response):

JSON
{
  "status": "success",
  "target_language": "python",
  "metrics": {
    "vulnerabilities_found": 2
  },
  "vulnerabilities": [
    {
      "type": "Hardcoded Secret",
      "severity": "Critical",
      "line": 3,
      "message": "Sensitive data assignment (password, key, or token) detected in plaintext."
    },
    {
      "type": "Dangerous Function Call",
      "severity": "High",
      "line": 4,
      "message": "Execution of dangerous function 'os.system' detected. Potential RCE risk!"
    }
  ]
}