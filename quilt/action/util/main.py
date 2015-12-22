import uuid

from cfg import SLACK_MSG_PREFIX
import os
import requests


def generate_uuid():
    return str(uuid.uuid1())


def run_cmd_lis(cmd_lis):
    full_cmd = " && ".join(cmd_lis)
    os.system(full_cmd)


def project_name_from_git_uri(uri):
    return uri.split("/")[-1].replace(".git", "")


def save_bitbucket_ssh_key(ssh_key):
    home = os.path.expanduser('~')
    ssh_path = os.path.join(home, '.ssh')
    if not os.path.exists(ssh_path):
        os.mkdir(ssh_path)
    id_rsa_path = os.path.join(home, '.ssh/id_rsa')
    with open(id_rsa_path, 'w') as f:
        f.write(ssh_key)
        f.close()
    run_cmd_lis(["chmod 600 %s" % (id_rsa_path)])


def post_to_slack(msg):
    from quilt.action import kv


    slack_webhook = kv.get(kv.Keys.SLACK_INCOMING_WEBHOOK, None)
    if slack_webhook is None:
        return

    requests.post(slack_webhook, json={
        'text': "%s%s" % (SLACK_MSG_PREFIX, msg),
    })
