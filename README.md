# Private Skills Platform

_A Proof of Concept developed during my internship at Cleverse._

This repository contains a proof of concept for **Private Skills**, developed during my internship project at Cleverse.

The goal of this project is to explore how AI-powered skills can be provided to clients without exposing proprietary prompts or implementation details.

The current prototype demonstrates an **Employment Contract Reviewer** built on top of a Gateway and Protected Skill architecture.

---

## Overview

In a typical AI application, prompts and business logic are often embedded inside the application itself. This makes it difficult to protect proprietary prompts when distributing AI features.

This project explores a different approach by separating responsibilities into three components:

- Frontend
- Gateway
- Protected Skill Service

The frontend communicates only with the Gateway, while the Gateway forwards requests to the Protected Skill Service. The confidential system prompt remains inside the Protected Skill Service and is never exposed to the client.

Instead of returning raw LLM responses, the service returns structured editing instructions that can be applied by the frontend.

---

## Current Features

- Employment contract review using Claude
- Gateway for request routing
- Protected Skill Service containing confidential prompts
- Structured output using Tool Calling
- Interactive review interface
- Apply / Dismiss suggested edits
- Separation between frontend, gateway, and AI implementation

---

## System Architecture

```
                +----------------------+
                |      Frontend        |
                | Embedded Review UI   |
                +----------+-----------+
                           |
                     POST /chat
                           |
                           ▼
                +----------------------+
                |       Gateway        |
                | Routing & Validation |
                +----------+-----------+
                           |
                     POST /execute
                           |
                           ▼
          +--------------------------------+
          |  Protected Skill Service       |
          |                                |
          |  • Secret System Prompt        |
          |  • Business Logic              |
          |  • Claude Tool Calling         |
          +---------------+----------------+
                          |
                          ▼
                       Claude API
                          |
                          ▼
              Structured Edit Instructions
                          |
                          ▼
                  Embedded Review UI
```

---

## Project Structure

```
private-skills-poc/

├── gateway/
│
├── protected_skill_service/
│   ├── Protected Skill
│   ├── Prompt
│   └── Claude integration
│
├── prototypes/
│   ├── embedded-review-panel.html
│   ├── document.js
│   ├── suggestions.js
│   └── script.js
│
└── README.md
```

---

## How It Works

1. The user opens an employment contract.
2. The frontend sends the document to the Gateway.
3. The Gateway forwards the request to the Protected Skill Service.
4. The Protected Skill Service injects its internal system prompt.
5. Claude analyzes the document using Tool Calling.
6. The service returns structured edit instructions.
7. The frontend displays suggested edits.
8. The user can apply or dismiss each suggestion.

---

## Prompt Protection

One of the main goals of this project is to keep proprietary prompts private.

| Component               | Access to System Prompt |
| ----------------------- | ----------------------- |
| Frontend                | No                      |
| Gateway                 | No                      |
| Protected Skill Service | Yes                     |

The frontend only receives structured edit instructions.

The Gateway forwards requests without knowing how the AI generates those instructions.

The Protected Skill Service is the only component that contains the confidential prompt and business logic.

---

## Example Response

```json
{
  "instructions": [
    {
      "old_str": "...",
      "new_str": "...",
      "reason": "...",
      "priority": "high"
    }
  ]
}
```

---

## Running the Project

### Start Protected Skill Service

```bash
cd private-skills-poc/protected_skill_service
python -m uvicorn main:app --reload --port 8001
```

### Start Gateway

```bash
cd gateway
python -m uvicorn main:app --reload --port 8000
```

### Start Frontend

```bash
cd private-skills-poc/prototypes
python -m http.server 5500
```

Open:

```
http://127.0.0.1:5500/private-skills-poc/prototypes/embedded-review-panel.html
```

---

## Demo

The current prototype demonstrates the following workflow:

1. Open an employment contract.
2. Click **Analyze Document**.
3. Review AI-generated suggestions.
4. Apply or dismiss each suggestion.
5. The document is updated interactively.

---

## Technologies

**Frontend**

- HTML
- CSS
- JavaScript

**Backend**

- FastAPI
- Python

**AI**

- Claude
- Tool Calling

---

## Documentation

Additional design documents created during the internship can be found in the `docs/` directory, including:

- Problem Definition
- Requirements
- Use Cases
- System Context
- Architecture Design

---

## Future Work

Some ideas for future development include:

- PDF upload
- OCR support
- Multiple Private Skills
- Skill Registry
- Authentication
- Version history
- Audit logging

---

## Status

Current status:

- Research completed
- Architecture completed
- End-to-end prototype completed
- Interactive review interface completed

The current implementation focuses on validating the Private Skills architecture rather than building a production-ready document editor.
