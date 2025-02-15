import io
import sys

from fastapi import FastAPI
from pydantic import BaseModel

from sards import shell

app = FastAPI(title="SARDS API", version="1.0.0")


@app.get("/test-output", response_model=dict)
async def test_output():
    stdout_backup = sys.stdout
    sys.stdout = io.StringIO()
    try:
        # Simulate terminal output
        print("Terminal output capture is working!")

        # Capture terminal output
        captured_output = sys.stdout.getvalue()
    finally:
        sys.stdout = stdout_backup

    return {"captured_output": captured_output}


class CodeRequest(BaseModel):
    code: str


@app.post("/execute", response_model=dict)
async def execute_code(request: CodeRequest):
    code = request.code

    stdout_backup = sys.stdout
    sys.stdout = io.StringIO()

    try:
        print(code)
    finally:
        sys.stdout = stdout_backup


@app.post("/parse", response_model=dict)
async def parse_code(request: CodeRequest):
    code = request.code

    ast = shell.run("<stdin>", code)

    return {"ast": str(ast)}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
