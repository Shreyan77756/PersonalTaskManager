import json
import os
from datetime import datetime
import click

TASKS_FILE = "tasks.json"

def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as file:
            return json.load(file)
    else:
        return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=2)

def display_tasks(tasks):
    if not tasks:
        print("No tasks found.")
    else:
        for task in tasks:
            print(f"Title: {task['title']}")
            print(f"Description: {task['description']}")
            print(f"Due Date: {task['due_date']}")
            print(f"Status: {task['status']}")
            print("------")

def add_task():
    title = input("Enter task title: ")
    description = input("Enter task description: ")

    while True:
        try:
            due_date = datetime.strptime(input("Enter due date (YYYY-MM-DD): "), "%Y-%m-%d")
            break
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

    tasks = load_tasks()
    new_task = {
        "title": title,
        "description": description,
        "due_date": due_date.strftime("%Y-%m-%d"),
        "status": "pending"
    }
    tasks.append(new_task)
    save_tasks(tasks)
    print("Task added successfully.")

def mark_completed(title):
    tasks = load_tasks()
    for task in tasks:
        if task['title'] == title:
            task['status'] = 'completed'
            save_tasks(tasks)
            print(f"Task '{title}' marked as completed.")
            return
    print(f"Task '{title}' not found.")

def edit_task(title):
    tasks = load_tasks()
    for task in tasks:
        if task['title'] == title:
            print(f"Editing task: {title}")
            task['title'] = input(f"Enter new title (currently: {task['title']}): ") or task['title']
            task['description'] = input(f"Enter new description (currently: {task['description']}): ") or task['description']
            while True:
                try:
                    task['due_date'] = datetime.strptime(input(f"Enter new due date (YYYY-MM-DD) (currently: {task['due_date']}): "), "%Y-%m-%d").strftime("%Y-%m-%d")
                    break
                except ValueError:
                    print("Invalid date format. Please use YYYY-MM-DD.")
            save_tasks(tasks)
            print(f"Task '{title}' edited successfully.")
            return
    print(f"Task '{title}' not found.")

def delete_task(title):
    tasks = load_tasks()
    tasks = [task for task in tasks if task['title'] != title]
    save_tasks(tasks)
    print(f"Task '{title}' deleted successfully.")

def sort_tasks():
    tasks = load_tasks()
    sorted_tasks = sorted(tasks, key=lambda x: datetime.strptime(x['due_date'], "%Y-%m-%d"))
    display_tasks(sorted_tasks)

def filter_tasks(status):
    if status.lower() not in ['pending', 'completed']:
        print("Invalid status. Please enter 'pending' or 'completed'.")
        return
    tasks = load_tasks()
    filtered_tasks = [task for task in tasks if task['status'] == status.lower()]
    display_tasks(filtered_tasks)

if __name__ == "__main__":
    while True:
        print("1. Add Task")
        print("2. Display Tasks")
        print("3. Mark Task as Completed")
        print("4. Edit Task")
        print("5. Delete Task")
        print("6. Sort Tasks by Due Date")
        print("7. Filter Tasks by Status")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_task()
        elif choice == "2":
            tasks = load_tasks()
            display_tasks(tasks)
        elif choice == "3":
            title_to_mark = input("Enter the title of the task to mark as completed: ")
            mark_completed(title_to_mark)
        elif choice == "4":
            title_to_edit = input("Enter the title of the task to edit: ")
            edit_task(title_to_edit)
        elif choice == "5":
            title_to_delete = input("Enter the title of the task to delete: ")
            delete_task(title_to_delete)
        elif choice == "6":
            sort_tasks()
        elif choice == "7":
            status_to_filter = input("Enter status to filter (pending/completed): ")
            filter_tasks(status_to_filter)
        elif choice == "8":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
