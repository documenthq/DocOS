# filesystem.py
import os
import json
from datetime import datetime

FS_FILE = "document_fs.json"

class DocumentFS:
    def __init__(self):
        self.cwd = "/"
        self.todos = []
        self.notes = []
        self.contacts = {}
        
        if os.path.exists(FS_FILE):
            try:
                with open(FS_FILE, "r") as f:
                    data = json.load(f)
                    self.files = data.get("files", {})
                    self.todos = data.get("todos", [])
                    self.notes = data.get("notes", [])
                    self.contacts = data.get("contacts", {})
            except:
                self.create_default_fs()
        else:
            self.create_default_fs()

    def create_default_fs(self):
        self.files = {
            "/": {"type": "dir", "children": ["home", "bin", "documents", "readme.txt"]},
            "/home": {"type": "dir", "children": ["user"]},
            "/home/user": {"type": "dir", "children": ["welcome.txt"]},
            "/bin": {"type": "dir", "children": []},
            "/documents": {"type": "dir", "children": ["about.txt"]},
            "/readme.txt": {"type": "file", "content": "Welcome to Document OS 1.0"},
            "/home/user/welcome.txt": {"type": "file", "content": "All business data is saved permanently."},
            "/documents/about.txt": {"type": "file", "content": "Document OS 1.0\nOfficial Operating System"}
        }

    def save(self):
        try:
            data = {
                "files": self.files,
                "todos": self.todos,
                "notes": self.notes,
                "contacts": self.contacts
            }
            with open(FS_FILE, "w") as f:
                json.dump(data, f, indent=2)
        except:
            pass

    def resolve_path(self, path):
        if path.startswith("/"):
            return os.path.normpath(path).replace("\\", "/")
        return os.path.normpath(os.path.join(self.cwd, path)).replace("\\", "/")

    # All file system methods (files_cmd, goto, makedir, create, delete, read, write, etc.)
    def files_cmd(self, path=None):
        p = self.resolve_path(path) if path else self.cwd
        if p in self.files and self.files[p]["type"] == "dir":
            return self.files[p].get("children", [])
        return ["No such directory"]

    def goto(self, path):
        if path == "..":
            self.cwd = "/".join(self.cwd.split("/")[:-1]) or "/"
            return
        new_path = self.resolve_path(path)
        if new_path in self.files and self.files[new_path]["type"] == "dir":
            self.cwd = new_path
        else:
            print(f"goto: no such directory: {path}")

    def makedir(self, name):
        full = self.resolve_path(name)
        if full in self.files:
            print("makedir: directory already exists")
            return
        self.files[full] = {"type": "dir", "children": []}
        parent = os.path.dirname(full) or "/"
        if parent in self.files:
            children = self.files[parent].setdefault("children", [])
            if os.path.basename(full) not in children:
                children.append(os.path.basename(full))
        self.save()
        print(f"Directory created: {name}")

    def create(self, name):
        full = self.resolve_path(name)
        self.files[full] = {"type": "file", "content": ""}
        parent = os.path.dirname(full) or "/"
        if parent in self.files:
            children = self.files[parent].setdefault("children", [])
            if os.path.basename(full) not in children:
                children.append(os.path.basename(full))
        self.save()
        print(f"File created: {name}")

    def delete(self, name):
        full = self.resolve_path(name)
        if full in self.files:
            del self.files[full]
            parent = os.path.dirname(full) or "/"
            if parent in self.files and "children" in self.files[parent]:
                if os.path.basename(full) in self.files[parent]["children"]:
                    self.files[parent]["children"].remove(os.path.basename(full))
            self.save()
            print(f"Deleted: {name}")
        else:
            print(f"delete: cannot remove '{name}': No such file or directory")

    def read(self, path):
        full = self.resolve_path(path)
        if full in self.files and self.files[full]["type"] == "file":
            print(self.files[full]["content"])
        else:
            print("read: file not found")

    def write(self, text, file):
        full = self.resolve_path(file)
        self.files[full] = {"type": "file", "content": text}
        parent = os.path.dirname(full) or "/"
        if parent in self.files:
            children = self.files[parent].setdefault("children", [])
            if os.path.basename(full) not in children:
                children.append(os.path.basename(full))
        self.save()
        print(f"Saved to {file}")

    def copy(self, source, dest):
        src = self.resolve_path(source)
        dst = self.resolve_path(dest)
        if src in self.files and self.files[src]["type"] == "file":
            self.files[dst] = self.files[src].copy()
            parent = os.path.dirname(dst) or "/"
            if parent in self.files:
                children = self.files[parent].setdefault("children", [])
                if os.path.basename(dst) not in children:
                    children.append(os.path.basename(dst))
            self.save()
            print(f"Copied {source} to {dest}")
        else:
            print("copy: source file not found")

    def rename(self, old, new):
        old_path = self.resolve_path(old)
        new_path = self.resolve_path(new)
        if old_path in self.files:
            self.files[new_path] = self.files.pop(old_path)
            old_parent = os.path.dirname(old_path) or "/"
            new_parent = os.path.dirname(new_path) or "/"
            if old_parent in self.files and "children" in self.files[old_parent]:
                if os.path.basename(old_path) in self.files[old_parent]["children"]:
                    self.files[old_parent]["children"].remove(os.path.basename(old_path))
            if new_parent in self.files:
                children = self.files[new_parent].setdefault("children", [])
                if os.path.basename(new_path) not in children:
                    children.append(os.path.basename(new_path))
            self.save()
            print(f"Renamed {old} to {new}")
        else:
            print("rename: file or directory not found")

    def tree(self, path=None, prefix=""):
        p = self.resolve_path(path) if path else self.cwd
        if p not in self.files or self.files[p]["type"] != "dir":
            print("tree: not a directory")
            return
        print(prefix + (os.path.basename(p) if p != "/" else "/"))
        children = sorted(self.files[p].get("children", []))
        for i, child in enumerate(children):
            child_path = os.path.join(p, child).replace("\\", "/")
            is_last = i == len(children) - 1
            if child_path in self.files and self.files[child_path]["type"] == "dir":
                self.tree(child_path, prefix + ("    " if is_last else "│   "))
            else:
                print(prefix + ("└── " if is_last else "├── ") + child)

    def size(self, name):
        full = self.resolve_path(name)
        if full in self.files and self.files[full]["type"] == "file":
            size = len(self.files[full]["content"].encode('utf-8'))
            print(f"{name}: {size} bytes")
        else:
            print("size: file not found")

    def edit(self, name):
        full = self.resolve_path(name)
        if full not in self.files or self.files[full]["type"] != "file":
            print("edit: file not found. Create it first with 'create'")
            return
        print(f"\n--- Editing {name} ---")
        print("Current content:\n")
        print(self.files[full]["content"])
        print("\nEnter new content (type 'END' on a new line to save):\n")
        lines = []
        while True:
            line = input()
            if line == "END":
                break
            lines.append(line)
        self.files[full]["content"] = "\n".join(lines)
        self.save()
        print(f"File {name} saved.")