from cfg import WORKSPACE_PATH
import os
from quilt.action import util


def is_cloned(uri):
    return os.path.exists(os.path.join(WORKSPACE_PATH, util.project_name_from_git_uri(uri)))


def clone(uri):
    if is_cloned(uri):
        return pull(uri, 'master')

    util.run_cmd_lis(["cd %s" % (WORKSPACE_PATH)])
    return os.system("git clone %s" % (uri)) == 0


def pull(uri, branch):
    if not is_cloned(uri):
        return clone(uri)

    util.run_cmd_lis(["cd %s" % (os.path.join(WORKSPACE_PATH, util.project_name_from_git_uri(uri))),
                      "git checkout %s" % (branch),
                      "git pull"])
    return True
