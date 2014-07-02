#!/usr/bin/env python
import os
import json
import fileinput
import argparse
import sys
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
        self.config_file_path = config_file_path + '/' + file_name

        # TODO handle exception if the file does not exist
        with open(self.config_file_path) as config_file:
            self.config = json.load(config_file)
            todo_path = os.path.abspath(self.config['todo_path'])
            self.todo_file = todo_path + '/' + self.config['todo_file']

    def add_list(self, list_name):
        """Adds another list file to the todo_list config_file
        :list_name: the file name for the new list
        """

        with open(self.config_file_path, 'r+') as config_file:
            self.config = json.load(config_file)
            # add a default extension
            if '.' not in list_name:
                list_name = list_name + '.txt'
            if list_name not in self.config['todo_lists']:
                self.config['todo_lists'].append(list_name)

            self.config['todo_file'] = list_name
            # write back to the file
            config_file.seek(0)
            config_file.write(json.dumps(self.config, indent=4,
                                         separators=(',', ':')))
            # to delete the extra data
            config_file.truncate()

    def add_task(self, task):
        """adds a task to the list
        :task: the task(str) to be added"""

        # open file in append mode so we don't delete the previous contents
        # + ensures that if the file does not exist then create it
        with open(self.todo_file, 'a+') as todo_file:
            todo_file.write(task + '\n')

    def list_tasks(self):
        """lists all the tasks
        """
        with open(self.todo_file, 'r') as todo_file:
            for i, task in enumerate(todo_file):
                # assuming the last @ is for time
                # __ is throw away
                task, __,  time = task.rpartition('@')
                # if the string does not has time then,
                # time contains the whole string
                if not task:
                    task = time
                    time = ""
                print str(i + 1) + ' @' + time.strip() + ' ' + task

    def clear_file(self):
        """deletes the todo_file
        """
        os.remove(self.todo_file)

    def _replace_task(self, task_number, replacement="", regex=""):
        """ replaces a task with the replacement
        :task_number: the task_number to be deleted
        :replacement: the new task to be replaced
        """
        # the inplace redirects the stdout to file
        # so whatever we are printing is going there
        # after this loop file closes so we can print anything
        for i, line in enumerate(fileinput.input(self.todo_file, inplace=True)):
            if i == task_number - 1:
                if replacement:
                    if regex:
                        replacement = re.sub(regex, replacement, line, count=1).strip()
                    print replacement
                continue
            # trailing comma with print omits the new line char
            print line,

    def del_task(self, task_number):
        """ deletes a task
        :task_number: the task_number to be deleted
        """
        self._replace_task(task_number)

    def edit_task(self, task_number, replacement):
        """ edits a task and replaces it with the replacement
        :task_number: the task_number to be deleted
        """
        regex = ""
        if replacement.count('/') == 3:
            regex = r'' + replacement.split('/')[1]
            replacement = replacement.split('/')[2]
        self._replace_task(task_number, replacement, regex)


def parse_arguments(t):
    """ parses the arguments and takes an action on todo
    :t: Todo list object"""
    # if no argument is passed then just list_tasks
    if len(sys.argv) == 1:
        t.list_tasks()
        return

    t.add_task
    parser = argparse.ArgumentParser(description='Minmal Todo list... really')

    parser.add_argument(
        '-d', '--done',
        type=int,
        help="delete the task number as it is finished"
    )

    parser.add_argument(
        '--clear',
        action='store_true',
        help="clear the tasks and delete the file \
        though it should rarely be used (c'mon all tasks done really??!!)\
        "
    )

    parser.add_argument(
        '-e', '--edit',
        type=int,
        help="edit a task example t -e 1 change the boot "
    )

    parser.add_argument(
        '--add-list',
        help="add another todo list"
    )

    parser.add_argument(
        '--list',
        nargs='?',
        const=True,
        help="choses the specified list as the current list\
        or creates new if it does not exist or \
        prints the current filename if no argument is provided"
    )

    parser.add_argument(
        'task_to_add', nargs='*',
        help="if no arguments are provided then \
        all the arguments are combined and passed to add_task"
    )

    args = parser.parse_args()
    if args.add_list:
        t.add_list(args.add_list)
        return

    # don't worry it is not a keyword
    if args.list:
        # if user didn't provide any argument then just print the current file
        if type(args.list) == bool:
            print t.config['todo_file']
            return
        t.add_list(args.list)
        return
    if args.done:
        t.del_task(args.done)
        return
    if args.clear:
        t.clear_file()
        return
    if args.edit:
        t.edit_task(args.edit, ' '.join(args.task_to_add))
        return
    if args.task_to_add:
        t.add_task(' '.join(args.task_to_add))
        return


def main():
    t = Todo()
    parse_arguments(t)


if __name__ == '__main__':
    main()
