A simple task tracker cli written in Python written based on the instructions at https://roadmap.sh/projects/task-tracker


## Features
- Add new tasks
- Update existing task
- Delete tasks by ID
- Mark tasks as "todo" , "in-progress" ,"done"
- List all task or filter them by status
- Store task data persistently using JSON
- Automatically assing unique IDs to tasks.


## Technologies Used
- Python 3
- JSON
- OS Module
- Datetime Module


## Installation
1. Clone the repository:
   git clone REPOSITORY_URL
2. Navigate to the project directory:
   cd tasktracker
3. Run the application: 
   python task_tracker.py

## Usage
Add Task
- python task_tracker.py add "Learn Python"

Update Task
- python task_tracker.py update 1 "Start Learning Advanced Python"

Delete Task
- python task_tracker.py delete 1

Mark a Task as In Progress
- python task_tracker.py mark-in-progress 1

Mark a Task as Done
- python task_tracker.py mark-done 1

List All Tasks
- python task_tracker.py list

Filter Tasks by Status
- python task_tracker.py list todo
- python task_tracker.py list in-progress
- python task_tracker.py list done

## Data Storage
Task information is stored locally in a tasks.json file.

Each task contains:
- id: Unique task identifier.
- description: Task description.
- status: Current task status.
- createdAT: Task creation timestamp.
- updatedAT: Last update timestamp.





  
