#! /usr/bin/env python
import os
import json
import fileinput
import re


class Todo:

    """
    This class maintains the Todo file and all the supported methods
    """

    def __init__(self, config_file_path=None):
        """This takes in a config file (json) parses it
        and does the initilization

        :config_file_path: it takes in a path to config_file
           - (default cwd/tconfig.json)
        """

        if not config_file_path:
            config_file_path = os.getcwd()
        file_name = 'tconfig.json'
        full_file_path = config_file_path + '/' + file_name

        # TODO handle exception if the file does not exist
        with open(full_file_path) as config_file:
            self.config = json.load(config_file)
            todo_path = os.path.abspath(self.config['todo_path'])
            self.todo_file = todo_path + '/' + self.config['todo_file']

    def add_task(self, task):
        """adds a task to the list

        :task: the task(str) to be added
        """

        # open file in append mode so we don't delete the previous contents
        # + ensures that if the file does not exist then create it
        with open(self.todo_file, 'a+') as todo_file:
            todo_file.write(task + '\n')

    def list_tasks(self):
        """lists all the tasks
        """
        with open(self.todo_file, 'r') as todo_file:
            for i, task in enumerate(todo_file):
                print str(i + 1) + ' ' + task,

    def del_task(self, task_number):
        """delete a task

        :task_number: the task_number to be deleted
        """
        # the inplace redirects the stdout to file
        # so whatever we are printing is going there
        # after this loop file closes so we can print anything
        for i, line in enumerate(fileinput.input(self.todo_file, inplace=True)):
            if i == task_number - 1:
                continue
            # trailing comma with print omits the new line char
            print line,


def main():
    t = Todo()


if __name__ == '__main__':
    main()
