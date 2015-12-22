from quilt.app import session, save
from quilt.model import KeyValue


class Keys:
    ADMIN_USERNAME = "admin_username"
    ADMIN_PASSWD = "admin_passwd"
    BITBUCKET_SSH_KEY = "bitbucket_ssh_key"
    DOCKER_USERNAME = "docker_username"
    DOCKER_PASSWD = "docker_passwd"
    DOCKER_EMAIL = "docker_email"
    SLACK_INCOMING_WEBHOOK = "slack_incoming_webhook"


def get(key, default_value):
    q = session.query(KeyValue).filter(KeyValue.key == key).first()
    if q is None:
        return default_value
    return q.val


def set(key, val):
    q = session.query(KeyValue).filter(KeyValue.key).first()
    if q is None:
        obj = KeyValue()
        obj.key = key
        obj.val = val
        return save(obj)

    q.val = val
    save(q)
    return q
