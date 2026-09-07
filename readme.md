# 🔎 LaptopSearchEngine — Flask Edition

A full-stack file-search web app built with **Python + Flask + vanilla JS**.
The backend uses the `os` module; the frontend talks to it via REST API calls.

---

## 📁 Project Structure

```
LaptopSearchEngine/
│
├── app.py              ← Flask server  (API routes)
├── scanner.py          ← os-module logic  (unchanged from Phase 1)
│
├── templates/
│   └── index.html      ← HTML page served by Flask
│
├── static/
│   ├── css/style.css   ← Styling
│   └── js/app.js       ← fetch() calls to Flask API
│
└── README.md
```

---

## 🚀 Setup & Run

```bash
# 1. Install Flask (one-time)
pip install flask

# 2. Run the server
python app.py

# 3. Open your browser
http://127.0.0.1:5000
```

---

## 🔗 How Flask Connects Everything

```
Browser (index.html + app.js)
    │
    │  fetch("/api/search/name", { body: { path, keyword } })
    ▼
Flask (app.py)  →  calls scanner.py  →  os.walk(path)
    │
    │  returns JSON  { success: true, results: [...] }
    ▼
app.js builds HTML cards and injects them into the page
```

---

## 🌐 API Routes

| Method | Route | What it does |
|--------|-------|--------------|
| GET  | `/`                    | Serves the HTML frontend |
| GET  | `/api/location`        | Returns `os.getcwd()` |
| GET  | `/api/sysinfo`         | Returns `os.name`, `os.environ` info |
| POST | `/api/list`            | `os.listdir()` for a given path |
| POST | `/api/search/name`     | `os.walk()` search by keyword |
| POST | `/api/search/extension`| `os.walk()` + `splitext()` search |

---

## 🧠 What You Learn

- How Flask routes work (`@app.route`)
- How to return JSON from Flask (`jsonify`)
- How to call your own Python module from Flask
- How the browser fetches JSON from a server (`fetch` API)
- How to build HTML dynamically from JSON responses

---

*Phase 1 taught the `os` module. Phase 2 connects it to the web.*