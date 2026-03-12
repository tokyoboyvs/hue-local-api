# hue-local-api

Mini API REST en Python avec FastAPI pour piloter des lumières Philips Hue.

## Features

- health check
- liste des lumières
- détail d'une lumière
- on / off / toggle
- mise à jour de la luminosité
- mise à jour de la couleur
- liste des rooms
- liste des lumières par room
- mode mock
- protection API par clé

## Stack

- Python
- FastAPI
- Uvicorn
- Pydantic
- Pytest
- httpx

## Project structure

```text
app/
  routes/
  services/
  utils/
tests/
run.py
requirements.txt
```

## Environment variables

- `APP_MODE`: mode de l'application, `mock` ou `real`
- `HUE_BRIDGE_IP`: adresse IP du Hue Bridge
- `HUE_APP_KEY`: clé d'application du Hue Bridge
- `API_KEY`: clé attendue dans le header `X-API-Key`

```env
APP_MODE=mock
HUE_BRIDGE_IP=
HUE_APP_KEY=
API_KEY=dev-key
```

## Run locally

```bash
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
py run.py
```

## Authentication

Toutes les routes `/api/...` demandent le header `X-API-Key`.

La route `/health` reste publique.

```bash
curl -X GET "http://127.0.0.1:8000/api/lights" -H "accept: application/json" -H "X-API-Key: dev-key"
```

## Available endpoints

- `GET /health`
- `GET /api/lights`
- `GET /api/lights/{light_id}`
- `POST /api/lights/{light_id}/on`
- `POST /api/lights/{light_id}/off`
- `POST /api/lights/{light_id}/toggle`
- `POST /api/lights/{light_id}/brightness`
- `POST /api/lights/{light_id}/color`
- `GET /api/lights/bridge/status`
- `GET /api/rooms`
- `GET /api/rooms/{room_name}/lights`

## Example payloads

```json
{ "brightness": 20 }
```

```json
{ "color": "#00FFAA" }
```

## Tests

```bash
pytest
```

## Current status

Le mode mock est fonctionnel.

Le client réel Hue est préparé, mais l'intégration complète avec un vrai Hue Bridge reste à finaliser.

## Next steps

- intégration réelle du Hue Bridge
- actions groupées
- gestion avancée des rooms
- refactor du service layer si nécessaire
