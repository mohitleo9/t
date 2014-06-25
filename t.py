#! /usr/bin/env python
import os
import json
import fileinput


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
            self.todo_path = os.path.abspath(self.config['todo_path'])
            self.todo_file = self.todo_path + '/' + self.config['todo_file']

    def add_task(self, task):
        """adds a task to the list

        :task: the task(str) to be added
        """
        # open file in write append mode
        # + ensures that if the file does not exist then create it
        with open(self.todo_file, 'a+') as todo_file:
            todo_file.write(task + '\n')

    def del_task(self, task):
        """delete a task

        :task: search the task to be deleted
        """
        task = task + '\n'
        # the inplace redirects the stdout to file
        # so whatever we are printing is going there
        # after this loop file closes so we can print anything
        for line in fileinput.input(self.todo_file, inplace=True):
            if task == line:
                continue
            # trailing comma with print omits the new line char
            print line,


def main():
    t = Todo()
    t.del_task('aaasdf')


if __name__ == '__main__':
    main()
