"""
main.py — LaptopSearchEngine
Run this file to start the search engine.
"""

import os
import scanner   # importing our own scanner.py


# ── Helpers ────────────────────────────────────────────────────────────────────

def print_banner():
    print("""
╔══════════════════════════════════════╗
║       🔎  Laptop Search Engine       ║
║     Learn `os` module in action!     ║
╚══════════════════════════════════════╝
""")

def print_results(results):
    """Neatly display a list of file-match dicts."""
    if not results:
        print("\n  ⚠️  No files found.\n")
        return
    print(f"\n  ✅  Found {len(results)} file(s):\n")
    for i, item in enumerate(results, 1):
        print(f"  {i:>3}. {item['name']}")
        print(f"       📁 {item['path']}")
        print(f"       📦 {item['size']}\n")

def ask_path(prompt="  Enter folder path: "):
    """Ask for a path and expand '~' to the real home directory."""
    raw = input(prompt).strip()
    return os.path.expanduser(raw)   # os.path.expanduser turns ~ into /home/you


# ── Menu options ───────────────────────────────────────────────────────────────

def option_current_location():
    location = scanner.get_current_location()
    print(f"\n  📍 You are running this script from:\n     {location}\n")


def option_list_folder():
    path = ask_path("  Which folder do you want to peek inside? ")
    data = scanner.list_folder(path)

    print(f"\n  📂 Folders ({len(data['folders'])}):")
    for f in data["folders"]:
        print(f"     📁  {os.path.basename(f)}")   # os.path.basename strips the full path

    print(f"\n  📄 Files ({len(data['files'])}):")
    for f in data["files"]:
        print(f"     📄  {os.path.basename(f)}")
    print()


def option_search_by_name():
    path    = ask_path("  Root folder to search in: ")
    keyword = input("  File name keyword (e.g. resume, photo): ").strip()
    results = scanner.search_by_name(path, keyword)
    print_results(results)


def option_search_by_extension():
    path = ask_path("  Root folder to search in: ")
    ext  = input("  File extension (e.g. pdf, mp3, jpg): ").strip()
    results = scanner.search_by_extension(path, ext)
    print_results(results)


def option_system_info():
    info = scanner.get_system_info()
    print("\n  💻 System Information (from os module):\n")
    for key, value in info.items():
        print(f"     {key:<18} →  {value}")
    print()


# ── Main loop ──────────────────────────────────────────────────────────────────

MENU = {
    "1": ("📍  Where am I? (os.getcwd)",          option_current_location),
    "2": ("📂  List a folder (os.listdir)",        option_list_folder),
    "3": ("🔍  Search files by name (os.walk)",    option_search_by_name),
    "4": ("📄  Search by extension (splitext)",    option_search_by_extension),
    "5": ("💻  System info (os.environ / os.name)", option_system_info),
    "0": ("🚪  Exit",                              None),
}

def main():
    print_banner()

    while True:
        print("  ─── MENU ───────────────────────────────")
        for key, (label, _) in MENU.items():
            print(f"   [{key}]  {label}")
        print("  ─────────────────────────────────────────")

        choice = input("\n  Your choice: ").strip()

        if choice == "0":
            print("\n  👋  Bye! Keep exploring with `os`.\n")
            break
        elif choice in MENU:
            _, action = MENU[choice]
            action()
        else:
            print("\n  ❌  Invalid option. Try again.\n")


if __name__ == "__main__":
    main()