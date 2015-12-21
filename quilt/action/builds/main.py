from quilt.app import session
from quilt.model import BuildFlow


def all():
    return session.query(BuildFlow).all()


def get_by_repo_image(repo_image):
    return session.query(BuildFlow).filter(BuildFlow.docker_repo_image == repo_image).first() if repo_image is not None else None


def get(id):
    return session.query(BuildFlow).filter(BuildFlow.id == id).first() if id is not None else None
