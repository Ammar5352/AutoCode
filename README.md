# AutoCode AI 🚀

AutoCode is a powerful, full-stack Agentic AI web application. The system accepts user prompts or tasks and seamlessly communicates with an AI agent backend to process, generate, and execute code intelligence.

Link: https://auto-codeai.vercel.app/
## 🏗 System Architecture

The project is split into two seamlessly integrated environments:

- **Frontend (`/frontend`)**: A modern, lightning-fast user interface built with React, Vite, and TypeScript.
- **Backend (`/backend`)**: A highly performant and scalable API built with Python and FastAPI, serving as the AI agent orchestrator.

### 💻 Frontend (React + Vite + TypeScript)
- **Framework**: Built with React and optimized by Vite for instant Hot Module Replacement (HMR).
- **Type Safety**: Strictly typed with TypeScript for reliable code quality.
- **API Communication**: Utilizes an environment-driven configuration (matching `VITE_API_URL` to local or production backends) to securely pass tasks from the user to the agent.
- **Deployment**: Configured for edge deployment platforms like Vercel with automatic Vite integrations.

### 🧠 Backend (FastAPI + Agentic AI)
- **Framework**: Built on FastAPI, offering asynchronous support and native speed.
- **Routing Structure**: Modular API paths including the dedicated AI routing endpoint (`/autocodeai/autocode_agent`).
- **CORS Configuration**: Fully managed Cross-Origin Resource Sharing allowing seamless communication across distinct ports during development and cloud domains (like Vercel/Render) during production.
- **AI Agents Module**: Handles the complex logic of parsing user instructions. It operates using a sophisticated graph of specialist agents:
  - **PlannerAgent**: Analyzes the initial user request and breaks it down into a structured, actionable plan.
  - **ExecutorAgent**: Writes the code and executes the steps defined by the Planner.
  - **CodeReviewAgent**: Audits the Executor's output for bugs, security issues, and code quality.
  - **SupervisorAgent**: The orchestrator that evaluates the current state and decides whether to loop back for fixes or proceed.
  - **SummaryAgent**: Compiles a concise summary of all the operations performed.
  - **FeedbackAgent**: Processes errors or feedback to adjust and self-correct during the workflow.
  - **ResponseAgent**: Formats the final results and readies the payload to be sent back to the frontend.

## 🚀 Getting Started Locally

### 1. Backend Setup
1. Navigate to the root directory.
2. Activate your virtual environment (if not already active):
   ```bash
   source venv/bin/activate  # On Linux/Mac
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the FastAPI server (typically on port 8000/8081 depending on your setup):
   ```bash
   uvicorn backend.app:app --reload
   ```

### 2. Frontend Setup
1. Open a new terminal and navigate to the frontend folder:
   ```bash
   cd frontend
   ```
2. Install frontend packages:
   ```bash
   npm install
   ```
3. Start the Vite development server:
   ```bash
   npm run dev
   ```

## 🌍 Production Deployment

- **Backend**: Hosted on cloud platforms (e.g., Render) as a web service. 
- **Frontend**: Hosted on static site/edge platforms (e.g., Vercel). The frontend consumes the deployed backend URL using a defined `VITE_API_URL` environment variable to fetch data.

## 🛡 Features
- **Agentic Workflows**: Pass instructions to intelligent code agents that can reason about and execute sub-tasks.
- **Secure Types**: Shared API types between TypeScript and Python to ensure contract stability.
- **Developer Ready**: Comes heavily configured for immediate spin-up without boilerplate.
