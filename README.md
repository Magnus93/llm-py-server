
## Installing dependencies
```bash
pip install -r requirements.txt
```


## Running Open WebUI

### Stopping and removing the old container

> Only needed if you want to recreate the container (e.g., change environment variables or network settings).
```bash
sudo docker stop open-webui
sudo docker rm open-webui
```
- stop → stops the running container
- rm → removes the container (the mounted volume keeps your data, so history and logins aren’t lost)



### Creating a new Open WebUI container

```bash
sudo docker run -d \
  --network host \
  -v open-webui:/app/backend/data \
  -e OLLAMA_BASE_URL=http://127.0.0.1:11434 \
  --name open-webui \
  ghcr.io/open-webui/open-webui:main
```
`-d` Run detached (in the background)
`--network host` - Makes the container use your host’s network so it can reach your local Ollama API at `127.0.0.1:11434` (Linux only).
`-v open-webui:/app/backend/data` - Mount a persistent volume so **login info and chat history** survive container recreation
`-e OLLAMA_BASE_URL=http://127.0.0.1:11434` - Tell Open WebUI where to find your local Ollama API
`--name open-webui` - Give the container a human-readable name for easier management (`docker stop open-webui`, `docker logs open-webui`, etc.)
`ghcr.io/open-webui/open-webui:main` - The Docker image to run (latest Open WebUI release)


Switch to this to use the py-server as proxy.
```bash
sudo docker run -d \
  --network host \
  -v open-webui:/app/backend/data \
  -e OLLAMA_BASE_URL=http://127.0.0.1:8000 \
  --name open-webui \
  ghcr.io/open-webui/open-webui:main
```

After this, Open WebUI will be accessible at `http://localhost:8080`

### .env
Add `.env` file:
```ini
OLLAMA_BASE_URL=<URL and PORT where ollama model is hosted>

BRAVE_BASE_URL="https://api.search.brave.com"
BRAVE_API_KEY=<Valid Brave API Key>
```