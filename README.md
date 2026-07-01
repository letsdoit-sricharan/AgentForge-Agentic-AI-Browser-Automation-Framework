# AgentForge

AgentForge is a production-grade Agentic AI Automation Framework capable of understanding natural language, planning complex workflows, and autonomously interacting with websites through browser automation.

## Project Structure

The repository is structured as a multi-container application:

```
AI_project/
├── .github/              # CI/CD Workflows
├── backend/              # FastAPI Application (Python)
│   ├── app/              # Core API Logic, Database, Models & Schemas
│   └── tests/            # Backend unit & integration tests
├── frontend/             # Next.js Application (TypeScript & TailwindCSS)
├── runtime/              # Agent Orchestration (Intent, Planning, Execution, State, etc.)
├── browser_engine/       # Isolated Playwright-based Browser Automation Layer
├── plugins/              # Independent Website Integrations
│   ├── sdk/              # Common SDK Interfaces for all plugins
│   └── bookmyshow/       # BookMyShow custom validation & workflow implementation
├── shared/               # Shared constants, config, exceptions, and logging
├── docker/               # Additional Docker utilities and configurations
├── docs/                 # System design and architecture documentation
└── scripts/              # Helper script utilities
```

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/)
- [Python 3.11+](https://www.python.org/) (for local backend development)
- [Node.js 18+](https://nodejs.org/) (for local frontend development)

### Quick Start with Docker Compose

1. Clone the repository and navigate to the directory:
   ```bash
   cd AI_project
   ```

2. Copy the environment variables:
   ```bash
   cp .env.example .env
   ```
   Modify `.env` to include your LLM provider API keys (e.g., `OPENAI_API_KEY`).

3. Start all services using Docker Compose:
   ```bash
   docker-compose up --build
   ```
   - Frontend is available at `http://localhost:3000`
   - Backend API is available at `http://localhost:8000`
   - PostgreSQL Database runs on port `5432`

## Documentation

For architectural and system design details, refer to:
- [PLATFORM_ARCHITECTURE.md](file:///e:/projrcts/AI_project/PLATFORM_ARCHITECTURE.md)
- [SYSTEM_DESIGN.md](file:///e:/projrcts/AI_project/SYSTEM_DESIGN.md)
- [AGENT_RUNTIME.md](file:///e:/projrcts/AI_project/AGENT_RUNTIME.md)
- [BROWSER_ENGINE.md](file:///e:/projrcts/AI_project/BROWSER_ENGINE.md)
- [PLUGIN_SDK.md](file:///e:/projrcts/AI_project/PLUGIN_SDK.md)
- [PROJECT_GUIDE.md](file:///e:/projrcts/AI_project/PROJECT_GUIDE.md)

## License

This project is licensed under the MIT License - see the [LICENSE](file:///e:/projrcts/AI_project/LICENSE) file for details.
