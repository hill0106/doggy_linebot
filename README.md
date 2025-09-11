## Doggy Line Bot

A Python/Flask web service integrated with the LINE Messaging API to help pet owners manage pet info and quickly find pet-related resources (shelters, stores, hospitals, and a pet dictionary). The bot persists data in AWS DynamoDB and stores images in Azure Blob Storage. A simple web UI is provided via Flask templates for adding/editing/viewing pets.

### Highlights
- **LINE chatbot**: Conversational interface for pet utilities and quick actions
- **Pet management**: Add, edit, view pet profiles (with image upload)
- **Pet resources**: Browse shelters, stores, hospitals, dictionary pages
- **Cloud-native storage**: Data in **AWS DynamoDB**, images in **Azure Blob Storage**
- **Web UI**: Flask + Jinja templates served from the app

---

### Tech Stack
- **Language**: Python 3.9
- **Framework**: Flask
- **Messaging**: LINE Messaging API (Webhook + Reply/Push)
- **Database**: AWS DynamoDB
- **Object Storage**: Azure Blob Storage
- **Templating**: Jinja2 (Flask templates in `templates/`)
- **Static Assets**: Served from `static/` (images, CSS)
- **Environment**: `venv` (included) and dependencies pinned in `requirements.txt`

---

### Architecture Overview
- `application.py`: Flask app entrypoint; serves web pages and integrates endpoints
- `line_bot.py`: LINE webhook and bot message handling
- `line_chatbot_api.py`: Abstractions/helpers for bot flows and replies
- `dynamoDB.py`: DynamoDB CRUD wrapper for pet data
- `azure_blob.py`: Azure Blob Storage utilities (upload, URL generation)
- `templates/`: Jinja2 HTML templates for pages (add/edit/view, resources)
- `static/`: CSS and images (e.g., `static/images/doggy-menu.png`)

Data flow (high level):
1) LINE user sends message → webhook (`line_bot.py`) parses intent → replies via LINE API
2) Pet data is read/written via `dynamoDB.py`
3) Image uploads go to Azure Blob via `azure_blob.py`, persisted URL stored with pet
4) Flask serves UI pages for owners to manage content

---

### Features
- **Add/Edit Pet**: Create and update pet profiles with metadata and image
- **All Pets View**: List/query stored pet profiles
- **Resource Pages**: Prebuilt pages for shelters, pet stores, hospitals, and a dictionary
- **LINE Chatbot**: Menu-driven or keyword-triggered interactions

Key templates:
- `templates/add_pet.html`, `templates/edit_pet.html`, `templates/all_dog_info.html`
- `templates/pet_shelter.html`, `templates/pet_store.html`, `templates/pet_hospital.html`, `templates/dic.html`

---

### Getting Started

Prerequisites:
- Python 3.9+
- LINE Developer account (channel secret + access token)
- AWS credentials/permissions for DynamoDB
- Azure Storage account + Blob container for images

Install dependencies (recommended: use the provided venv or create your own):
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Environment variables (example):
```bash
export LINE_CHANNEL_SECRET=...           # from LINE Developers
export LINE_CHANNEL_ACCESS_TOKEN=...

export AWS_REGION=...
export DYNAMODB_TABLE=...                # pets table name
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...

export AZURE_STORAGE_CONNECTION_STRING=...
export AZURE_BLOB_CONTAINER=...
```

Run locally:
```bash
source venv/bin/activate
flask --app application.py run --debug
```

Expose webhook during development (choose one):
- **ngrok**: `ngrok http 5000`
- **Cloud tunnel** of your choice

Set the LINE webhook URL to: `https://<your-tunnel-domain>/callback` (adjust if your route differs in `line_bot.py`).

---

### Project Structure
```text
doggy_linebot/
  application.py           # Flask app entry
  line_bot.py              # LINE webhook and handlers
  line_chatbot_api.py      # Reply/flow helpers
  dynamoDB.py              # DynamoDB access layer
  azure_blob.py            # Azure Blob utils
  templates/               # Jinja2 templates (UI pages)
  static/                  # CSS, images
  requirements.txt         # Python deps
```

---

### Notable Endpoints
Note: Exact paths may vary depending on `application.py` routing.
- `GET /` or `/pets` – list/view pets
- `GET /pets/add` – add pet form
- `POST /pets` – create pet (uploads to Azure, writes to DynamoDB)
- `GET /pets/<id>/edit` – edit form
- `POST/PUT /pets/<id>` – update pet
- `POST /callback` – LINE webhook endpoint

---

### Screenshots
You can use the existing image in the repo for documentation or README previews:
`static/images/doggy-menu.png`

---

### Development Notes
- Keep secrets in environment variables; do not commit them
- Use separate AWS/Azure resources per environment
- Validate file uploads and sanitize user input

---

### License
This repository is for educational use. Add a license if you plan to distribute.

---



