from __future__ import print_function

import pprint

import six

from .cmd_base import DoitCmdBase
from .exceptions import InvalidCommand




def my_safe_repr(obj, context, maxlevels, level):
    """pretty print supressing unicode prefix

    http://stackoverflow.com/questions/16888409/
           suppress-unicode-prefix-on-strings-when-using-pprint
    """
    typ = type(obj)
    if six.PY2 and typ is unicode:
        obj = str(obj)
    return pprint._safe_repr(obj, context, maxlevels, level)


class Info(DoitCmdBase):
    doc_purpose = "show info about a task"
    doc_usage = "TASK"
    doc_description = None

    def _execute(self, pos_args):
        if len(pos_args) != 1:
            msg = ('doit info failed, must select *one* task.'
                   '\nCheck `doit help info`.')
            raise InvalidCommand(msg)

        task_name = pos_args[0]
        # dict of all tasks
        tasks = dict([(t.name, t) for t in self.task_list])

        pp = pprint.PrettyPrinter(indent=4, stream=self.outstream)
        pp.format = my_safe_repr

        task = tasks[task_name]
        for attr in (
            'name', 'file_dep', 'task_dep', 'setup_tasks', 'calc_dep',
            'targets',
            # these fields usually contains reference to python functions
            # 'actions', 'clean', 'uptodate', 'teardown', 'title'
            'getargs', 'params', 'verbosity', 'watch'
            ):
            value = getattr(task, attr)
            # by default only print fields that have non-empty value
            if value:
                self.outstream.write('\n{0}:'.format(attr))
                pp.pprint(getattr(task, attr))
