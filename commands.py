# commands.py
from datetime import datetime

class CommandHandler:
    def __init__(self, fs):
        self.fs = fs

    def calc(self, expr):
        try:
            result = eval(expr, {"__builtins__": {}})
            print(f"Result: {result}")
        except:
            print("calc: Invalid expression")

    def todo(self, action, *args):
        if action == "add" and args:
            task = " ".join(args)
            self.fs.todos.append({"task": task, "done": False})
            self.fs.save()
            print(f"Task added: {task}")
        elif action == "list":
            if not self.fs.todos:
                print("No tasks.")
            else:
                for i, t in enumerate(self.fs.todos):
                    status = "✓" if t["done"] else " "
                    print(f"{i+1}. [{status}] {t['task']}")
        elif action == "done" and args:
            try:
                idx = int(args[0]) - 1
                self.fs.todos[idx]["done"] = True
                self.fs.save()
                print("Task marked as done.")
            except:
                print("Invalid task number")
        else:
            print("Usage: todo add <task> | todo list | todo done <number>")

    def note(self, *args):
        if args:
            note_text = " ".join(args)
            self.fs.notes.append({"time": datetime.now().strftime("%Y-%m-%d %H:%M"), "content": note_text})
            self.fs.save()
            print("Note saved.")
        else:
            print("Recent Notes:")
            for n in self.fs.notes[-5:]:
                print(f"[{n['time']}] {n['content']}")

    def contacts(self, action=None, *args):
        if action == "add":
            name = input("Name: ").strip()
            phone = input("Phone: ").strip()
            email = input("Email: ").strip()
            if name:
                self.fs.contacts[name.lower()] = {"phone": phone, "email": email}
                self.fs.save()
                print(f"Contact added: {name}")
        elif action == "list" or not action:
            if not self.fs.contacts:
                print("No contacts.")
            else:
                for name, info in self.fs.contacts.items():
                    print(f"{name.title()} | {info['phone']} | {info['email']}")
        else:
            print("Usage: contacts add | contacts list")

    def show_time(self):
        now = datetime.now()
        print(f"Current Time: {now.strftime('%H:%M:%S')}")
        print(f"Date: {now.strftime('%A, %B %d, %Y')}")

    # File Commands
    def files(self, path=None):
        print("  ".join(self.fs.files_cmd(path)))

    def goto(self, path):
        self.fs.goto(path)

    def makedir(self, name):
        if name: self.fs.makedir(name)
        else: print("Usage: makedir <directory>")

    def create(self, name):
        if name: self.fs.create(name)
        else: print("Usage: create <filename>")

    def delete(self, name):
        if name: self.fs.delete(name)
        else: print("Usage: delete <filename>")

    def read(self, name):
        if name: self.fs.read(name)
        else: print("Usage: read <filename>")

    def write(self, text, file):
        self.fs.write(text, file)

    def print_text(self, text):
        self.fs.print_text(text)

    def copy(self, source, dest):
        if source and dest: self.fs.copy(source, dest)
        else: print("Usage: copy <source> <destination>")

    def rename(self, old, new):
        if old and new: self.fs.rename(old, new)
        else: print("Usage: rename <old> <new>")

    def tree(self):
        self.fs.tree()

    def size(self, name):
        if name: self.fs.size(name)
        else: print("Usage: size <filename>")

    def edit(self, name):
        if name: self.fs.edit(name)
        else: print("Usage: edit <filename>")