import ast
import re
from typing import List, Dict, Any

class SecurityScanner:
    """
    A Static Application Security Testing (SAST) engine that analyzes Python source code 
    to detect vulnerabilities such as hardcoded secrets and dangerous function calls.
    """

    def __init__(self, source_code: str):
        self.source_code = source_code
        self.vulnerabilities: List[Dict[str, Any]] = []

    def scan(self) -> List[Dict[str, Any]]:
        """
        Executes the security scanning rules against the provided source code.
        
        Returns:
            List[Dict[str, Any]]: A list of detected vulnerabilities with their severity and details.
        """
        self._check_hardcoded_secrets()
        
        try:
            tree = ast.parse(self.source_code)
            self._check_dangerous_functions(tree)
        except SyntaxError as e:
            self.vulnerabilities.append({
                "type": "SyntaxError",
                "severity": "High",
                "line": getattr(e, 'lineno', 'Unknown'),
                "message": "The provided payload is not valid Python code and failed to compile."
            })

        return self.vulnerabilities

    def _check_hardcoded_secrets(self) -> None:
        """
        Scans for hardcoded credentials or API keys using Regular Expressions.
        """
        pattern = re.compile(r'(password|secret|api_key|token)\s*=\s*[\'"][^\'"]+[\'"]', re.IGNORECASE)
        
        for line_number, line in enumerate(self.source_code.splitlines(), start=1):
            if pattern.search(line):
                self.vulnerabilities.append({
                    "type": "Hardcoded Secret",
                    "severity": "Critical",
                    "line": line_number,
                    "message": "Sensitive data assignment (password, key, or token) detected in plaintext."
                })

    def _check_dangerous_functions(self, tree: ast.AST) -> None:
        """
        Traverses the Abstract Syntax Tree (AST) to identify executions of dangerous functions 
        that may lead to Remote Code Execution (RCE).
        """
        dangerous_calls = {'eval', 'exec', 'os.system', 'subprocess.call', 'subprocess.Popen'}
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                # Extract function name if it's a direct call or an attribute call (e.g., os.system)
                func_name = None
                if hasattr(node.func, 'id'):
                    func_name = node.func.id
                elif hasattr(node.func, 'attr'):
                    func_name = f"{getattr(node.func.value, 'id', '')}.{node.func.attr}"

                if func_name and func_name in dangerous_calls:
                    self.vulnerabilities.append({
                        "type": "Dangerous Function Call",
                        "severity": "High",
                        "line": getattr(node, 'lineno', 'Unknown'),
                        "message": f"Execution of dangerous function '{func_name}' detected. Potential RCE risk!"
                    })