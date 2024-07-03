# project-aopse

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

## Setup

The backend requires that you correctly fill out the [`config.yaml`](./aopse-backend/config.yaml) in the `aopse-backend` folder with the following content:

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
   3. The frontend can be reached under <localhist:5173>
3. Execute the `create-venv.sh` script in the root of the repository, this will create a virtual python environment for the project
   1. Activate the environment by using `source ./aopse-backend/bin/activate`
4. Open the `aopse-backend` folder
   1. Run the `scripts.sh` using `scripts.sh load`, to install all dependencies
   2. Run the backend using `fastapi run`

### Extensions

You can use the [Svelte DevTools](https://chromewebstore.google.com/detail/kfidecgcdjjfpeckbblhmfkhmlgecoff) 
extension for your browser. 

And the [Svelte](https://plugins.jetbrains.com/plugin/12375-svelte) extension for JetBrains IDEs.
