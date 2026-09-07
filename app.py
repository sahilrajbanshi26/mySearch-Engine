"""
app.py — Flask backend for LaptopSearchEngine
Connects scanner.py functions to the web frontend via REST API routes.

Run:  python app.py
Open: http://127.0.0.1:5000
"""

from flask import Flask, render_template, request, jsonify
import scanner   # our own scanner.py
import os

app = Flask(__name__, static_folder="statistic", static_url_path="/static")


# ─────────────────────────────────────────────────────────
#  PAGE ROUTE — serves the HTML frontend
# ─────────────────────────────────────────────────────────

@app.route("/")
def index():
    """Render the main search-engine page."""
    return render_template("index.html")


# ─────────────────────────────────────────────────────────
#  API ROUTES — called by JavaScript fetch() in the browser
#  All return JSON so the frontend can display the results.
# ─────────────────────────────────────────────────────────

@app.route("/api/location", methods=["GET"])
def api_location():
    """Return the current working directory."""
    try:
        path = scanner.get_current_location()
        return jsonify({"success": True, "path": path})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/sysinfo", methods=["GET"])
def api_sysinfo():
    """Return OS / environment information."""
    try:
        info = scanner.get_system_info()
        return jsonify({"success": True, "info": info})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/list", methods=["POST"])
def api_list():
    """
    List the contents of a given folder.
    Expects JSON body: { "path": "/some/folder" }
    """
    data = request.get_json()
    path = data.get("path", "").strip()

    if not path:
        return jsonify({"success": False, "error": "No path provided."}), 400

    path = os.path.expanduser(path)   # handle  ~  shorthand

    try:
        result = scanner.list_folder(path)
        # Add basename for cleaner display in the UI
        files   = [{"name": os.path.basename(f), "full": f} for f in result["files"]]
        folders = [{"name": os.path.basename(f), "full": f} for f in result["folders"]]
        return jsonify({"success": True, "files": files, "folders": folders})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/search/name", methods=["POST"])
def api_search_name():
    """
    Deep-search for files whose name contains a keyword.
    Expects JSON body: { "path": "/some/folder", "keyword": "resume" }
    """
    data    = request.get_json()
    path    = os.path.expanduser(data.get("path", "").strip())
    keyword = data.get("keyword", "").strip()

    if not path or not keyword:
        return jsonify({"success": False, "error": "Path and keyword are required."}), 400

    try:
        results = scanner.search_by_name(path, keyword)
        return jsonify({"success": True, "results": results, "count": len(results)})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/search/extension", methods=["POST"])
def api_search_extension():
    """
    Deep-search for files matching a given extension.
    Expects JSON body: { "path": "/some/folder", "extension": "pdf" }
    """
    data      = request.get_json()
    path      = os.path.expanduser(data.get("path", "").strip())
    extension = data.get("extension", "").strip()

    if not path or not extension:
        return jsonify({"success": False, "error": "Path and extension are required."}), 400

    try:
        results = scanner.search_by_extension(path, extension)
        return jsonify({"success": True, "results": results, "count": len(results)})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ─────────────────────────────────────────────────────────
#  START THE SERVER
# ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n  🔎  LaptopSearchEngine is running!")
    print("  👉  Open your browser at:  http://127.0.0.1:5000\n")
    app.run(debug=True)