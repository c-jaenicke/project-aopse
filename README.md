# project-aopse

<p align="center">
   <img src="/documentation/logo/logo.png" alt="Logo" width="200">
</p>

AI-Driven OSINT People Search Engine

## Disclaimer

This tool and all scripts included should be used for educational purposes only. Any misuse of this software will not be
the responsibility of the author or of any other collaborator.

## Idea

Our project aims to enhance user privacy and online security by utilizing Open Source
Intelligence (OSINT) techniques, service breaches, and search engines. By leveraging
these tools, we can identify and address vulnerabilities, providing users with insights and
strategies to safeguard their personal data.
This proactive approach not only helps in mitigating potential risks but also empowers
users to take control of their online presence and protect their information

## Project Structure

The project is divided into two main parts: the frontend and the backend.
- The frontend is a Svelte application that communicates with the backend using a WebSocket connection.
- The backend is a FastAPI application that communicates with the frontend and various services.

### Backend Structure

The `app` directory contains the main application code, including:

- `main.py`: The main FastAPI application
- `models.py`: Pydantic models used for request and response validation
- `config.py`: Configuration file that loads settings from `config.yaml`

#### Routes
- `routes/`
  - `websocket.py`: Contains the WebSocket route

#### Services
- `services/`
  - `ai_service.py`: The core of the backend, containing most of the application logic

#### Storage
- `storage/`
  - `chroma_storage.py`: Manages data storage and retrieval from the Chroma database

#### Utils
- `utils/`
  - `account_checker.py`: Uses Sherlock to check for account existence across various platforms
  - `hibp.py`: Interfaces with the HaveIBeenPwned API to check for compromised emails
  - `tavily_search.py`: Implements internet search functionality using the Tavily API
  - `sherlock_search.py`: Sherlock implementation for username searches

#### Wordlists
- `wordlists/`: Contains wordlists stored in the Chroma database


## Setup

The backend requires that you correctly fill out the [`config.yaml`](./aopse-backend/config.yaml) in the `aopse-backend`
folder with the following content:

```yaml
aopse:
  default_provider: "openai"
  providers:
    openai:
      api_key: "<YOUR OPENAI API KEY HERE>"
      model: gpt-3.5-turbo
      assistant_id: ""  # Leave this empty, it will be filled on start
  tools:
    tavily:
      api_key: "<YOUR TAVIL API KEY HERE>"
    hibp:
      api_key: "<YOUR HAVEIBEENPWNED API KEY HERE>"
```

## Development Setup

1. Clone the project using git
2. Open the `aopse-frontend` folder
    1. Run `npm install` to install all frontend dependencies
    2. Run the frontend using `npm run dev`
    3. The frontend can be reached under [localhost:5173](http://localhost:5173)
3. Execute the `create-venv.sh` script in the root of the repository, this will create a virtual python environment for
   the project
    1. Activate the environment by using `source ./aopse-backend/bin/activate`
4. Open the `aopse-backend` folder
    1. Run the `scripts.sh` using `scripts.sh load`, to install all dependencies
    2. Run the backend using `fastapi run`

### Extensions

You can use the [Svelte DevTools](https://chromewebstore.google.com/detail/kfidecgcdjjfpeckbblhmfkhmlgecoff)
extension for your browser.

And the [Svelte](https://plugins.jetbrains.com/plugin/12375-svelte) extension for JetBrains IDEs.
