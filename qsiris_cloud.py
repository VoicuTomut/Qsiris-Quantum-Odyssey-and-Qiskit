"""
Run the server using:
uvicorn qsiris_cloud:app --host 0.0.0.0 --port 7001 --reload

"""
import json
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any

from qsiris_api import execute_qiskit,decompose_qiskit


# Initialize FastAPI app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


# Root endpoint for a basic server check
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Qiskit Server!"}


# Define an input Pydantic model for JSON input
class InputData(BaseModel):
    di: dict


# QO_QK_convertor Endpoint - Handles file uploads
@app.post("/QO_QK_convertor")
async def qo_qk_convertor(data: InputData):
    """
    Endpoint to handle QO_QK conversion with JSON input as a dictionary.
    """
    puzzle = data.di  # Extract the dictionary from the input

    try:
        # Process the puzzle with execute_qiskit and decompose_qiskit
        simulated_counts = execute_qiskit(puzzle)
        qasm_circuit = decompose_qiskit(puzzle)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Prepare the response
    result = {
        "simulated_counts": simulated_counts,
        "qasm_circuit": qasm_circuit,
    }
    return result