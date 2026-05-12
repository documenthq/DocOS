#!/usr/bin/env python3
# Document OS 1.0 - Official Company System

import os
import sys
import time
import getpass
from datetime import datetime

from filesystem import DocumentFS
from commands import CommandHandler

# === User System (same as before) ===
def load_users():
    USERS_FILE = "document_users.json"
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r") as f:
                return __import__('json').load(f)
        except:
            return {}
    return {}

def save_users(users):
    USERS_FILE = "document_users.json"
    try:
        with open(USERS_FILE, "w") as f:
            __import__('json').dump(users, f, indent=2)
    except:
        pass

def create_account():
    print("\n=== Document Company - Create Account ===")
    while True:
        username = input("Choose username: ").strip()
        if not username:
            print("Username cannot be empty.")
            continue
        users = load_users()
        if username.lower() in users:
            print(f"\033[91m\033[4m{username}\033[0m is already taken.")
            print("Please add a number or change the username.\n")
            continue
        password = getpass.getpass("Choose password: ")
        confirm = getpass.getpass("Confirm password: ")
        if password != confirm:
            print("Passwords do not match.")
            continue
        if len(password) < 3:
            print("Password too short.")
            continue
        users[username.lower()] = password
        save_users(users)
        print(f"Account '{username}' created successfully.\n")
        return username

def login():
    users = load_users()
    if not users:
        return create_account()
    print("\n" + "="*65)
    print("               Document OS 1.0")
    print("          Official Company System")
    print("="*65)
    print("\nLogin required")
    for _ in range(3):
        username = input("Username: ").strip()
        password = getpass.getpass("Password: ")
        if username.lower() in users and users[username.lower()] == password:
            print("Login successful.\n")
            return username
        print("Invalid credentials.\n")
    print("Access denied.")
    sys.exit(1)


def main():
    username = login()
    hostname = "document"
    fs = DocumentFS()
    cmd = CommandHandler(fs)

    print("="*65)
    print(f"Logged in as {username}@{hostname}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    print("Welcome to Document OS\n")

    while True:
        try:
            prompt = f"[{username}@{hostname} {fs.cwd}]$ "
            line = input(prompt).strip()
            if not line: continue

            parts = line.split()
            command = parts[0].lower()

            if command == "help":
                print("\n" + "="*60)
                print("                 AVAILABLE COMMANDS")
                print("="*60)
                print("  help                  - Show this help menu")
                print("  files [path]          - List files and directories")
                print("  goto <dir>            - Change directory (.. to go up)")
                print("  makedir <name>        - Create new directory")
                print("  create <file>         - Create new empty file")
                print("  delete <file>         - Delete a file")
                print("  read <file>           - View file contents")
                print("  write <text> > <file> - Write text to a file")
                print("  print <text>          - Print text on screen")
                print("  copy <src> <dest>     - Copy a file")
                print("  rename <old> <new>    - Rename file or folder")
                print("  tree                  - Show folder structure")
                print("  size <file>           - Show file size")
                print("  edit <file>           - Simple text editor")
                print("")
                print("  calc <expression>     - Calculator (e.g. 250 * 12)")
                print("  todo add <task>       - Add a task")
                print("  todo list             - List all tasks")
                print("  todo done <number>    - Mark task as done")
                print("  note <text>           - Add quick note")
                print("  contacts add          - Add new contact")
                print("  contacts list         - Show contacts")
                print("  time                  - Show current time & date")
                print("  date                  - Show full date")
                print("  whoami                - Show current user")
                print("  clear                 - Clear screen")
                print("  neofetch              - System information")
                print("  shutdown              - Save & exit")
                print("="*60)

            elif command == "files":     cmd.files(parts[1] if len(parts)>1 else None)
            elif command == "goto":      cmd.goto(parts[1] if len(parts)>1 else "/")
            elif command == "makedir":   cmd.makedir(parts[1] if len(parts)>1 else None)
            elif command == "create":    cmd.create(parts[1] if len(parts)>1 else None)
            elif command == "delete":    cmd.delete(parts[1] if len(parts)>1 else None)
            elif command == "read":      cmd.read(parts[1] if len(parts)>1 else None)
            elif command == "print":     cmd.print_text(" ".join(parts[1:]))
            elif command == "write":
                if ">" in line:
                    text = line.split(">", 1)[0].replace("write","").strip()
                    file = line.split(">", 1)[1].strip()
                    cmd.write(text, file)
                else:
                    print("Usage: write <text> > <file>")
            elif command == "copy":      cmd.copy(parts[1] if len(parts)>1 else None, parts[2] if len(parts)>2 else None)
            elif command == "rename":    cmd.rename(parts[1] if len(parts)>1 else None, parts[2] if len(parts)>2 else None)
            elif command == "tree":      cmd.tree()
            elif command == "size":      cmd.size(parts[1] if len(parts)>1 else None)
            elif command == "edit":      cmd.edit(parts[1] if len(parts)>1 else None)

            elif command == "calc":      cmd.calc(" ".join(parts[1:]))
            elif command == "todo":      cmd.todo(parts[1] if len(parts)>1 else "list", *parts[2:])
            elif command == "note":      cmd.note(*parts[1:])
            elif command == "contacts":  cmd.contacts(parts[1] if len(parts)>1 else None)
            elif command == "time":      cmd.show_time()
            elif command == "date":      print(datetime.now().strftime("%A, %B %d, %Y"))
            elif command == "whoami":    print(username)
            elif command == "clear":     os.system('cls' if os.name == 'nt' else 'clear')
            elif command == "neofetch":
                print(f"\n   Document OS 1.0\n   Company: Document\n   User: {username}\n   Tasks: {len(fs.todos)}\n")
            elif command == "shutdown":
                fs.save()
                print("Saving all business data...")
                time.sleep(0.8)
                print("Document OS shutdown completed successfully.")
                sys.exit(0)
            else:
                print(f"Command not found: {command}")
                print("Type 'help' for full list of commands.")

        except KeyboardInterrupt:
            print("\nUse 'shutdown' to exit.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()