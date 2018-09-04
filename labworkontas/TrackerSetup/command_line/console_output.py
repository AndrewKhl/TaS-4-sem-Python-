import os
from collections import deque
from datetime import datetime


from tracker.manager import Manager
from tracker.logger import Logger
from tracker.base import Task
from command_line.config import Config


def view_task(key_task):
    """Output information about task"""

    manager = Manager(Config.get_tasks_file(), Config.get_messages_file())

    task = manager.get_task(key_task)

    if not task:
        print("No task with this key!")
        return

    print('Name: ' + task.name)
    print('Number: ' + str(task.key))
    print('Status: ' + task.status)
    print('Type: ' + str(task.type_task))
    print('Priority: ' + str(task.priority))
    print('Parent task: ' + str(task.parent))
    print('Name host: ' + task.host)

    print('Link tasks: ' + str(len(task.links)))
    if len(task.links):
        string = ''
        for i in task.links:
            string += i + ' '
        print('Number link tasks: ' + string)

    print('Count subtasks: ' + str(len(task.subtasks)))
    if len(task.subtasks):
        string = ''
        for i in task.subtasks:
            string += i + ' '
        print('Numbers subtask: ' + string)

    print('Count admins: ' + str(len(task.admins)))
    if len(task.admins):
        string = ''
        for i in task.admins:
            string += i + ' '
        print('Admins: ' + string)

    print('Count members: ' + str(len(task.members)))
    if len(task.members):
        string = ''
        for i in task.members:
            string += i + ' '
        print('Members: ' + string)

    print("Create time: " + task.create_time)
    print("Start time: " + str(task.start_time))
    print("Change time: " + str(task.change_time))
    print("End time: " + str(task.end_time))
    print("Period: ", end="")
    if task.period and task.period != "":
        periods = task.period.split("/")
        print("month={0} days={1} hour={2} minutes={3}".format(periods[0], periods[1], periods[2], periods[3]))
    print("\n")
    manager.save_task(task)


def view_all_users():
    """Output name all users mentioned in Task.admins and Task.members"""

    manager = Manager(Config.get_tasks_file(), Config.get_messages_file())

    users = manager.get_all_users()
    if users:
        for user in users:
            print(user)
    else:
        print("No users")


def view_task_user(name_user, more_information=False):
    """View all task when thiw user was mentioned. If view=True displays more information about task"""

    manager = Manager(Config.get_tasks_file(), Config.get_messages_file())
    tasks = manager.get_user_task(name_user)

    if tasks:
        admin_task = []
        member_task = []
        for task in tasks:
            if name_user in task.admins:
                admin_task.append(task.key)
            if name_user in task.members:
                member_task.append(task.key)
            manager.save_task(task)

        print("Admin in tasks: ")
        for key_task in admin_task:
            print(key_task, end=" ")
        print("\nMember in task: ")
        for key_task in member_task:
            print(key_task, end=" ")

        if more_information:
            print("\n")
            priority_tasks = []
            for key_task in set(admin_task + member_task):
                priority_tasks.append(manager.get_task(key_task))
            for task in sorted(priority_tasks, key=lambda x: x.priority, reverse=True):
                manager.save_task(task)
                view_task(task.key)
        print()
    else:
        print("No task this user")


def view_messages_user(name_user):

    manager = Manager(Config.get_tasks_file(), Config.get_messages_file())

    messages = manager.get_message_user(name_user)
    if messages:
        for mes in messages:
            print(mes)
    else:
        not_found_user(name_user)


def remove_user(name_user):

    manager = Manager(Config.get_tasks_file(), Config.get_messages_file())

    tasks = manager.get_user_task(name_user)
    if tasks:
        for task in tasks:
            if name_user in task.admins:
                task.admins.remove(name_user)
            if name_user in task.members:
                task.members.remove(name_user)
            manager.save_task(task)
        print("User '{0}' was removed".format(name_user))
    else:
        not_found_user(name_user)


def view_all_tasks():

    manager = Manager(Config.get_tasks_file(), Config.get_messages_file())

    tasks = manager.get_all_tasks()
    if tasks:
        for task in tasks:
            print(task)
            manager.save_task(task)
    else:
        print("No tasks")


def delete_task(key_task):
    try:

        manager = Manager(Config.get_tasks_file(), Config.get_messages_file())

        manager.delete_task(key_task)
        print("Task N{0} and subtasks was removed".format(key_task))
    except Exception as e:
        print(e)


def add_task(name_user, key_parent, name_task, status, priority_task, time_start, time_end, period, type_task):  # ok
    try:

        if time_start:
            time_start = normal_format_date(time_start)
        else:
            time_start = datetime.now().strftime("%H:%M %d/%m/%Y")

        if time_end:
            time_end = normal_format_date(time_end)
            if datetime.strptime(time_start, "%H:%M %d/%m/%Y") >= datetime.strptime(time_end, "%H:%M %d/%m/%Y"):
                raise Exception("Start time later then end time")
        else:
            time_end = ""

        check_correct_format_period(period)

        manager = Manager(Config.get_tasks_file(), Config.get_messages_file())

        task = Task(key_parent, name_task, name_user, priority_task,
                    status, time_start, time_end, period, type_task)
        manager.add_task(task)
        print("Task N{0} was added".format(task.key))
    except ValueError as ve:
        print(ve)
    except Exception as e:
        print(e)


def change_task(key_task, *args):
    """args and params = name, priority, period, start_time, end_time, status, type_task"""
    try:

        manager = Manager(Config.get_tasks_file(), Config.get_messages_file())

        task = manager.get_task(key_task)

        if task:

            params_task = task.get_changed_task_params()
            for i in range(0, len(params_task)):
                if args[i]:
                    params_task[i] = args[i]

            params_task[3] = normal_format_date(params_task[3])
            if params_task[4] != "":
                params_task[4] = normal_format_date(params_task[4])

                if datetime.strptime(params_task[3], "%H:%M %d/%m/%Y") >= datetime.strptime(params_task[4], "%H:%M %d/%m/%Y"):
                    raise Exception("Start time later then end time")

            check_correct_format_period(params_task[2])  # param_task[2] this is period task
            manager.save_task(task)
            manager.set_new_params_task(key_task, params_task)
            print("Params task N{0} was changed".format(key_task))
    except ValueError as ve:
        print(ve)
    except Exception as e:
        print(e)


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


def check_correct_format_period(period):
    """Check period task on format m/d/H/M"""
    if period and period != "" and len(period.split("/")) != 4:
        raise ValueError("Incorrect format period. Format months/days/hours/minutes")


def finish_task(key_task):
    """Set status task = ended"""

    manager = Manager(Config.get_tasks_file(), Config.get_messages_file())

    task = manager.get_task(key_task)
    if task:
        task.status = "ended"
        print("Task N{0} was completed".format(key_task))
        manager.save_task(task)
    else:
        not_found_task(key_task)


def new_current_user(name_user):
    """Login user in system"""
    Logger.enter(name_user)
    print("Hello, {0}".format(name_user))


def current_user(logger):
    """Check user in system"""
    name_user = logger.get_name_last_login_user()
    if name_user:
        print("Current user: {0}".format(name_user))
    else:
        print("Please, login in system")


def my_tasks(logger):
    name_user = logger.get_name_last_login_user()
    if name_user:
        view_task_user(name_user, True)
    else:
        print("Please, login in system")


def my_messages(logger):
    name_user = logger.get_name_last_login_user()
    if name_user:
        view_messages_user(name_user)
    else:
        print("Please, login in system")


def not_found_user(key_user):
    print("User with name '{0}' not found!".format(key_user))


def not_found_task(key_task):
    print("Task with key N{0} not found!".format(key_task))


def error_data():
    print("Incorrect input data")


def view_all_project():
    """Ouput information each task with its sutasks, admins and members"""

    manager = Manager(Config.get_tasks_file(), Config.get_messages_file())

    keys_tasks = manager.get_keys_tasks()
    if keys_tasks:
        number_project = 0
        for key_task in keys_tasks:
            task = manager.get_task(key_task)
            if not task.parent:
                q = deque()
                q.append(task)
                list_tasks_project = [task]
                queue_on_project(q, list_tasks_project, manager)
                number_project += 1
                print("Project N" + str(number_project))
                admins = set()
                members = set()
                for project_task in list_tasks_project:
                    for user in project_task.admins:
                        admins.add(user)
                    for user in project_task.members:
                        members.add(user)
                print("Admins:")
                for admin in admins:
                    print(admin, end=" ")
                print("\nMembers:")
                for member in members:
                    print(member, end=" ")
                print("\n\nTasks:")
                for project_task in list_tasks_project:
                    print(project_task)
                print("\n")
            manager.save_task(task)
    else:
        print("No projects")


def queue_on_project(q, list_tasks_project, manager):
    """Recursive function for collection all tasks this project in list(use BFS)

    :param
    q: queue with unvisited tasks
    list_tasks_tree: list with subtasks select task
    """
    if not len(q):
        return
    else:
        task = q.popleft()
        for key_sub in task.subtasks:

            sub = manager.get_task(key_sub)
            list_tasks_project.append(sub)
            q.append(sub)
            manager.save_task(sub)

        queue_on_project(q, list_tasks_project, manager)


def change_status_logger(status):
    """ON/OFF logger"""
    Config.set_status_logger(status)
    print("Status logger was changed on {}".format(status))


def view_logger_output(logger, level=None):
    """View logger records with level = 'INFO', 'DEBUG', 'ERROR'"""

    if not level:
        messages = logger.get_all_logger_output_messages()
    else:
        messages = logger.get_logger_output_with_level(level)

    if not messages:
        print("Logger records not found")
    else:
        for line in messages:
            print(line)


def add_member(key_task, name_user):
    try:
        manager = Manager(Config.get_tasks_file(), Config.get_messages_file())

        manager.add_member_in_task(key_task, name_user)
        print("User '{0}' was added how member to task N{1}".format(name_user, key_task))
    except Exception as e:
        print(e)


def remove_member(key_task, name_user):
    try:
        manager = Manager(Config.get_tasks_file(), Config.get_messages_file())

        manager.delete_member_in_task(key_task, name_user)
        print("User '{0}' was removed how member to task N{1}".format(name_user, key_task))
    except Exception as e:
        print(e)


def add_admin(key_task, name_user):
    try:
        manager = Manager(Config.get_tasks_file(), Config.get_messages_file())

        manager.add_admin_in_task(key_task, name_user)
        print("User '{0}' was added how admin to task N{1}".format(name_user, key_task))
    except Exception as e:
        print(e)


def remove_admin(key_task, name_user):
    try:
        manager = Manager(Config.get_tasks_file(), Config.get_messages_file())

        manager.delete_admin_in_task(key_task, name_user)
        print("User '{0}' was removed how admin to task N{1}".format(name_user, key_task))
    except Exception as e:
        print(e)


def add_link(key_first_task, key_second_task):
    try:
        manager = Manager(Config.get_tasks_file(), Config.get_messages_file())

        manager.add_link(key_first_task, key_second_task)
        print("Link between task N{0} and N{1} was added".format(key_first_task, key_second_task))
    except Exception as e:
        print(e)


def removed_link(key_first_task, key_second_task):
    try:
        manager = Manager(Config.get_tasks_file(), Config.get_messages_file())

        manager.delete_link(key_first_task, key_second_task)
        print("Link between task N{0} and N{1} was removed".format(key_first_task, key_second_task))
    except Exception as e:
        print(e)


def removed_all_links(key_task):
    try:
        manager = Manager(Config.get_tasks_file(), Config.get_messages_file())

        task = manager.get_task(key_task)
        if not task:
            raise Exception("Task N{0} not found in file".format(key_task))
        linked_task = task.links.copy()
        manager.save_task(task)
        for link in linked_task:
            removed_link(key_task, link)
    except Exception as e:
        print(e)


def view_all_linked_tasks(key_task):
    try:
        manager = Manager(Config.get_tasks_file(), Config.get_messages_file())

        task = manager.get_task(key_task)
        if not task:
            raise Exception("Task N{0} not found in file".format(key_task))
        linked_task = task.links.copy()
        manager.save_task(task)
        view_task(key_task)
        for link in linked_task:
            view_task(link)
    except Exception as e:
        print(e)


def open_configuration_in_gedit():
    try:
        with open(Config.get_config_path(), 'r'):
            pass
        os.system("gedit {0}".format(Config.get_config_path()))
    except:
        print("File {} not found".format(Config.get_config_path()))

