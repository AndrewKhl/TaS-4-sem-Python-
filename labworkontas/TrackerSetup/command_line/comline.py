import os
import argparse

import command_line.console_output as cons_out
from tracker.logger import Logger
from command_line.config import Config


def create_parser():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest='command', description='Choose object/action for work', metavar='')

    user = subparser.add_parser('user', help='To work with users')
    user_parser = user.add_subparsers(dest='action', help='Methods for work with users', metavar='')
    create_user_parser(user_parser)

    task = subparser.add_parser('task', help='To work with tasks')
    task_parser = task.add_subparsers(dest='action', help='Methods for work with tasks', metavar='')
    create_task_parser(task_parser)

    logger = subparser.add_parser('logger', help='To work with logger')
    logger_parser = logger.add_subparsers(dest='action', help='Methods for work with logger', metavar='')
    create_logger_parser(logger_parser)

    member = subparser.add_parser('member', help='''To work with member in task. Member its user 
    who can view the task, but not changed it''')

    member_parser = member.add_subparsers(dest='action', help='''Methods for work with member in task. Member its user
    who can view the task, but not changed it''', metavar='')
    create_member_parser(member_parser)

    admin = subparser.add_parser('admin', help='''To work with admins in task. Admins its user
    who can view and changed task''')

    admin_parser = admin.add_subparsers(dest='action', help='''Methods for work with admins in task. Admins its user
    who can view and changed task''', metavar='')
    create_admin_parser(admin_parser)

    link = subparser.add_parser('link', help='''To work with link between tasks. Related task know
    information about each other''')
    link_parser = link.add_subparsers(dest='action', help='''Methods for work with link. Related task know
    information about each other''', metavar='')
    create_link_parser(link_parser)

    subparser.add_parser('project', help='Outputs the task with its subtasks, their members and admins')
    subparser.add_parser('mytasks', help='Output current user tasks')
    subparser.add_parser('mymessages', help='Output current user messages')
    subparser.add_parser('config', help="Open file configurations library tracker in gedit.\n"
                                        "      Lines in file:\n"
                                        " 0: path to logger records\n"
                                        " 1: path to file with task\n"
                                        " 2: path to file with messages\n"
                                        " 3: status logger ON/OFF (logger = ON/OFF)\n"
                         "(To see more information read doc. tracker.config)\n")

    return parser


def create_user_parser(parser):
    user_view = parser.add_parser('view', help='View information about user')
    user_view.add_argument('-n', '--name_user', default='all', help='Output user for given name (default = all users)')

    user_delete = parser.add_parser('delete', help='Removes user from tasks. (if is mentioned how admin or member)')
    user_delete.add_argument('name_user', default=None, help='Deleted user for given name')

    user_i = parser.add_parser('i', help='Authentication user')
    user_i.add_argument('name_user', default=None, help='Name user authentication')

    user_message = parser.add_parser('message', help='''Designed to display messages and notifications associated 
    with the selected user''')
    user_message.add_argument('name_user', default=None, help='Name displaying user')

    parser.add_parser('who', help='Display information about current user')


def create_member_parser(parser):
    member_add = parser.add_parser('add', help='Adds member to task')
    member_add.add_argument('key_task', default=None, help='Key task')
    member_add.add_argument('name_user', default=None, help="Name added user")

    member_delete = parser.add_parser('delete', help='Removes member to task')
    member_delete.add_argument('key_task', default=None, help='Key task')
    member_delete.add_argument('name_user', default=None, help="Name removed user")


def create_admin_parser(parser):
    admin_add = parser.add_parser('add', help='Adds admin to task')
    admin_add.add_argument('key_task', default=None, help='Key task')
    admin_add.add_argument('name_user', default=None, help='Name added user')

    admin_delete = parser.add_parser('delete', help='Removes admin to task')
    admin_delete.add_argument('key_task', default=None, help='Key task')
    admin_delete.add_argument('name_user', default=None, help='Name removed user')


def create_link_parser(parser):
    link_add = parser.add_parser('add', help='Adds link between task')
    link_add.add_argument('key_first', default=None, help='Key first task')
    link_add.add_argument('key_second', default=None, help="Key linked task")

    link_delete = parser.add_parser('delete', help='Removes link between task')
    link_delete.add_argument('key_first', default=None, help='Key first task')
    link_delete.add_argument('key_second', default=None, help="Key linked task (if all, remover all links this task")

    link_view = parser.add_parser('view', help='View all linked tasks')
    link_view.add_argument('key_task', default=None, help='Key task with links')


def create_task_parser(parser):
    task_add = parser.add_parser('add', help='Adds task to database')
    task_add.add_argument('--to', default='user', choices=['user', 'task'], required=True,
                          help='Adds task to user or task')
    task_add.add_argument('key_or_name', default=None, help='Name user or key task witch task was added')
    task_add.add_argument('-n', '--name', default='unnamed', help='Set name task (default = unnamed)')
    task_add.add_argument('--priority', default=3, type=int, choices=[1, 2, 3, 4, 5], help='''Set priority task 
    (default = 3)''')
    task_add.add_argument('--period', default='', help='Change period task. Format (mount/days/hour/minutes)')
    task_add.add_argument('--start', nargs='*', default=None, help='''Set start time task 
    (default = current time). Format H:M dd/mm/YY''')
    task_add.add_argument('--end', nargs='*', default=None, help='''Set end time task. Format H:M dd/mm/YY''')
    task_add.add_argument('--status', default='', type=str, choices=['', 'waiting', 'process', 'ended'],
                          help='Set status task')
    task_add.add_argument('-t', '--type', default='', help='Set any convenient type of task')

    task_view = parser.add_parser('view', help='View information about task')
    task_view.add_argument('-k', '--key_task', default='all', help='Output information about task (default = all tasks)')

    task_del = parser.add_parser('delete', help='Removes task from database')
    task_del.add_argument('key_task', default=None, help='Removes task for given key')

    task_end = parser.add_parser('finish', help='Marks task as complete')
    task_end.add_argument('key_task', default=None, help='Complete task for given key')

    task_change = parser.add_parser('change', help='Change the task public fields')
    task_change.add_argument('key_task', default=None, help='Key changed task')
    task_change.add_argument('-n', '--name', default=None, help='Change name task')
    task_change.add_argument('-p', '--priority', default=None, choices=[1, 2, 3, 4, 5], type=int,
                             help='Change priority task')
    task_change.add_argument('--period', default=None, help='Change period task. Format (mount/days/hour/minutes)')
    task_change.add_argument('-st', '--start', nargs='*', default=None,
                             help='Change start time task. Format H:M dd/mm/YY')
    task_change.add_argument('-et', '--end', nargs='*', default=None, help='Change end time task. Format H:M dd/mm/YY)')
    task_change.add_argument('--status', default=None, choices=['', 'waiting', 'process', 'ended'],
                             help='Set new status task')
    task_change.add_argument('-t', '--type', default=None, help='Change type of task')


def create_logger_parser(parser):
    parser.add_parser('on', help='Enabling logging')
    parser.add_parser('off', help='Disabling logging')

    logger_view = parser.add_parser('view', help='Output logger')
    logger_view.add_argument('what', default='all', choices=['all', 'actions', 'errors', 'login', ''],
                             help='Output information of different actions')


def run_user(parser, namespace, my_logger=None):
    action = namespace.action
    if action == 'delete':
        cons_out.remove_user(namespace.name_user)
    elif action == 'i':
        cons_out.new_current_user(namespace.name_user)
    elif action == 'who':
        cons_out.current_user(my_logger)
    elif action == 'message':
        cons_out.view_messages_user(namespace.name_user)
    elif action == 'view':
        if namespace.name_user == 'all':
            cons_out.view_all_users()
        else:
            cons_out.view_task_user(namespace.name_user)
    else:
        parser._subparsers._group_actions[0].choices['user'].print_help()


def run_task(parser, namespace):
    action = namespace.action
    if action == 'add':
        if namespace.to == 'user':
            cons_out.add_task(namespace.key_or_name, None, namespace.name, namespace.status, namespace.priority, namespace.start,
                              namespace.end, namespace.period, namespace.type)
        else:
            cons_out.add_task(None, namespace.key_or_name, namespace.name, namespace.status, namespace.priority, namespace.start,
                              namespace.end, namespace.period, namespace.type)
    elif action == 'change':
        cons_out.change_task(namespace.key_task, namespace.name, namespace.priority, namespace.period, namespace.start,
                             namespace.end, namespace.status, namespace.type)
    elif action == 'delete':
        cons_out.delete_task(namespace.key_task)
    elif action == 'end':
        cons_out.finish_task(namespace.key_task)
    elif action == 'view':
        if namespace.key_task == 'all':
            cons_out.view_all_tasks()
        else:
            cons_out.view_task(namespace.key_task)
    else:
        parser._subparsers._group_actions[0].choices['task'].print_help()


def run_logger(parser, namespace, my_logger):
    action = namespace.action
    if action == 'on':
        cons_out.change_status_logger('ON')
    elif action == 'off':
        cons_out.change_status_logger('OFF')
    elif action == 'view':
        if namespace.what == 'all':
            cons_out.view_logger_output(my_logger)
        elif namespace.what == 'actions':
            cons_out.view_logger_output(my_logger, 'DEBUG')
        elif namespace.what == 'errors':
            cons_out.view_logger_output(my_logger, 'ERROR')
        elif namespace.what == 'login':
            cons_out.view_logger_output(my_logger, 'INFO')
    else:
        parser._subparsers._group_actions[0].choices['logger'].print_help()


def run_member(parser, namespace):
    action = namespace.action
    if action == 'add':
        cons_out.add_member(namespace.key_task, namespace.name_user)
    elif action == 'delete':
        cons_out.remove_member(namespace.key_task, namespace.name_user)
    else:
        parser._subparsers._group_actions[0].choices['member'].print_help()


def run_admin(parser, namespace):
    action = namespace.action
    if action == 'add':
        cons_out.add_admin(namespace.key_task, namespace.name_user)
    elif action == 'delete':
        cons_out.remove_admin(namespace.key_task, namespace.name_user)
    else:
        parser._subparsers._group_actions[0].choices['admin'].print_help()


def run_link(parser, namespace):
    action = namespace.action
    if action == 'add':
        cons_out.add_link(namespace.key_first, namespace.key_second)
    elif action == 'delete':
        if namespace.key_second == 'all':
            cons_out.removed_all_links(namespace.key_first)
        else:
            cons_out.removed_link(namespace.key_first, namespace.key_second)
    elif action == 'view':
        cons_out.view_all_linked_tasks(namespace.key_task)
    else:
        parser._subparsers._group_actions[0].choices['link'].print_help()


def run_namespace(parser, my_logger=None):
    namespace = parser.parse_args()

    if namespace.command == 'user':
        run_user(parser, namespace, my_logger)
    elif namespace.command == 'task':
        run_task(parser, namespace)
    elif namespace.command == 'project':
        cons_out.view_all_project()
    elif namespace.command == 'logger':
        run_logger(parser, namespace, my_logger)
    elif namespace.command == 'member':
        run_member(parser, namespace)
    elif namespace.command == 'link':
        run_link(parser, namespace)
    elif namespace.command == 'admin':
        run_admin(parser, namespace)
    elif namespace.command == 'mytasks':
        cons_out.my_tasks(my_logger)
    elif namespace.command == 'mymessages':
        cons_out.my_messages(my_logger)
    elif namespace.command == 'config':
        cons_out.open_configuration_in_gedit()
    else:
        parser.print_help()


def main():
    Config.set_new_config_path(os.path.dirname(__file__) + '/configuration.txt')
    my_logger = Logger(path_to_logger_output=Config.get_logger_output_path())

    if Config.get_status_logger():
        my_logger.on_logger()
    else:
        my_logger.off_logger()

    parser = create_parser()
    run_namespace(parser, my_logger)


if __name__ == '__main__':
    main()
