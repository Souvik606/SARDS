import io
import sys

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from sards import shell

app = FastAPI(title="SARDS API", version="1.0.0")

@app.get("/test-output", response_model=dict)
async def test_output():
    stdout_backup = sys.stdout
    sys.stdout = io.StringIO()
    try:
        print("Terminal output capture is working!")
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
        shell.run("<stdin>", code)

        captured_output = sys.stdout.getvalue()
    finally:
        sys.stdout = stdout_backup

    return {"output": captured_output}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
