"""
scanner.py — The heart of LaptopSearchEngine
Teaches you how the `os` module lets Python talk to your file system.
"""

import os


# ─────────────────────────────────────────────
#  LESSON 1 — Where am I right now?
# ─────────────────────────────────────────────
def get_current_location():
    """os.getcwd() → returns the folder your script is running from."""
    return os.getcwd()


# ─────────────────────────────────────────────
#  LESSON 2 — What's inside a folder?
# ─────────────────────────────────────────────
def list_folder(path):
    """
    os.listdir(path) → returns a plain list of names (files + folders).
    os.path.join()   → safely glues a folder path + a name together.
    os.path.isfile() → True if the path points to a file (not a folder).
    os.path.isdir()  → True if the path points to a folder.
    """
    results = {"files": [], "folders": []}

    if not os.path.exists(path):          # os.path.exists() — does it exist?
        print(f"  ✗ Path not found: {path}")
        return results

    for name in os.listdir(path):
        full_path = os.path.join(path, name)   # never use path + "/" + name
        if os.path.isfile(full_path):
            results["files"].append(full_path)
        elif os.path.isdir(full_path):
            results["folders"].append(full_path)

    return results


# ─────────────────────────────────────────────
#  LESSON 3 — Deep search with os.walk()
# ─────────────────────────────────────────────
def search_by_name(root_path, keyword):
    """
    os.walk(root) → the magic tool for deep searching.
    Each step gives you:
        root   — the current folder being visited
        dirs   — list of sub-folder names inside root
        files  — list of file names inside root

    We use it to crawl every sub-folder automatically.
    """
    matches = []
    keyword = keyword.lower()

    print(f"\n  🔍 Searching inside: {root_path}")
    print(f"     Looking for: '{keyword}'\n")

    for root, dirs, files in os.walk(root_path):
        # Skip hidden folders (start with ".")
        dirs[:] = [d for d in dirs if not d.startswith(".")]

        for file_name in files:
            if keyword in file_name.lower():
                full_path = os.path.join(root, file_name)
                size_kb   = os.path.getsize(full_path) / 1024   # size in KB
                matches.append({
                    "name": file_name,
                    "path": full_path,
                    "size": f"{size_kb:.1f} KB"
                })

    return matches


# ─────────────────────────────────────────────
#  LESSON 4 — Search by file extension
# ─────────────────────────────────────────────
def search_by_extension(root_path, extension):
    """
    os.path.splitext(filename) → splits "notes.txt" into ("notes", ".txt")
    Great for filtering by file type.
    """
    matches = []
    extension = extension.lower()
    if not extension.startswith("."):
        extension = "." + extension      # make sure it looks like  .pdf  .mp3

    print(f"\n  🔍 Scanning for *{extension} files in: {root_path}\n")

    for root, dirs, files in os.walk(root_path):
        dirs[:] = [d for d in dirs if not d.startswith(".")]

        for file_name in files:
            _, ext = os.path.splitext(file_name)   # split name + extension
            if ext.lower() == extension:
                full_path = os.path.join(root, file_name)
                size_kb   = os.path.getsize(full_path) / 1024
                matches.append({
                    "name": file_name,
                    "path": full_path,
                    "size": f"{size_kb:.1f} KB"
                })

    return matches


# ─────────────────────────────────────────────
#  LESSON 5 — System info with os
# ─────────────────────────────────────────────
def get_system_info():
    """
    os.name     → 'nt' on Windows, 'posix' on Linux/macOS
    os.environ  → dict of all environment variables (PATH, HOME, USER …)
    os.sep      → the folder separator ('\\' on Windows, '/' on Linux/Mac)
    """
    info = {
        "OS type"      : "Windows" if os.name == "nt" else "Linux / macOS",
        "Path separator": os.sep,
        "Home folder"  : os.environ.get("HOME") or os.environ.get("USERPROFILE", "N/A"),
        "Username"     : os.environ.get("USER")  or os.environ.get("USERNAME",   "N/A"),
    }
    return info