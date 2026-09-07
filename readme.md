# 🔎 Laptop Search Engine

A beginner-friendly Python project that teaches you the **`os` module** by
building a real file-search tool — no extra libraries needed.

---

## 📁 File Structure

```
LaptopSearchEngine/
├── main.py       ← Run this. Shows the menu and calls scanner functions.
├── scanner.py    ← All the os-module logic lives here (read this to learn!).
└── README.md     ← You are here.
```

---

## 🚀 How to Run

```bash
python main.py
```

That's it. No installs, no virtual environments — just plain Python.

---

## 🧠 What You Learn (os module concepts)

| Function | What it does |
|---|---|
| `os.getcwd()` | Returns the folder your script is currently running from |
| `os.listdir(path)` | Lists all names (files + folders) inside a folder |
| `os.path.join(a, b)` | Safely combines two path parts → no manual `/` needed |
| `os.path.exists(path)` | Checks if a file or folder actually exists |
| `os.path.isfile(path)` | True if the path is a file |
| `os.path.isdir(path)` | True if the path is a folder |
| `os.walk(root)` | Deep-crawls every sub-folder automatically |
| `os.path.getsize(path)` | Returns file size in bytes |
| `os.path.splitext(name)` | Splits `"file.txt"` → `("file", ".txt")` |
| `os.path.basename(path)` | Extracts just the name from a full path |
| `os.path.expanduser("~")` | Converts `~` to your real home directory |
| `os.name` | `'nt'` on Windows, `'posix'` on Linux/macOS |
| `os.sep` | Path separator: `\` on Windows, `/` on Linux/macOS |
| `os.environ` | Dict of all environment variables (HOME, USER, PATH …) |

---

## 🎮 Menu Options

```
[1]  📍  Where am I?            → os.getcwd()
[2]  📂  List a folder          → os.listdir()
[3]  🔍  Search files by name   → os.walk()
[4]  📄  Search by extension    → os.path.splitext()
[5]  💻  System info            → os.environ, os.name
[0]  🚪  Exit
```

---

## 💡 Beginner Tips

- **Every lesson is a function** in `scanner.py` — read the comments inside each one.
- Start with option `[1]` and `[2]` before trying the deep search.
- For options `[3]` and `[4]`, try your **Desktop** or **Documents** folder as the root.
- `os.walk()` is the most powerful tool here — once you understand it, you can
  build your own file manager, duplicate finder, or backup tool.

---

## 🔧 Extend the Project (ideas for Phase 2)

- [ ] Search files **larger than** a given size using `os.path.getsize()`
- [ ] Sort results by size or name
- [ ] Count total files and total size in a folder tree
- [ ] Find **duplicate** files by comparing sizes
- [ ] Export results to a `.txt` file using `open()`

---

*Built with nothing but Python's built-in `os` module — proof that the
standard library is already powerful.*