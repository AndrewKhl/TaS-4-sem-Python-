"""
It is intended for management of all requests of the program

Each functions:
1. Gets task from the self.storage
2. Verifies the correctness of the data
3. Raises an exception on errors
4. Created/removed select links
5. Return task in the self.storage

Public Methods:

'add_task': add new task in 'self.__storage'
'delete task': removed task in 'self.__storage'
'self.error_key_task': generate Exception error key
'add_link': add link between tasks
'set_storage': replacing old __storage
'delete _link': delete link between tasks
'add_member_in_task': add new member in task
'delete_member_in_task': removed member in task
'add_admin_in_task': add new admin in task
'delete_admin_in_task': removed admin in task
'set_new_params_task': set new list changed params

Public Methods transferred from storage:

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

Admin - Admins its user who can view and changed task
Member - Member its user who can view the task, but not changed it
Link (linked tasks) -  Related task know information about each other
"""

from datetime import datetime


from tracker.storage import Storage
from tracker.base import Task
from tracker.logger import Logger


class Manager:

    def __init__(self, path_to_task_file=None, path_to_message_file=None):
        self.__storage = Storage(path_to_task_file, path_to_message_file)

    def set_storage(self, new_storage):
        """Adds a new class, which will be used as a Storage.
        Must have all the functions specified in init.

        :param
        'new_storage'
        """
        self.__storage = new_storage

    def add_task(self, task=None):
        """Adds task to select user/task and save this task in self.__storage

        :param
        'task': saved object

        :return key saved task

        :raise
        'TypeError': if task not type Task
        'Exception': exceeded number of tasks or incorrect key
        """
        if type(task) != Task:
            raise TypeError("Object type is not Task")

        task.key = self.__storage.get_free_key_task()

        if task.key:
            if task.parent:
                parent_task = self.__storage.get_task(task.parent)
                if not parent_task:
                    self.error_key_task(task.parent)
                else:
                    parent_task.subtasks.append(task.key)
                    task.parent = parent_task.key
                    task.host = parent_task.host
                    task.admins = parent_task.admins.copy()
                    for admin in task.admins:
                        self.__storage.save_message(admin, "Admin {0} was added to task N{1}".format(admin, task.key))
                    Logger.get_logger().debug("Task N{0} was added how subtask to task N{1}".format(task.key,
                                                                                                    parent_task.key))
                    self.__storage.save_task(parent_task)

            self.__storage.save_task(task)
            self.__storage.save_message(task.host, "User {0} was added how host to task N{1}".format(task.host, task.key))
            Logger.get_logger().debug("Task N{0} was added to self.__storage".format(task.key))
            return task.key
        else:
            Logger.get_logger().error("The free number for the task was not found")
            raise Exception("The task limit is exceeded")

    @staticmethod
    def error_key_task(key_task):
        """Generate Exception in task with this key nor found in file

        :param
        'key_task': errors key task

        :return 'True' if the function succeeded

        :raise
        'Exception': task not found in file
        """
        Logger.get_logger().error("Task with number N{0} not found".format(key_task))
        raise Exception("Task N{0} not found in file".format(key_task))

    def add_link(self, key_first, key_second):
        """Adds link between tasks

        :param
        'key_first': key first task
        'key_second': key second task

        :return 'True' if the function succeeded

        :raise
        'Exception': same task keys are selected
        """
        if key_first == key_second:
            raise Exception("The same task keys are selected")
        first_task = self.__storage.get_task(key_first)
        second_task = self.__storage.get_task(key_second)

        if not first_task:
            if second_task:
                self.__storage.save_task(second_task)
            self.error_key_task(key_first)

        if not second_task:
            if first_task:
                self.__storage.save_task(first_task)
            self.error_key_task(key_second)

        if key_second in first_task.links or key_first in second_task.links:
            Logger.get_logger().error("Link between tasks N{0} and N{1} already exist".format(key_first, key_second))
            self.__storage.save_task(first_task)
            self.__storage.save_task(second_task)
            raise Exception("Link between tasks N{0} and N{1} already exist".format(key_first, key_second))
        else:
            first_task.links.append(key_second)
            second_task.links.append(key_first)
            Logger.get_logger().debug("Link between tasks N{0} and N{1} was created".format(key_first, key_second))

            for admin in first_task.admins:
                self.__storage.save_message(admin, "Link between tasks N{0} and N{1} was created".format(key_first,
                                                                                                       key_second))
            for admin in second_task.admins:
                self.__storage.save_message(admin, "Link between tasks N{0} and N{1} was created".format(key_first,
                                                                                                       key_second))

            self.__storage.save_task(first_task)
            self.__storage.save_task(second_task)
            return True

    def delete_link(self, key_first, key_second):
        """Removed link between tasks

        :param
        'key_first': key first task
        'key_second': key second task

        :return 'True' if the function succeeded

        :raise
        'Exception': same task keys are selected
        """
        if key_first == key_second:
            raise Exception("The same task keys are selected")

        first_task = self.__storage.get_task(key_first)
        second_task = self.__storage.get_task(key_second)

        if not first_task:
            if second_task:
                self.__storage.save_task(second_task)
            self.error_key_task(key_first)

        if not second_task:
            if first_task:
                self.__storage.save_task(first_task)
            self.error_key_task(key_second)

        if key_second not in first_task.links or key_first not in second_task.links:
            Logger.get_logger().error("Link between tasks N{0} and N{1} already removed".format(key_first, key_second))
            self.__storage.save_task(first_task)
            self.__storage.save_task(second_task)
            raise Exception("Link between tasks N{0} and N{1} already removed".format(key_first, key_second))
        else:
            first_task.links.remove(key_second)
            second_task.links.remove(key_first)
            Logger.get_logger().debug("Link between tasks N{0} and N{1} was created".format(key_first, key_second))

            for admin in first_task.admins:
                self.__storage.save_message(admin, "Link between tasks N{0} and N{1} was created".format(key_first,
                                                                                                       key_second))
            for admin in second_task.admins:
                self.__storage.save_message(admin, "Link between tasks N{0} and N{1} was created".format(key_first,
                                                                                                       key_second))

            self.__storage.save_task(first_task)
            self.__storage.save_task(second_task)
            return True

    def add_admin_in_task(self, key_task, new_admin):
        """Adds admin to select task

        :param
        'key_task': key select task
        'new_admin': name new admin from task

        :return 'True' if the function succeeded

        :raise
        'Exception': admin already exist
        """
        task = self.__storage.get_task(key_task)

        if not task:
            self.error_key_task(key_task)

        if new_admin not in task.admins:
            task.admins.append(new_admin)
            Logger.get_logger().debug("Added admin {0} to task N{1}".format(new_admin, key_task))
            self.__storage.save_message(new_admin, "User {0} was added how admin to task N{1}".format(new_admin, key_task))
            self.__storage.save_task(task)
            return True
        else:
            Logger.get_logger().error("Admin {0} already exist in task N{1}".format(new_admin, key_task))
            self.__storage.save_task(task)
            raise Exception("Admin {0} already exist in task N{1}".format(new_admin, key_task))

    def add_member_in_task(self, key_task, new_member):
        """Adds member to select task

        :param
        'key_task': key select task
        'new_member': name new member from task

        :return 'True' if the function succeeded

        :raise
        'Exception': member already exist
        """
        task = self.__storage.get_task(key_task)

        if not task:
            self.error_key_task(key_task)

        if new_member not in task.members:
            task.members.append(new_member)
            Logger.get_logger().debug("Added member {0} to tree N{1}".format(new_member, key_task))
            self.__storage.save_message(new_member, "User {0} was added how member to task N{1}".format(new_member,
                                                                                                      key_task))
            self.__storage.save_task(task)
            return True
        else:
            Logger.get_logger().error("Member {0} already exist in task N{1}".format(new_member, key_task))
            self.__storage.save_task(task)
            raise Exception("Member {0} already exist in task N{1}".format(new_member, key_task))

    def delete_admin_in_task(self, key_task, key_admin):
        """Removed admin to select task

        :param
        'key_task': key select task
        'key_admin': name removed admin from task

        :raise
        'Exception': admin not found in task
        """
        task = self.__storage.get_task(key_task)

        if not task:
            self.error_key_task(key_task)

        if key_admin in task.admins:
            task.admins.remove(key_admin)
            Logger.get_logger().debug("Removed admin {0} to task N{1}".format(key_admin, key_task))
            self.__storage.save_message(key_admin, "User {0} was removed how admin to task N{1}".format(key_admin,
                                                                                                      key_task))
            self.__storage.save_task(task)
            return True
        else:
            Logger.get_logger().error("Admin {0} not found in task N{1}".format(key_admin, key_task))
            self.__storage.save_task(task)
            raise Exception("Admin {0} not found in task N{1}".format(key_admin, key_task))

    def delete_member_in_task(self, key_task, key_member):
        """Removed member to select task

        :param
        'key_task': key select task
        'key_member': name removed member from task

        :return 'True' if the function succeeded

        :raise
        'Exception': member not found in task
        """
        task = self.__storage.get_task(key_task)

        if not task:
            self.error_key_task(key_task)

        if key_member in task.members:
            task.members.remove(key_member)
            Logger.get_logger().debug("Removed member {0} to task N{1}".format(key_member, key_task))
            self.__storage.save_message(key_member, "User {0} was removed how member to task N{1}".format(key_member,
                                                                                                        key_task))
            self.__storage.save_task(task)
            return True
        else:
            Logger.get_logger().error("Member {0} not found in task N{1}".format(key_member, key_task))
            self.__storage.save_task(task)
            raise Exception("Member {0} not found in task N{1}".format(key_member, key_task))

    def set_new_params_task(self, key_task, new_params=None):
        """Set new params task

        :param
        'key_task': key changed task
        'params': list new params
        """
        task = self.__storage.get_task(key_task)

        if not task:
            self.error_key_task(key_task)
        task.set_new_params_task(new_params)
        Logger.get_logger().debug("Task N{0} was changed".format(key_task))
        for admin in task.admins:
            self.__storage.save_message(admin, "Task N{0} was changed".format(key_task))
        self.__storage.save_task(task)

    def change_status_task(self, key_task, new_status=None):
        """Change status select task

        :param
        'key_task': key select task
        'status': new status task
        """
        task = self.__storage.get_task(key_task)

        if not task:
            self.error_key_task(key_task)
        task.status = new_status
        Logger.get_logger().debug("Status task N{0} was changed on {1}".format(key_task, new_status))
        for admin in task.admins:
            self.__storage.save_message(admin, "Status task N{0} was changed".format(key_task))
        self.__storage.save_task(task)

    def delete_task(self, key_task=None):
        """Removed select task

        :param
        'key_task': key select task
        """
        task = self.__storage.get_task(key_task)

        if not task:
            self.error_key_task(key_task)

        keys_subtask = task.subtasks.copy()  # for recursive removed subtasks

        self.__storage.save_task(task)
        for subtask in keys_subtask:  # removed subtasks this task (use DFS)
            self.delete_task(subtask)

        task = self.__storage.get_task(key_task)
        for admin in task.admins:
            self.__storage.save_message(admin, "Task N{0} was removed".format(key_task))

        if task.parent:  # check on root task tree and removed link
            parent_task = self.__storage.get_task(task.parent)
            if not parent_task:
                self.error_key_task(task.parent)
            else:
                parent_task.subtasks.remove(key_task)
                self.__storage.save_task(parent_task)

        for link in task.links:
            link_task = self.__storage.get_task(link)
            if link_task:
                link_task.links.remove(key_task)
                self.__storage.save_task(link_task)

        Logger.get_logger().debug("Task N{0} was removed".format(key_task))

    def change_params_task(self, key_task, name=None, priority=None, period=None, start_time=None, end_time=None,
                           status=None, type_task=None):
        task = self.__storage.get_task(key_task)

        if not task:
            self.error_key_task(key_task)

        if name:
            task.name = name

        if priority:
            if 1 <= int(priority) <= 5:
                task.priority = priority

        if status:
            task.status = status

        if type_task:
            task.type_task = type_task

        if period:
            self.check_correct_format_period(period)
            task.period = period

        if start_time:
            task.start_time = self.normal_format_date(start_time)

        if end_time:
            task.end_time = self.normal_format_date(end_time)

        Logger.get_logger().debug("Task N{0} was changed".format(key_task))
        for admin in task.admins:
            self.__storage.save_message(admin, "Task N{0} was changed".format(key_task))
        self.__storage.save_task(task)

    @staticmethod
    def normal_format_date(list_date):
        """Translate data to H:M d/m/Y format"""
        if type(list_date) != str:
            if len(list_date) != 2:
                raise ValueError("Incorrect format input date. Format H:M d/m/Y")
            datetime.strptime(list_date[0] + " " + list_date[1], "%H:%M %d/%m/%Y")
            return list_date[0] + " " + list_date[1]
        else:
            datetime.strptime(list_date, "%H:%M %d/%m/%Y")
            return list_date

    @staticmethod
    def check_correct_format_period(period):
        """Check period task on format m/d/H/M"""
        if period and period != "" and len(period.split("/")) != 4:
            raise ValueError("Incorrect format period. Format months/days/hours/minutes")


    def get_free_key_task(self):
        return self.__storage.get_free_key_task()

    def save_task(self, task):
        self.__storage.save_task(task)

    def get_task(self, key_task):
        return self.__storage.get_task(key_task)

    def get_all_tasks(self):
        return self.__storage.get_all_tasks()

    def get_keys_tasks(self):
        return self.__storage.get_keys_tasks()

    def get_all_users(self):
        return self.__storage.get_all_users()

    def get_user_task(self, name_user):
        return self.__storage.get_user_task(name_user)

    def save_message(self, user, message):
        self.__storage.save_message(user, message)

    def get_message_user(self, user):
        return self.__storage.get_message_user(user)

    def get_all_task_in_tree(self, key_task):
        return self.__storage.get_all_tasks_in_tree(key_task)
