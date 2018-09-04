"""
This module contains a class for storing and loading all task in file

Public class:

'Storage': Designed to store tasks and execute queries to them. (See the class Storage document for details)
"""

import random
import json
import os
from collections import deque
from datetime import datetime, timedelta


from tracker.base import Task


class Storage:
    """
    Is designed to store, load and save program task in file, receipt of necessary tasks and their parameters
    on request (default file for tasks=tasks.txt, for user messages=messages.txt)

    Public Methods:

    'give_free_key': generates a unique key for task (max value = 500)
    'save_task': save object Task to file
    'get_task': return object Task of file
    'get_all_task': return all objects Task of file
    'get_keys_tasks': return keys all Tasks in file
    'get_all_users': return names all users referred in the tasks
    'get_user_task': return tasks in which the name of this user is mentioned
    'save_message': save user message in file
    'get_user_messages': return all messages intended for this user
    'save_scanned_task': save task in json format in file
    'check_time': check start and end time in tasks
    'date_translation': translate start and end time in tasks with period
    'get_all_tasks_in_tree': return list with all subtasks select task
    """

    __DEFAULT_TASKS_FILE = os.path.dirname(__file__) + '/tasks.txt'
    __DEFAULT_MESSAGES_FILE = os.path.dirname(__file__) + '/messages.txt'

    def __init__(self, path_to_task_file=None, path_to_message_file=None):

        if path_to_task_file:
            self.path_to_task_file = path_to_task_file
        else:
            self.path_to_task_file = self.__DEFAULT_TASKS_FILE

        if path_to_message_file:
            self.path_to_message_file = path_to_message_file
        else:
            self.path_to_message_file = self.__DEFAULT_MESSAGES_FILE

    def get_free_key_task(self):
        """Generate unique key for tasks. Loads all tasks and returns the first random key. Max key counts = 500 (temp.)

        :return: key in string format or None if count key=500
        """
        keys = []

        try:
            with open(self.path_to_task_file, 'r') as file:
                for line in file:
                    current_task = Task()
                    current_task.load(line)
                    keys.append(current_task.key)
        except:
            pass

        while True:
            if len(keys) == 500:
                return None
            key = random.randint(0, 500)
            if key not in keys:
                return str(key)

    def save_task(self, task):
        """Check object on type Task and save object Task to file in json format (default file=tasks.txt)

        :param
        'task': object to save in file
        """
        if type(task) != Task:
            raise TypeError("Object type is not Task")

        with open(self.path_to_task_file, 'a') as output:
            json.dump(task.__dict__, output)
            output.write('\n')

    def get_task(self, key_task):
        """Returns a task with the specified key from a file (default file=tasks.txt). If task not found,
        return None

        :param
        'key_task': key of the selected tasks

        :return: object Task or None, if task not found in file
        """
        task = None
        scanned_tasks = []

        with open(self.path_to_task_file, 'r') as file:
            for line in file:
                current_task = Task()
                current_task.load(line)

                if current_task.key == key_task:
                    task = current_task
                else:
                    scanned_tasks.append(line)

        self.check_time(task)
        self.save_scanned_tasks(scanned_tasks)  # return unsuccessful tasks in file
        return task

    def save_scanned_tasks(self, scanned_tasks):
        """Save tasks in json format in file (default file=tasks.txt)

        :param
        'scanned_tasks': list tasks in json format
        """

        with open(self.path_to_task_file, 'w') as output:
            for json_task in scanned_tasks:
                output.write(json_task)

    def get_all_tasks(self):
        """Returns all objects tasks of file and clear this (default file=tasks.txt)

        :return: list objects Tasks of file
        """
        tasks = []

        with open(self.path_to_task_file, 'r') as file:
            for line in file:
                task = Task()
                task.load(line)
                tasks.append(task)
        with open(self.path_to_task_file, 'w'):
            pass

        for task in tasks:
            self.check_time(task)

        return tasks

    def get_keys_tasks(self):
        """Scanned all tasks in file and return list of task keys (default file=tasks.txt)

        :return: list keys tasks
        """
        keys_task = []
        scanned_task = []

        with open(self.path_to_task_file, 'r') as file:
            for line in file:
                task = Task()
                task.load(line)
                keys_task.append(task.key)
                scanned_task.append(line)

        self.save_scanned_tasks(scanned_task)  # return unsuccessful tasks in file
        return keys_task

    def get_all_tasks_in_tree(self, key_main_task=None):
        """Return list with keys all subtasks this tree (use BFS)

            :param
            key_main_task: key first task

            :return
            list tasks tree
        """
        queue_for_bfs = deque()

        task = self.get_task(key_main_task)
        if not task:
            return None

        queue_for_bfs.append(task)
        list_tasks_project = [task]
        self.queue_on_project(queue_for_bfs, list_tasks_project)
        self.save_task(task)
        return list_tasks_project

    def queue_on_project(self, queue_for_bfs, list_tasks_project):
        """Recursive function for collection all tasks this project in list(use BFS)

        :param
        queue_for_bfs: queue with unvisited tasks
        list_tasks_tree: list with subtasks select task
        """
        if not len(queue_for_bfs):
            return
        else:
            task = queue_for_bfs.popleft()
            for key_sub in task.subtasks:
                sub = self.get_task(key_sub)
                list_tasks_project.append(sub)
                queue_for_bfs.append(sub)
                self.save_task(sub)

            self.queue_on_project(queue_for_bfs, list_tasks_project)

    def get_all_users(self):
        """Scanned all tasks in file and return set name users meeting in the attributes 'admins' and 'members'
        (default file=tasks.txt)

        :return: set name users
        """
        set_users = set()
        scanned_task = []

        with open(self.path_to_task_file, 'r') as file:
            for line in file:
                task = Task()
                task.load(line)
                for user in task.admins:
                    set_users.add(user)
                for user in task.members:
                    set_users.add(user)
                scanned_task.append(line)

        self.save_scanned_tasks(scanned_task)  # return unsuccessful tasks in file
        return set_users

    def get_user_task(self, name_user):
        """Scanned all tasks in file and return list tasks when this user meeting in the attributes 'admins' and 'members'
        (default file=tasks.txt)

        :param
        'name_user': name selected user

        :return: list tasks with this user
        """
        user_tasks = []
        scanned_task = []

        with open(self.path_to_task_file, 'r') as file:
            for line in file:
                task = Task()
                task.load(line)
                if name_user in task.admins:
                    user_tasks.append(task)
                elif name_user in task.members:
                    user_tasks.append(task)
                else:
                    scanned_task.append(line)

        self.save_scanned_tasks(scanned_task)  # return unsuccessful tasks in file
        return user_tasks

    def save_message(self, user, message):
        """Save user message on file in format "date user message" (default file=messages.txt)

        :param
        'user': name message user
        'message': string message
        """
        full_message = '{0} {1} {2}'.format(str(datetime.now()), user, message)
        with open(self.path_to_message_file, 'a') as output:
            output.write(full_message + '\n')

    def get_message_user(self, name_user):
        """Return list messages this user of file (default file=messages.txt)

        :param
        'name_user': name select user

        :return: list tasks
        """
        messages = []

        with open(self.path_to_message_file, 'r') as file:
            for line in file:
                if line.split()[2] == name_user:  # you must select 3 item, because string in format:
                    messages.append(line)         # "date" "time" "user" "messages"
        return messages

    @classmethod
    def check_time(cls, task):
        """Checks the time of the task relative to the current time and translates it if necessary

        :param
        'task': object type of Task
        """
        if not task:
            return
        cur_time = datetime.now().strftime("%H:%M %d/%m/%Y")
        if task.period:
            # if this task has end time and period and end time has passed, we  will move time this step period
            # while end time less then current time
            while datetime.strptime(cur_time, "%H:%M %d/%m/%Y") > datetime.strptime(task.time_last_copy, "%H:%M %d/%m/%Y"):
                task.time_last_copy = cls.date_translation(task.time_last_copy, task.period)
                new_task = Task()
                new_task.name = task.name
                new_task.parent = task.parent
                new_task.host = task.host
                new_task.key = cls.get_free_key_task()
                new_task.type_task = task.type_task
                new_task.admins = task.admins.copy()
                new_task.members = task.members.copy()
                new_task.priority = task.priority
                new_task.status = task.status
                new_task.start_time = task.start_time
                new_task.end_time = task.end_time
                new_task.period = ''
                cls.save_task(new_task)

    @staticmethod
    def date_translation(date_str, period):
        """Translate the date for a given period forward

        :param
        'date_str': date in string format
        'period': period in format month/days/hours/minutes

        :return: new date in string format "%H:%M %d/%m/%Y"
        """
        time = datetime.strptime(date_str, "%H:%M %d/%m/%Y")
        periods = period.split("/")

        time = time.replace(year=time.year + int(periods[0]) // 12)

        try:
            time = time.replace(month=time.month + (int(periods[0]) % 12))
        except:
            # if count month > 12 after added new month
            time = time.replace(year=time.year + 1, month=time.month + (int(periods[0]) % 12) - 12)

        time = time + timedelta(days=int(periods[1]), hours=int(periods[2]), minutes=int(periods[3]))

        return time.strftime("%H:%M %d/%m/%Y")
    ''''''