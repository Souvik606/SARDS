import io
import queue
import sys
import threading

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from sards import shell

app = FastAPI(title="SARDS API", version="1.0.0")

# Dictionary to hold session states
sessions = {}


class CodeRequest(BaseModel):
    code: str


class InputRequest(BaseModel):
    input_data: str


def run_shell(session_id: str, input_queue: queue.Queue, output_queue: queue.Queue):
    """Run the shell in a separate thread."""
    stdout_backup = sys.stdout
    stdin_backup = sys.stdin
    sys.stdout = io.StringIO()

    while True:
        try:
            command = input_queue.get()
            if command is None:
                break

            sys.stdin = io.StringIO(command)

            # Execute the command
            shell.run("<stdin>", command)

            # Capture the output
            captured_output = sys.stdout.getvalue()
            output_queue.put(captured_output)

            sys.stdout.truncate(0)
            sys.stdout.seek(0)

        except Exception as e:
            output_queue.put(f"Error: {str(e)}")

    sys.stdout = stdout_backup
    sys.stdin = stdin_backup


@app.post("/execute/{session_id}", response_model=dict)
async def execute_code(session_id: str, request: CodeRequest):
    # Check if the session already exists
    if session_id not in sessions:
        # Create a new session
        sessions[session_id] = {
            "input_queue": queue.Queue(),
            "output_queue": queue.Queue(),
            "thread": None  # Initialize thread as None
        }
        # Start the shell thread
        sessions[session_id]["thread"] = threading.Thread(
            target=run_shell,
            args=(session_id, sessions[session_id]["input_queue"], sessions[session_id]["output_queue"]),
            daemon=True
        )
        sessions[session_id]["thread"].start()

    # Execute the provided code
    sessions[session_id]["input_queue"].put(request.code)  # Send code to the shell

    # Check for output from the output queue
    output = []
    while not sessions[session_id]["output_queue"].empty():
        output.append(sessions[session_id]["output_queue"].get())

    return {"output": "\n".join(output)}


@app.post("/input/{session_id}", response_model=dict)
async def input_data(session_id: str, request: InputRequest):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    # Send input data to the shell
    sessions[session_id]["input_queue"].put(request.input_data)

    # Retrieve output from the output queue
    output = []
    while not sessions[session_id]["output_queue"].empty():
        output.append(sessions[session_id]["output_queue"].get())

    return {"output": "\n".join(output), "message": "Input sent successfully"}


@app.get("/")
async def get():
    return {"message": "Welcome to the SARDS API. Use /execute and /input endpoints."}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
