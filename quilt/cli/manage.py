import shutil

from cfg import CWD, RESOURCES_PATH, WORKSPACE_PATH, CHERRYPY_PORT
from cherrypy import wsgiserver
import os
from manager import Manager
from quilt.app import Base, db
from quilt.action import util
from quilt.web import app


manager = Manager()


@manager.command
def reset(confirm):
    """
    Dangerous! Deletes and re-initializes the sqlite DB.
    To use, call the command with the confirm arg as "True"
    :return:
    """
    if confirm == "True":
        util.run_cmd_lis([
            "rm -f %s" % (os.path.join(CWD, "state.db")),
        ])
        init()
        return "Done."
    else:
        return "Please confirm."


@manager.command
def init():
    Base.metadata.create_all(db)
    print "Initialized DB.."

    try:
        shutil.rmtree(RESOURCES_PATH)
    except: pass

    os.mkdir(RESOURCES_PATH)
    os.mkdir(WORKSPACE_PATH)
    print "Created ./resources/*"

    return True


@manager.command
def is_repo_cloned(uri):
    """
    Checks if a repo is already cloned in the workspace

    Some examples of URI:
    * git@bitbucket.org:gom-vpn/gom-provider-dockerfile.git
    * https://github.com/fgrehm/vagrant-lxc.git
    * git@github.com:fgrehm/vagrant-lxc.git
    """
    return os.path.exists(os.path.join(WORKSPACE_PATH, util.project_name_from_git_uri(uri)))


@manager.command
def clone_from_repo(uri):
    if is_repo_cloned(uri):
        return pull_from_repo(uri)

    util.run_cmd_lis(["cd %s" % (WORKSPACE_PATH),
                      "git clone %s" % (uri)])
    return True


@manager.command
def pull_from_repo(uri, branch):
    if not is_repo_cloned(uri):
        return clone_from_repo(uri)

    util.run_cmd_lis(["cd %s" % (os.path.join(WORKSPACE_PATH, util.project_name_from_git_uri(uri))),
                      "git checkout %s" % (branch),
                      "git pull"])
    return True


@manager.command
def build_image(uri, repo_image, tag):
    util.run_cmd_lis(["cd %s" % (os.path.join(WORKSPACE_PATH, util.project_name_from_git_uri(uri)))])
    return os.system('docker pull %s:%s' % (repo_image, tag)) == 0


@manager.command
def login_to_docker(username, email, passwd):
    return os.system('docker login -e %s -p %s -u %s' % (email, passwd, username)) == 0


@manager.command
def push_docker_image(repo_image, tag):
    return os.system('docker pull %s:%s' % (repo_image, tag)) == 0


@manager.command
def run():
    app.debug = True
    app.run(host='0.0.0.0', port=5001)


@manager.command
def deploy():
    app.debug = True
    app.run(host='0.0.0.0', port=80)
    # d = wsgiserver.WSGIPathInfoDispatcher({'/': app})
    # host = '0.0.0.0'
    # port = CHERRYPY_PORT
    # server = wsgiserver.CherryPyWSGIServer((host, port), d, numthreads=30, timeout=21600, request_queue_size=200)
    #
    # try:
    #     print "Server started on http://%s:%d" % (host, port)
    #     server.start()
    # except KeyboardInterrupt:
    #     server.stop()


if __name__ == '__main__':
    manager.main()
