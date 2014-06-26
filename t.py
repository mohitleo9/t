#!/usr/bin/env python
import os
import json
import fileinput
import argparse
import sys


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
        """ deletes a task
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


def parse_arguments(t):
    """ parses the arguments and takes an action on todo
    :t: Todo list object
    """
    # if no argument is passed then just list_tasks
    if len(sys.argv) == 1:
        t.list_tasks()
        return

    parser = argparse.ArgumentParser(description='Minmal Todo list... really')

    parser.add_argument(
        '-d', '--delete',
        type=int,
        help="delete the task number"
    )

    parser.add_argument(
        'task_to_add', nargs='*',
        help="if no arguments are provided then \
        all the arguments are combined and passed to add_task"
    )

    args = parser.parse_args()

    if args.delete:
        t.del_task(args.delete)

    if args.task_to_add:
        t.add_task(' '.join(args.task_to_add))


def main():
    t = Todo()
    parse_arguments(t)


if __name__ == '__main__':
    main()
