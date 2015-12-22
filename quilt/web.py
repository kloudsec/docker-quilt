from functools import wraps

from cfg import DEBUG
from flask import render_template, redirect, request, Response
from quilt.app import app, save, delete
from quilt.action import kv, docker, util, builds, git
from quilt.model import BuildFlow


def _check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    admin_username = kv.get(kv.Keys.ADMIN_USERNAME, None)
    admin_password = kv.get(kv.Keys.ADMIN_PASSWD, None)
    if admin_password is None or admin_username is None:
        return True

    return password == admin_password and username == admin_username


def _authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})


def _requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not _check_auth(auth.username, auth.password):
            return _authenticate()
        return f(*args, **kwargs)

    return decorated


def index():
    username = kv.get(kv.Keys.ADMIN_USERNAME, None)
    if username is not None and not DEBUG:
        return redirect("/manage")

    return render_template("setup.html")


@_requires_auth
def manage():
    admin_username = kv.get(kv.Keys.ADMIN_USERNAME, None)
    if admin_username is None:
        return redirect("/")

    build_flow_lis = builds.all()
    return render_template("manage.html", **{
        'build_flows': build_flow_lis,
        'base_url': request.url_root,
    })


def init():
    username = request.form.get('username')
    passwd = request.form.get('passwd')
    bitbucket_ssh_key = request.form.get('bitbucket_ssh_key')
    slack_incoming_webhook = request.form.get('slack_incoming_webbook')

    docker_hub_email = request.form.get('docker_hub_email')
    docker_hub_username = request.form.get('docker_hub_username')
    docker_hub_passwd = request.form.get('docker_hub_passwd')

    if not docker.login(docker_hub_username, docker_hub_email, docker_hub_passwd):
        return render_template("error.html", **{
            "error_msg": "Unable to login to Docker Hub, incorrect credentials maybe?"
        })

    kv.set(kv.Keys.ADMIN_USERNAME, username)
    kv.set(kv.Keys.ADMIN_PASSWD, passwd)
    if slack_incoming_webhook is not None:
        kv.set(kv.Keys.SLACK_INCOMING_WEBHOOK, slack_incoming_webhook)
        util.post_to_slack("Welcome to Quilt")
    if not DEBUG and bitbucket_ssh_key is not None: util.save_bitbucket_ssh_key(bitbucket_ssh_key)
    return redirect("/manage")


def error():
    return render_template("error.html")


@_requires_auth
def new_build():
    repository_uri = request.form.get('repository_uri')
    repo_image = request.form.get('repo_image')

    if builds.get_by_repo_image(repo_image):
        return render_template("error.html", **{
            "error_msg": "Another build already pushes to the same %s repository" % (repo_image),
        })

    clone_success = git.clone(repository_uri)
    if not clone_success:
        return render_template("error.html", **{
            "error_msg": "Unable to clone from %s" % (repository_uri),
        })

    build_flow = BuildFlow()
    build_flow.uri = repository_uri
    build_flow.docker_repo_image = repo_image
    save(build_flow)
    return redirect('/manage')


@_requires_auth
def del_build(id):
    build_flow = builds.get(id)
    if build_flow is not None:
        delete(build_flow)
    return redirect('/manage')


def webhook(build_flow_id):
    build_flow = builds.get(build_flow_id)
    if build_flow is not None:
        return

    json_dic = request.get_json()
    branch = None
    commit_msg = None
    if "bitbucket.org/" in build_flow.uri:
        if 'push' in json_dic and \
                        'changes' in json_dic['push'] and \
                        'new' in json_dic['push']['changes'] and \
                        'type' in json_dic['push']['changes']['new'] and \
                        json_dic['push']['changes']['new']['type'] == 'branch':
            branch = json_dic['push']['changes']['new']['name']
            commit_msg = json_dic['push']['changes']['new']['target']['message']

    elif "github.com/" in build_flow.uri:
        if 'ref' in json_dic and \
                        'head_commit' in json_dic:
            branch = json_dic['ref'].split("/")[-1]
            commit_msg = json_dic['head_commit']['message']

    if None in [branch, commit_msg]:
        return

    util.post_to_slack('New push from %s/%s (%s)' % (util.project_name_from_git_uri(build_flow.uri), branch, commit_msg))
    misc_tags = []
    if branch == 'master':
        misc_tags += ['latest']
    if branch == 'develop':
        misc_tags += ['staging']
    git.pull(build_flow.uri, branch)
    util.post_to_slack('Building Dockerfile of %s..' % (util.project_name_from_git_uri(build_flow.uri)))
    docker.build(build_flow.uri, build_flow.docker_repo_image, branch, misc_tags)
    util.post_to_slack('Finished Dockerfile of %s!' % (util.project_name_from_git_uri(build_flow.uri)))
    all_tags = misc_tags + [branch]
    util.post_to_slack('Pushing Docker image to %s..' % (build_flow.docker_repo_image))
    for t in all_tags:
        docker.push(build_flow.uri, t)
    util.post_to_slack('Docker image pushedto %s! All done.' % (build_flow.docker_repo_image))


@_requires_auth
def update_ssh_key():
    ssh_key = request.form.get('ssh_key')
    slack_incoming_webhook = request.form.get('slack_incoming_webbook')
    if ssh_key is not None and not DEBUG:
        util.save_bitbucket_ssh_key(ssh_key)

    if slack_incoming_webhook is not None:
        kv.set(kv.Keys.SLACK_INCOMING_WEBHOOK, slack_incoming_webhook)
        util.post_to_slack("Successfully setuped Slack notifications!")
    return redirect("/manage")


app.add_url_rule('/hook/<build_flow_id>',
                 "webhook", webhook, methods=['GET'])

app.add_url_rule('/manage',
                 "manage", manage, methods=['GET'])

app.add_url_rule('/setup',
                 "init", init, methods=['POST'])

app.add_url_rule('/build/del/<id>',
                 "del_build", del_build, methods=['GET'])

app.add_url_rule('/build',
                 "new_build", new_build, methods=['POST'])

app.add_url_rule('/ssh_key',
                 "update_ssh_key", update_ssh_key, methods=['POST'])

app.add_url_rule('/error',
                 "error", error, methods=['GET'])

app.add_url_rule('/',
                 "index", index, methods=['GET'])
