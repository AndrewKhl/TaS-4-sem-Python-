"""
The module is designed to store the base classes of the program

Public class in module:

'Task': The main class for working with the tracker. Contains all information about the task:
its name, participants, deadlines, etc. (See the class Task document for details)
"""


import json
from datetime import datetime


class Task:
    """
    Designed to store the object task and work with it

    Public Attributes

    'name': name task
    'host': name user, created this task
    'type': belonging task to any group
    'parent': parent task (for related task)
    'subtasks': list subtask (for related task)
    'priority': priority task (1-5), is taken into account in the output tasks
    'members': users working on this task
    'links': keys linked tasks
    'status': status task (ended, waiting, process), show the jobs process
    'start_time': time start task in format HH:MM dd/mm/YY
    'end_time': time end task in format HH:MM dd/mm/YY
    'period': show line period task in format month/days/hours/minutes

    Readonly Attributes:

    'key': unique key task in Storage
    'create_time': time create task in format HH:MM dd/mm/YY
    'change_time': time change task in format HH:MM dd/mm/YY

    Public Methods:

    'return_changed_params_task': provides list changed params
    'set_new_params_task': set new params task
    'load': loading information from json string
    """
    def __init__(self, parent=None, name=None, host=None, priority=None, status=None, start=None, end=None,
                 period=None, type_task=None, time_last_copy=None):
        self.name = name
        self.parent = parent
        self.host = host
        self.__key = None
        self.type_task = type_task
        self.subtasks = []
        if host:
            self.admins = [host]
            self.members = [host]
        else:
            self.admins = []
            self.members = []
        self.links = []
        if time_last_copy:
            self.time_last_copy = None
        else:
            self.time_last_copy = str(datetime.now().strftime("%H:%M:%S %d/%m/%Y"))
        self.__create_time = str(datetime.now().strftime("%H:%M:%S %d/%m/%Y"))
        self.__change_time = str(datetime.now().strftime("%H:%M:%S %d/%m/%Y"))
        self.priority = priority
        self.status = status
        self.start_time = start
        self.end_time = end
        self.period = period

    def __str__(self):
        if self.parent:
            return 'N' + str(self.key) + ' ' + self.name + ' ' + '(pr N' + self.parent + ')'
        else:
            return 'N' + str(self.key) + ' ' + self.name

    @property
    def key(self):
        return self.__key

    @key.setter
    def key(self, value):
        if type(value) == str:
            self.__key = value
        else:
            raise TypeError('attribute not type str')

    @property
    def create_time(self):
        return self.__create_time

    @property
    def change_time(self):
        return self.__change_time

    def load(self, string):
        """Load information from json string

        :param task recorded in json format
        """
        self.__dict__ = json.loads(string)

    def get_changed_task_params(self):
        """Return list changed params task
        list params included: name, priority, period, start time task, end time task, status and type task

        :return list changed params
        """
        return [self.name, self.priority, self.period, self.start_time, self.end_time, self.status, self.type_task]

    def set_new_params_task(self, params):
        """Set new params task
        list params included: name, priority, period, start time task, end time task, status and type task

        :param params: new params task
        """
        self.name = params[0]
        self.priority = params[1]
        self.period = params[2]
        self.start_time = params[3]
        self.end_time = params[4]
        self.status = params[5]
        self.type_task = params[6]
        self.__change_time = str(datetime.now().strftime("%H:%M:%S %d/%m/%Y"))
