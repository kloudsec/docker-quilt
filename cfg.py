import os


CWD = os.path.dirname(os.path.realpath(__file__))
RESOURCES_PATH = os.path.join(CWD, 'resources')
WORKSPACE_PATH = os.path.join(RESOURCES_PATH, 'workspace')
SQL_URI = 'sqlite:///state.db'
CHERRYPY_PORT = 80
DEBUG = False
SLACK_MSG_PREFIX = "[QUILT] "
