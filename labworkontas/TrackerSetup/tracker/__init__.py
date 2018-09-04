"""This library implements the task tracker.
Tracker can:
1. Create task
2. Add task to Storage
3. Changed task
4. Output information about task
5. Creates links between tasks
6. Added admins and members in task
7. Removed task on Storage
8. Adds link parent->subtask
9. Records messages about all actions in library
10. Save and load tasks with file in JSON format

Modules in library:
1. 'manager': creates and deletes different links between tasks
2. 'base': contains a description about bases class Task for library
3. 'logger': write and gets all actions in library
4. 'storage': load and saved all tasks and messages in file. Managed all requests to tasks

Manager:
The main module in the library. Responsible for relationships between object Task
    Functions are divided into 3 groups:
    1. Work with tasks: add/deleted/changed task
    2. Work with links: add/deleted link
    3. Work with users: add/deleted admin/member

    Admin - Admins its user who can view and changed task
    Member - Member its user who can view the task, but not changed it
    Link (linked tasks) -  Related task know information about each other
    (for more information read doc. 'tracker.manager)

Storage:
Auxiliary class, which includes functions for working with files
    Main methods:
    1. get_task
    2. save_task
    3. get_all_tasks
    4. get_all_users
    etc. (for more information read doc. 'tracker.storage')

Base:
An auxiliary module that stores a class of objects for working with libraries
(for more information read doc. 'tracker.base')

Logger:
A helper class that records all your actions and errors in a file
(for more information read doc. 'tracker.logger')


Library contains two default directories: (if file configuration not found)
1. 'database': contains files with tasks and messages
2. 'logger_output': contains files with logger records

For more information, read the documentation for the modules


Templates
________________________________________________________________________________

from tracker.manager import Manager
from tracker.logger import Logger
from tracker.base import Task

"Added task"
manager = Manager('path_to_task_file', 'path_to_message_file')  # default 'database.tasks/messages.txt'

manager.add_task(Task(parent=None, name='my_task', host='andrew', key='11', priority=5, status='worked',
                        start='11:20 05/06/2018', end='12:00 05/06/2018', period='0/0/1/20', type_task='work'))


"Get task"
task = manager.storage.get_task('11')  # after receiving the task, it is removed from the storage

print(task.start_time)
print(task.name)
etc.


"Save task"
manager.save_task(task)


"Delete task"
manager.delete_task('11')


"Add member/admin"
manager.add_member_in_task('11', 'Tom')


"Removed member/admin"
manager.delete_member_in_task('11', 'Tom')


"Add/removed link"
key_second = manager.add_task(key='100', name='sec_task')

manager.add_link('11', key_second)
manager.deleter_link('11', key_second)


"Set_new_params_task"

params = manager.get_changed_task_params('11')

# old params included: name, priority, period, start time task, end time task, status and type task

params[0] = 'new_name'
params[6] = 'new_status'

manager.set_new_params_task('11', params)


"Set_logger"
my_logger = Logger(path_to_logger_output='path to output logger')  # default logger_output/logger_output.txt
"""
