import uuid

import os


def generate_uuid():
    return str(uuid.uuid1())


def run_cmd_lis(cmd_lis):
    full_cmd = " && ".join(cmd_lis)
    os.system(full_cmd)


def project_name_from_git_uri(uri):
    return uri.split("/")[-1].replace(".git", "")


def save_bitbucket_ssh_key(ssh_key):
    home = os.path.expanduser('~')
    with open(os.path.join(home, '.ssh/id_rsa', 'w')) as f:
        f.write(ssh_key)
        f.close()
