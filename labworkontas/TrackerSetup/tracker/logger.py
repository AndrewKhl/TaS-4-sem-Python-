"""
Module stores a class called a logger that logs messages about user logins, errors, and various actions

Public Class:

'Logger': Is intended for recording messages about all actions with the program
"""

import os
import logging


class Logger:
    """
    Is intended for recording messages about all actions with the program

    Public Methods:

    'add_handler': set new handler logger or use default
    'get_logger': return logger with name 'tracker'
    'add': write actions in program (logger records with level 'DEBUG')
    'error': write errors in program (logger records with level 'ERROR')
    'login': write login in program (logger records with level 'INFO')
    'get_logger_output_with_level': return logger records with different levels (DEBUG, ERROR, INFO)
    'get_all_logger_output_message': return logger records with all levels
    'get_name_last_login_user': return name last login user in system


    Constant:

    '__DEFAULT_PATH_TO_LOGGER_OUTPUT' = __file__ + '/logger_output.txt'
    """

    __DEFAULT_PATH_TO_LOGGER_OUTPUT = os.path.dirname(__file__) + '/logger_output.txt'

    def __init__(self, path_to_logger_output=None, handler=None):
        if path_to_logger_output:
            self.path_to_logger_output = path_to_logger_output
        else:
            self.path_to_logger_output = self.__DEFAULT_PATH_TO_LOGGER_OUTPUT

        self.add_handler(handler)

    def add_handler(self, new_handler=None):
        """Set library logger new fileHandler. If fileHandler == None, sets default settings

        Default settings:
        logger.setLevel = 'DEBUG'
        path logger output for FileHandler in configuration file
        setFormatter = 'time' - 'level logging' - 'message'

        :param
        'new_handler': object types logging.FileHandler created outside
        """
        logger = logging.getLogger('tracker')
        logger.setLevel(logging.DEBUG)

        if not new_handler:
            fh = logging.FileHandler(self.path_to_logger_output)
            fh.setLevel(logging.DEBUG)
            fh.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s - %(pathname)s - %(lineno)s'))
            logger.addHandler(fh)
        else:
            if type(new_handler) != logging.FileHandler:
                raise Exception("Param new_handler not type logging.FileHandler")
            logger.addHandler(new_handler)

    def on_logger(self):
        logger = self.get_logger()
        logger.disabled = False

    def off_logger(self):
        logger = self.get_logger()
        logger.disabled = True

    @classmethod
    def get_logger(cls):
        """Return library logger with name 'tracker'"""
        return logging.getLogger('tracker')

    @classmethod
    def enter(cls, key_user):
        """Write login in file (default=logger_ouput.txt))

        :param
        'messages': message to write to file
        """
        cls.get_logger().info('User {0} login the system'.format(key_user))

    def get_logger_output_with_level(self, level_logging):
        """Return records logger for a given level logging ('INFO", 'DEBUG', 'ERROR')
        The read file is specified in the configuration file. (default=logger_ouput.txt)

        :return: list of messages
        """
        messages = []

        with open(self.path_to_logger_output) as file:
            for line in file:
                if len(line.split()) > 4 and line.split()[3] == level_logging:
                    messages.append(line[:-1])

        return messages

    def get_all_logger_output_messages(self):
        """Return records all actions in program
        The read files is specified in the configuration file. (default=logger_output.txt)

        :return: list of messages
        """
        messages = []

        with open(self.path_to_logger_output) as file:
            for line in file:
                messages.append(line[:-1])

        return messages

    def get_name_last_login_user(self):
        """Returns the name of the last user logged in.
        The read file is specified in the configuration file. (default=logger_output.txt)

        :return: name user or None, if this does not exit
        """
        last_message = None

        with open(self.path_to_logger_output) as file:
            for line in file:
                if len(line.split()) > 4 and line.split()[3] == 'INFO':
                    last_message = line

        if last_message:
            return last_message.split()[6]
        else:
            return None

