import sys
import os
import json
import datetime
import requests

FILENAME = 'tasks.json'
STATUSES = [
    "todo",
    "done",
    "in-progress"
]


class Task:
    def __init__(self, task_id, description, status):
        self.task_id = task_id
        self.description = description
        self.status = status
        self.createdAT = datetime.datetime.now()
        self.updatedAT = datetime.datetime.now()

    def to_dict(self):
        return {
            "id": self.task_id,
            "description": self.description,
            "status": self.status,
            "createdAT": self.createdAT.strftime("%H:%M:%S"),
            "updatedAT": self.updatedAT.strftime("%H:%M:%S")
        }


def add(args):
    # get description
    description = get_description(args, "add")

    # get the tasks
    tasks = check_file()

    try:
        # get last task's id
        task_id = int(tasks[-1]["id"]) + 1
    except IndexError:
        # first task
        task_id = 1

    # Create a new task
    new_task = Task(task_id, description, STATUSES[0])

    # Get the dictionary form
    task_dict = new_task.to_dict()

    # Append new task
    tasks.append(task_dict)

    # Write updated list back to file
    with open(FILENAME, 'w') as f:
        json.dump(tasks, f, indent=4)
    print(f"\nTask added successfully (ID: {task_id})\n")


def delete(args):
    id = get_second_element(args, "delete")
    tasks = check_file()
    taskIds = task_ids()
    if tasks == []:
        print("\nTask list is empty.\n")
    else:
        if id in taskIds:
            for task in tasks:
                if task.get('id') == id:
                    task_index = tasks.index(task)
                    tasks.pop(task_index)
                    print(f"\nTask {id} deleted.\n")
                    with open(FILENAME, 'w') as f:
                        json.dump(tasks, f, indent=4)
                    return
        else:
            print("\nInvalid task id.\n")


def list(args):
    status = get_second_element(args, "list")
    sorted_tasks = sort_tasks(status)
    print()
    print("-" * 10, f"{status.capitalize()} Tasks", "-" * 10, "\n")
    if sorted_tasks == None:
        print("Invalid Status.\n")
    elif not sorted_tasks:
        print("No tasks for this status.\n")
    else:
        for task in sorted_tasks:
            task = f"Task {task["id"]}:\n Description - {task["description"]}\n Status - {task["status"]}\n Created at - {task["createdAT"]}\n Updated at - {task["updatedAT"]}\n"
            print(task)
    print("-" * 40, "\n")


def mark(args):
    new_status = get_description(args, "mark")
    id = get_second_element(args, "mark")
    taskIds = task_ids()
    tasks = check_file()
    if id in taskIds:
        for task in tasks:
            if id == task.get('id'):
                if new_status in STATUSES:
                    task["status"] = new_status
                    updatedAT = datetime.datetime.now()
                    task["updatedAT"] = updatedAT.strftime("%H:%M:%S")
                    with open(FILENAME, 'w') as f:
                        json.dump(tasks, f, indent=4)
                    return
                else:
                    print(f"\nInvalid {new_status} status.\n")
                    continue
            else:
                continue
    else:
        print("\nInvalid task id.\n")
        return


def update(args):
    new_description = get_description(args, "update")
    id = get_second_element(args, "update")
    taskIds = task_ids()
    tasks = check_file()
    if id in taskIds:
        for task in tasks:
            if id == task.get('id'):
                task["description"] = new_description
                updatedAT = datetime.datetime.now()
                task["updatedAT"] = updatedAT.strftime("%H:%M:%S")
                with open(FILENAME, 'w') as f:
                    json.dump(tasks, f, indent=4)
                return
            else:
                continue
    else:
        print("\nInvalid task id.\n")
        return


def check_file():
    # Load existing tasks if file exists
    if os.path.exists(FILENAME):
        try:
            with open(FILENAME, "r") as f:
                tasks = json.load(f)
        except json.decoder.JSONDecodeError:
            # if the file is empty
            tasks = []
    else:
        # create an empty
        tasks = []

    return tasks


def get_description(args, func):
    if len(args) > 1:
        if func == "add":
            description = " ".join(args[1:])
            return description
        elif func == "update":
            if len(args[2:]) > 0:
                description = " ".join(args[2:])
                return description
            else:
                print("\nNew task description needed.\n")
        elif func == "mark":
            if len(args[2:]) > 0:
                description = " ".join(args[2:])
                return description
            else:
                print("\nNew task status needed.\n")

    else:
        if func == "add":
            print("\nTask description needed.\n")
        elif func == "update":
            print("\nTask id and description needed.\n")
        elif func == "mark":
            print("\nTask id and new status needed.\n")

    main()


def sort_tasks(status):
    tasks = check_file()

    match status:
        case "all":
            return tasks
        case "todo":
            todo_tasks = [
                task for task in tasks if task.get('status') == "todo"]
            return todo_tasks
        case "done":
            done_tasks = [
                task for task in tasks if task.get('status') == "done"]
            return done_tasks
        case "in-progress":
            inProgress_tasks = [task for task in tasks if task.get(
                'status') == "in-progress"]
            return inProgress_tasks
        case _:
            return None


def task_ids():
    tasks = check_file()
    taskIds = [task["id"] for task in tasks]
    return taskIds


def get_second_element(args, func):
    if func == "list":
        try:
            second_element = args[1].lower()
            if second_element.isalpha():
                return second_element
            elif second_element == "in-progress":
                return second_element
        except IndexError:
            second_element = "all"
            return second_element
    elif func in ["delete", "update", "mark"]:
        try:
            second_element = args[1]
            if second_element.isdigit():
                return int(second_element)
        except IndexError:
            return 0


def help_file():
    filename = "help.txt"
    if os.path.exists(filename):
        print("Help file found...printing...\n\n\n")
        with open(filename, "r") as f:
            for line in f:
                print(line)
        print()
        main()
    else:
        print("\nDownloading help file...please wait before using help\n")
        url = "https://github.com/Xqni/taskcli/blob/main/help.txt"
        filename = requests.get(url)
        main()


def main():

    # check for file
    check_file()
    try:
        # task user input
        # strip whitespace
        # split into a list of words
        while True:
            args = input("task-cli: ").strip().split()

            # get first element in list

            cmd = args[0].lower()  # convert to lowercase

            if cmd == "add":
                add(args)
            elif cmd == "list":
                list(args)
            elif cmd == "mark":
                mark(args)
            elif cmd == "delete":
                delete(args)
            elif cmd == "update":
                update(args)
            elif cmd == "help" or cmd == "-h":
                help_file()
            else:
                print("\nInvalid syntax. Type 'help' or '-h' if need help.\n")
                continue
    except KeyboardInterrupt:
        print("\nExisting the program. User interruption.\n")
        sys.exit(1)
    except IndexError:
        main()


if __name__ == "__main__":
    print("\nWelcome, to get started type 'help' or '-h' to view help file.\n")
    main()
