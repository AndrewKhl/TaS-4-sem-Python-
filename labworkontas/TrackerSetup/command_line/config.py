"""
This module contains a class for loading, applying and saving all program settings

Public class:

'Config': Is intended for reading and applying program settings
"""

import os
from pathlib import Path


class Config:
    """
    Is intended for reading and applying program settings with file configuration.txt

    Public Constant:

    'LIBRARY_PATH': contains the path to the installed program folder

    Private Attributes:

    '__configuration_file_path': contains the path to the configuration program
    '__LOGGER_OUTPUT_PATH': contains the path to the history login users in program
    '__DATABASE_FOLDER_PATH': contains the path folder with information about tasks and messages

    Public Methods:

    'load_dirs': read information on configuration.txt file
    'check_file_path': check file on exist
    'get_config_path': return path on configuration file
    'set_config_path': set new path for configuration file
    'get_task_file': return path on file with tasks
    'get_messages_file': return path on file with user messages
    'get_logger_output_path': return path on file with logger output
    'get_status_logger': return status logger
    'get_status_logger': return status logger
    'set_status_logger': set new status logger

    Default work file: configuration.txt

    Lines in file:
    0: path to logger records
    1: path to file with task
    2: path to file with messages
    3: status logger ON/OFF (logger = ON/OFF)

    P.S. If records in configurations file was just name file, then work path was 'default directory' + 'name file'.
    ('default directory' for logger records=/logger_output, for task and messages=/database), else if records was
    directory, then work path was 'directory with file'.
    """

    LIBRARY_PATH = os.path.dirname(__file__)
    __configuration_file_path = LIBRARY_PATH + '/configuration.txt'
    __LOGGER_OUTPUT_PATH = LIBRARY_PATH + '/logger_output/'
    __DATABASE_FOLDER_PATH = LIBRARY_PATH + '/database/'

    @classmethod
    def load_dirs(cls):
        """ Load information of program and all settings with configuration.txt
        If file not found, create it.
        If some path is not specified, applies it for it default values
        Return list with paths to files

        :return
        'work_dirs': list with different path tos files
        """
        work_dirs = [None] * 4  # config include 4 settings: path for tasks, messages, output logger and status logger

        if Path(cls.__configuration_file_path).is_file():
            with open(cls.__configuration_file_path, 'r') as file:
                i = 0
                for line in file:
                    work_dirs[i] = line[:-1]
                    i += 1

        if not work_dirs[0]:
            work_dirs[0] = 'logger_output.txt'  # default for logger_output file
        if not work_dirs[1]:
            work_dirs[1] = 'new_tasks.txt'  # default for tasks file
        if not work_dirs[2]:
            work_dirs[2] = 'messages.txt'  # default for messages file
        if not work_dirs[3]:
            work_dirs[3] = 'logger = ON'

        return work_dirs

    @classmethod
    def check_file_path(cls, path):
        """ Check file on exist, if file not found create it

        :param
        'path': path checked file

        :return: path file
        """
        if not os.path.exists(cls.__DATABASE_FOLDER_PATH):
            os.makedirs(cls.__DATABASE_FOLDER_PATH)

        if not os.path.exists(cls.__LOGGER_OUTPUT_PATH):
            os.makedirs(cls.__LOGGER_OUTPUT_PATH)

        if not Path(path).is_file():
            with open(path, 'w'):
                pass

        return path

    @classmethod
    def get_logger_output_path(cls):
        """ Return path file with logger output"""
        work_dirs = cls.load_dirs()
        if work_dirs[0].find('/') == -1:
            return cls.check_file_path(cls.__LOGGER_OUTPUT_PATH + str(work_dirs[0]))
        else:
            return cls.check_file_path(work_dirs[0])

    @classmethod
    def get_tasks_file(cls):
        """ Return path file with tasks"""
        work_dirs = cls.load_dirs()
        if work_dirs[1].find('/') == -1:
            return cls.check_file_path(cls.__DATABASE_FOLDER_PATH + str(work_dirs[1]))
        else:
            return cls.check_file_path(work_dirs[1])

    @classmethod
    def get_messages_file(cls):
        """ Return path file with messages"""
        work_dirs = cls.load_dirs()
        if work_dirs[2].find('/') == -1:
            return cls.check_file_path(cls.__DATABASE_FOLDER_PATH + str(work_dirs[2]))
        else:
            return cls.check_file_path(work_dirs[2])

    @classmethod
    def get_config_path(cls):
        """ Return path configuration file"""
        cls.load_dirs()
        return cls.__configuration_file_path

    @classmethod
    def set_new_config_path(cls, new_path):
        """Set new path for configuration file. Default this library/configuration.txt"""
        cls.__configuration_file_path = new_path

    @classmethod
    def get_status_logger(cls):
        """Return status logger (ON/OFF). Default status = ON

        :raise
        'Exeption": if status not equal ON/OFF
        """
        work_dirs = cls.load_dirs()
        if len(work_dirs[3].split()) == 3 and work_dirs[3].split()[2] == 'ON':
            return True
        elif len(work_dirs[3].split()) == 3 and work_dirs[3].split()[2] == 'OFF':
            return False
        else:
            Exception('Incorrect status logger')

    @classmethod
    def set_status_logger(cls, status):
        """Set status logger (ON/OFF). Default status = ON"""
        work_dirs = cls.load_dirs()
        if status == 'OFF':
            work_dirs[3] = 'logger = OFF'
        else:
            work_dirs[3] = 'logger = ON'

        cls.save_changes(work_dirs)

    @classmethod
    def save_changes(cls, work_dirs):
        """ Save new settings program. Default file = configuration.txt

        :param
        'work_dirs': settings to save file
        """
        with open(cls.__configuration_file_path, 'w') as file:
            for line in work_dirs:
                file.write(line + '\n')
