<div align="center">
  <img src="media/sards-logo.png" alt="SARDS Logo" style="padding:10px" width="200">
  <br>
  <a href="https://github.com/Souvik606/SARDS/releases">
    <img src="https://img.shields.io/badge/0.0.4-teal?label=version" alt="Version">
  </a>
  <a href="https://github.com/Souvik606/SARDS/issues">
    <img src="https://img.shields.io/github/issues/Souvik606/SARDS" alt="Issues">
  </a>
  <a href="https://github.com/Souvik606/SARDS">
    <img src="https://img.shields.io/github/stars/Souvik606/SARDS" alt="GitHub Stars">
  </a>
</div>

# SARDS: A Custom Language Made with Python

SARDS is a custom programming language built with Python. It combines a powerful **Lexer**,
**Parser**, and **Interpreter** to process and execute code written in our bespoke language. In
addition, SARDS offers an **Interactive Shell** for real-time coding, a **REST API** for remote
execution and parsing, and a modern **Web Frontend** to enhance your development experience.

---

[//]: # ([![Tests]&#40;https://github.com/Souvik^06/SARDS/actions/workflows/run-tests.yml/badge.svg&#41;]&#40;https://github.com/Souvik^06/SARDS/actions/workflows/run-tests.yml&#41;)

[//]: # ([![Builds]&#40;https://github.com/Souvik^06/SARDS/actions/workflows/builds.yml/badge.svg&#41;]&#40;https://github.com/Souvik^06/SARDS/actions/workflows/builds.yml&#41;)
[![Pylint](https://github.com/Souvik606/SARDS/actions/workflows/pylint.yml/badge.svg)](https://github.com/Souvik606/SARDS/actions/workflows/pylint.yml)
---

## 🚀 Features

- **🖥️ Interactive Shell**: A REPL to write and execute SARDS code on the fly.
- **📜 Custom Language Support**: Implements language constructs like **switch-case**, **if**, **while**, and more.
- **🌐 REST API**: Exposes endpoints to execute code and retrieve its AST remotely.
- **💻 Web Frontend**: A sleek, interactive UI for editing and running SARDS programs.

---

## 📋 Table of Contents

  - [✅ Prerequisites](#-prerequisites)
  - [⚙️ Setup](#️-setup)
  - [🛠️ Environment Variables](#️-environment-variables)
  - [🌐 API Endpoints](#-api-endpoints)
  - [📌 Usage](#-usage)
  - [🛠️ Technologies Used](#️-technologies-used)
  - [📜 License](#-license)
  - [🤝 Contributing](#-contributing)

---

## ✅ Prerequisites

- [Python](https://www.python.org/) (v3.10 or higher)
- [Node.js](https://nodejs.org/) (v20 or higher) – required for the frontend
- [Git](https://git-scm.com/)

---

## ⚙️ Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Souvik606/SARDS.git
   cd SARDS
   ```

2. **Language Setup:**

   we have no dependencies for the language. you just need python to run it.

3. **Frontend Setup:**
    - Navigate to the `frontend/` directory and install Node dependencies:
      ```bash
      cd frontend
      npm install
      cd ..
      ```

4. **Run the Interactive Shell:**
   ```bash
   python -m sards.shell
   ```

5. **Run a SARDS Program:**
   ```bash
   python -m sards.main hello.sard
   ```

6. **Run the API Server:**
    - Navigate to the `backend/` directory and start the server:
      ```bash
      cd backend
      python app.py
      ```

7. **Run the Frontend:**
    - Start the frontend development server:
      ```bash
      cd frontend
      npm start
      ```

---

## 🛠️ Environment Variables

For the API server and frontend, create a `.env` file in the `backend/` and `/frontend` directories with your
configuration settings provided in the `.env.example` files. For example:


---

## 🌐 API Endpoints

### Code Execution

#### **POST** `/api/execute`

- **Description**: Executes a SARDS code snippet.
- **Request Body:**
  ```json
  {
    "code": "menu a { choice 1 { show(\"Hello\") } fallback { show(\"World\") } }"
  }
  ```
- **Response**: Returns the result of the code execution.

#### **POST** `/api/parse`

- **Description**: Parses a SARDS code snippet and returns its Abstract Syntax Tree (AST).
- **Request Body:**
  ```json
  {
    "code": "menu a { choice 1 { show(\"Hello\") } fallback { show(\"World\") } }"
  }
  ```
- **Response**: Returns the AST representation of the code.

---

## 📌 Usage

### Running the Interactive Shell

Launch the shell to interactively write and run SARDS code:

```bash
python -m sards.shell
```

### Running a SARDS Program from File

Execute a SARDS program (e.g., `hello.sard`) by running:

```bash
python -m sards.main hello.sard
```

### Using the API

- **Execute Code**:
  ```bash
  curl -X POST http://localhost:8000/api/execute \
  -H "Content-Type: application/json" \
  -d '{"code": "menu a { choice 1 { show(\"Hello\") } fallback { show(\"World\") } }"}'
  ```

- **Parse Code**:
  ```bash
  curl -X POST http://localhost:8000/api/parse \
  -H "Content-Type: application/json" \
  -d '{"code": "menu a { choice 1 { show(\"Hello\") } fallback { show(\"World\") } }"}'
  ```

---

## 🛠️ Technologies Used

- **Python**: Core interpreter and backend logic.
- **Flask/FastAPI**: (Choose one) for building the REST API.
- **React**: (Or your preferred framework) for the web frontend.
- **Docker** (Optional): For containerizing the application.

---

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

Contributions are welcome! Please read
our [Contributing Guidelines](CONTRIBUTING.md) to get started.
