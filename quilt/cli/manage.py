import shutil

from cfg import CWD, RESOURCES_PATH, WORKSPACE_PATH
import os
from manager import Manager
from quilt.app import Base, db
from quilt.action import util, git
from quilt.web import app, webhook


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
def clone(uri):
    return git.clone(uri)


@manager.command
def build(build_flow_id):
    webhook(build_flow_id)


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
