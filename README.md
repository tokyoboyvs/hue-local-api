# hue-local-api

Mini API REST en Python avec FastAPI pour piloter des lumieres Philips Hue.

## Features

- health check
- liste des lumieres
- detail d'une lumiere
- on / off / toggle
- mise a jour de la luminosite
- mise a jour de la couleur
- liste des rooms
- liste des lumieres par room
- mode mock
- protection API par cle

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
- `HUE_APP_KEY`: cle d'application du Hue Bridge
- `API_KEY`: cle attendue dans le header `X-API-Key`
- `APP_HOST`: host d'ecoute Uvicorn
- `APP_PORT`: port d'ecoute Uvicorn
- `APP_RELOAD`: active ou non le reload automatique

```env
APP_MODE=mock
HUE_BRIDGE_IP=
HUE_APP_KEY=
API_KEY=dev-key
APP_HOST=127.0.0.1
APP_PORT=8000
APP_RELOAD=true
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
{"brightness": 20}
```

```json
{"color": "#00FFAA"}
```

## Tests

```bash
pytest
```

## Current status

Le mode mock est fonctionnel.

Le client reel Hue est prepare, mais l'integration complete avec un vrai Hue Bridge reste a finaliser.

## Raspberry Pi notes

- utiliser `APP_RELOAD=false`
- exposer l'API sur `0.0.0.0`
- garder une IP locale stable pour le Raspberry Pi
- utiliser Docker ou un service systemd plus tard

```env
APP_HOST=0.0.0.0
APP_PORT=8000
APP_RELOAD=false
```

## Next steps

- integration reelle du Hue Bridge
- actions groupees
- gestion avancee des rooms
- refactor du service layer si necessaire
