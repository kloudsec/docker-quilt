import subprocess

from cfg import WORKSPACE_PATH
import os


def login(username, email, passwd):
    return os.system('docker login -e %s -p %s -u %s' % (email, passwd, username)) == 0


def build(uri, repo_image, main_tag, other_tags=None, use_cache=True):
    from quilt.action import util


    if other_tags == None:
        other_tags = []

    cd_cmd = "cd %s" % (os.path.join(WORKSPACE_PATH, util.project_name_from_git_uri(uri)))
    util.run_cmd_lis([cd_cmd])
    repo_image_tag = '%s:%s' % (repo_image, main_tag)
    if use_cache:
        build_success = os.system("docker build -t %s ." % (repo_image_tag)) == 0
    else:
        build_success = os.system("docker build --no-cache -t %s ." % (repo_image_tag)) == 0
    if build_success:
        image_id = subprocess.check_output("docker images -q %s" % (repo_image_tag), shell=True)
        util.run_cmd_lis(["docker tag %s %s:%s" % (image_id, repo_image, t) for t in other_tags])
    return build_success


def push(repo_image, tag):
    return os.system("docker push %s:%s" % (repo_image, tag)) == 0
