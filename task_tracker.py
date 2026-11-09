#!/usr/bin/env python3
"""
task_cli.py - basit Task Tracker CLI
Kullanım (positional args):
  python task_cli.py add "Buy groceries"
  python task_cli.py update 1 "New description"
  python task_cli.py delete 1
  python task_cli.py mark-in-progress 1
  python task_cli.py mark-done 1
  python task_cli.py list            # tüm görevler
  python task_cli.py list done
  python task_cli.py list todo
  python task_cli.py list in-progress

"""

import sys
import json
import os
from datetime import datetime

TASKS_FILE = "tasks.json"
VALID_STATUSES = {"todo", "in-progress", "done"}

def now_iso():
    return datetime.now().isoformat(timespec='seconds')

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return[]
    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data,list):
                return[]
            return data
    except (json.JSONDecodeError, IOError):
        return[]

def save_tasks(tasks):
    tmp = TASKS_FILE + ".tmp"
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=2, ensure_ascii=False)
        os.replace(tmp,TASKS_FILE)
    except IOError as e:
        print(f"Hata: Görevler kaydedilemedi. {e}")

def next_id(tasks):
    if not tasks:
        return 1
    try:
        max_id = max(int(t.get("id", 0)) for t in tasks)
        return max_id + 1
    except Exception:
        return max((t.get("id") for t in tasks if isinstance (t.get("id"), int)), default=0) + 1

def add_task(description):
    if not description or not description.strip():
        print("Hata: Açıklama boş olamaz.")
        return
    tasks = load_tasks()
    tid = next_id(tasks)
    now = now_iso()
    task = {
        "id": tid,
        "description": description,
        "status": "todo",
        "createdAT": now,
        "updatedAT": now
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Task added succesfully (ID: {tid})")

def find_task(tasks, tid):
    for t in tasks:
        try:
            if int (t.get("id")) == int(tid):
                return t
        except Exception:
            continue
    return None

def update_task(tid, new_description):
    if not new_description or not new_description.strip():
        print("Hata: Yeni açıklama boş olamaz.")
        return
    tasks = load_tasks()
    task = find_task(tasks, tid)
    if not task:
        print(f"Hata:ID {tid} bulunamadı.")
        return
    task["description"] = new_description
    task["updatedAT"] = now_iso()
    save_tasks(tasks)
    print(f"Task {tid} updated succesfully.")

def delete_task(tid):
    tasks = load_tasks()
    task = find_task(tasks, tid)
    if not task:
        print(f"Hata: ID {tid} bulunamadı.")
        return
    tasks = [t for t in tasks if str(t.get("id")) != str(tid)]
    save_tasks(tasks)
    print(f"Task {tid} deleted succesfully.")

def set_status(tid,status):
    if status not in VALID_STATUSES:
        print(f"Hata:Geçeresiz status: {status}.")
        return
    tasks=load_tasks()
    task = find_task(tasks, tid)
    if not task:
        print(f"Hata: ID {tid} bulunamadı.")
        return
    task["status"] = status
    task["updatedAT"] = now_iso()
    save_tasks(tasks)
    print(f"Task {tid} marked as {status}.")

def list_tasks(filter_status = None):
    tasks = load_tasks()

    if filter_status:
        if filter_status not in VALID_STATUSES:
            print(f"Hata: Geçersiz filter")
            return

        tasks = [
            t for t in tasks
            if t.get("status") == filter_status
        ]

    if not tasks:
        print("Görev yok.")
        return

    print(f"{'ID':<4} {'STATUS':<11} DESCRIPTION")
    print("-"*50)
    for t in tasks:
        print(f"{t.get('id'):4}"
              f" {t.get('status')}"
              f" {t.get('description')}"
              )


def print_help():
    print("Kullanım (positional args):")
    print("  add \"description\"")
    print("  update <id> \"new description\"")
    print("  delete <id>")
    print("  mark-in-progress <id>")
    print("  mark-done <id>")
    print("  list [todo|in-progress|done]")
    print("Örnek: python task_cli.py add \"Buy groceries\"")

def main(argv):
    if len(argv) <2:
        print_help()
        return

    cmd = argv[1]

    try:
        if cmd == "add":
            if len(argv) < 3:
                print("Hata: add komutu için açıklama ver.")
                return
            description = " ".join(argv[2:]).strip()
            add_task(description)

        elif cmd == "update":
            if len(argv) < 4:
                print("Hata: update <id> \"new description\"")
                return
            tid = argv[2]
            new_description = " ".join(argv[3:]).strip()
            update_task(tid, new_description)

        elif cmd == "delete":
            if len(argv) != 3:
                print("Hata: delete <id>")
                return
            delete_task(argv[2])

        elif cmd == "mark-in-progress":
            if len(argv) != 3:
                print("Hata: mark-in-progress <id>")
                return
            set_status(argv[2], "in-progress")

        elif cmd == "mark-done":
            if len(argv) != 3:
                print("Hata: mark-done <id>")
                return
            set_status(argv[2], "done")

        elif cmd == "list":
            if len(argv) == 1:
                list_tasks()
            elif len(argv) == 2:
                list_tasks()
            elif len(argv) == 3:
                list_tasks(argv[2])
            else:
                print("Hata: list [todo|in-progress|done]")
                return

        elif cmd in ("help", "-h", "--help"):
            print_help()

        else:
            print(f"Tanımadığım komut: {cmd}")
            print_help()

    except Exception as e:
        print("Beklenmeyen bir hata oluştu:", str(e))


if __name__ == "__main__":
    main(sys.argv)
