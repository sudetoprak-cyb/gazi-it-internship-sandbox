from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from core.scanner import SecurityScanner 

# --- API Application Setup ---
app = FastAPI(
    title="SecurCode SAST Engine",
    version="1.0.0",
    description="A DevSecOps microservice for structural Static Application Security Testing (SAST). Detects security flaws in source code prior to deployment.",
    contact={
        "name": "Security Engineering Team"
    }
)

# --- Data Validation Models ---
class CodePayload(BaseModel):
    language: str = Field(
        ..., 
        description="Target programming language (e.g., python)",
        examples=["python"]
    )
    source_code: str = Field(
        ..., 
        description="Raw source code payload to be analyzed",
        examples=["def authenticate():\n    api_key = 'sk_test_12345'\n    eval('print(\"Executing user input...\")')"]
    )

# --- API Endpoints ---

@app.get("/", tags=["System Health"], summary="Check API Status")
def health_check() -> dict:
    """
    Verifies that the SecurCode engine is active and ready to accept requests.
    """
    return {"status": "active", "service": "SecurCode SAST API is operational."}

@app.post("/api/v1/scan", tags=["Security Engine"], summary="Initiate Code Analysis")
def scan_code(payload: CodePayload) -> dict:
    """
    Ingests source code and executes the SAST engine to identify vulnerabilities 
    using Abstract Syntax Tree (AST) parsing and pattern matching.
    """
    if payload.language.lower() != "python":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported language. Currently, only Python is supported."
        )

    # Initialize the scanner with the provided source code
    scanner = SecurityScanner(payload.source_code)
    
    # Execute the analysis
    findings = scanner.scan()

    return {
        "status": "success",
        "target_language": payload.language,
        "metrics": {
            "vulnerabilities_found": len(findings)
        },
        "vulnerabilities": findings
    }