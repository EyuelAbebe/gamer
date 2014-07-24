from fabric.api import sudo, execute, run, env, local
import boto.ec2
from fabric.contrib.project import rsync_project
from fabric.contrib.files import upload_template
import time

env.hosts = ['localhost', ]
env.aws_region = 'us-west-2'
env.key_filename = '/home/caderache2014/.ssh/BilinghamKepPair1.pem'
sync_exclude_list = [
    '.git',
    '*.pyc',
    'fabfile.py',
    'supervisord.conf',
    'credentials.txt',
    '.travis.yml',
    '/imagr_images/test_data',
    '/media/',
    'nginx_config'
]


def host_type():
    run('uname -s')


def run_command_to_selected_server(command, *args, **kwargs):
    select_instance()
    selected_hosts = [
        'ubuntu@' + env.active_instance.public_dns_name
    ]
    execute(command, *args,  hosts=selected_hosts, **kwargs)


def get_ec2_connection():
    if 'ec2' not in env:
        conn = boto.ec2.connect_to_region(env.aws_region)
        if conn is not None:
            env.ec2 = conn
            print "Connected to EC2 region %s" % env.aws_region
        else:
            msg = "Unable to connect to EC2 region %s"
            raise IOError(msg % env.aws_region)
    return env.ec2


def provision_instance(wait_for_running=False, timeout=60, interval=2):
    wait_val = int(interval)
    timeout_val = int(timeout)
    conn = get_ec2_connection()
    instance_type = 't1.micro'
    key_name = 'BilinghamKepPair1'
    security_group = 'ssh-access'
    image_id = 'ami-4bbcc47b'

    reservations = conn.run_instances(
        image_id,
        key_name=key_name,
        instance_type=instance_type,
        security_groups=[security_group, ]
    )
    new_instances = [
        i for i in reservations.instances if i.state == u'pending']
    running_instance = []
    if wait_for_running:
        waited = 0
        while new_instances and (waited < timeout_val):
            time.sleep(wait_val)
            waited += int(wait_val)
            for instance in new_instances:
                state = instance.state
                print "Instance %s is %s" % (instance.id, state)
                if state == "running":
                    running_instance.append(
                        new_instances.pop(new_instances.index(i))
                    )
                instance.update()


def list_aws_instances(verbose=False, state='all'):
    conn = get_ec2_connection()

    reservations = conn.get_all_reservations()
    instances = []
    for res in reservations:
        for instance in res.instances:
            if state == 'all' or instance.state == state:
                instance = {
                    'id': instance.id,
                    'type': instance.instance_type,
                    'image': instance.image_id,
                    'state': instance.state,
                    'instance': instance,
                }
                instances.append(instance)
    env.instances = instances
    if verbose:
        import pprint
        pprint.pprint(env.instances)
# add an import
from fabric.api import prompt


def select_instance(state='running'):
    if env.get('active_instance', False):
        return

    list_aws_instances(state=state)

    prompt_text = "Please select from the following instances:\n"
    instance_template = " %(ct)d: %(state)s instance %(id)s\n"
    for idx, instance in enumerate(env.instances):
        ct = idx + 1
        args = {'ct': ct}
        args.update(instance)
        prompt_text += instance_template % args
    prompt_text += "Choose an instance: "

    def validation(input):
        choice = int(input)
        if choice not in range(1, len(env.instances) + 1):
            raise ValueError("%d is not a valid instance" % choice)
        return choice

    choice = prompt(prompt_text, validate=validation)
    env.active_instance = env.instances[choice - 1]['instance']


def stop_instance():
    select_instance(state='running')
    env.ec2.stop_instances(env.active_instance.id)


def terminate_instance():
    select_instance(state="stopped")
    env.ec2.terminate_instances(env.active_instance.id)


def deploy():
    select_instance()
    user_wants_installs = ask_user_to_run_installs()
    run_rsync()
    if user_wants_installs:
        update_ubuntu()
        do_apt_and_pip_installs()
        install_nginx()
    else:
        print "\nYOU ARE SKIPPING SOFTWARE UPDATES AND INSTALLS"
    mk_static_and_media_dirs()
    give_ubuntu_user_static_media_own()
    run_collect_static()
    move_nginx_config()
    restart_nginx()
    move_supervisor_config()
    restart_supervisor()


def _run_collect_static():
    sec_key = 'export SECRET_KEY=foo; '
    django_config = 'export DJANGO_CONFIGURATION=Prod; '
    collect_static = 'python manage.py collectstatic'
    sudo(sec_key + django_config + collect_static)


def run_collect_static():
    run_command_to_selected_server(_run_collect_static)


def ask_user_to_run_installs():
    response = raw_input("\nWould you like to update and install? (y/n): ")
    if response == 'y':
        return True
    else:
        return False


def restart_nginx():
    run_command_to_selected_server(_restart_nginx)


def _restart_nginx():
    sudo('/etc/init.d/nginx restart')


def move_nginx_config():
    run_command_to_selected_server(_move_nginx_config)


def _move_nginx_config():
    upload_template(
        'nginx_config', '~/',
        context={'host_dns': env.active_instance.public_dns_name})
    sudo('mv nginx_config /etc/nginx/sites-available/default')


def move_supervisor_config():
    run_command_to_selected_server(_move_supervisor_config)


def _move_supervisor_config():
    upload_template(
        'supervisord.conf',
        '~/', context={'host_envs': read_envs()})
    # move the supervisor conf file into place
    sudo('mv supervisord.conf /etc/supervisor/conf.d/imagr_app.conf')


def do_apt_and_pip_installs():
    run_command_to_selected_server(_do_apt_and_pip_installs)


def _do_apt_and_pip_installs():
    sudo('apt-get install -y python-pip')
    sudo('apt-get install -y libpq-dev')
    sudo('apt-get install -y libjpeg-dev')
    sudo('apt-get install -y zlib1g-dev')
    sudo('apt-get install -y python-dev')
    sudo('apt-get install -y supervisor')
    sudo("pip install -r requirements.txt")


def run_rsync():
    run_command_to_selected_server(_run_rsync)


def _run_rsync():
    # sync_exclude_list now at top of file
    rsync_project(exclude=sync_exclude_list, local_dir="./", remote_dir="~/")


def update_ubuntu():
    run_command_to_selected_server(_update_ubuntu)


def _update_ubuntu():
    sudo('apt-get update -y')


def restart_supervisor():
    run_command_to_selected_server(_restart_supervisor)


def _restart_supervisor():
    sudo("/etc/init.d/supervisor stop")
    sudo("/etc/init.d/supervisor start")


def _install_nginx():
    sudo('apt-get install nginx')
    sudo('/etc/init.d/nginx start')


def install_nginx():
    run_command_to_selected_server(_install_nginx)


def read_envs():
    with open('credentials.txt') as f:
        lines = map(str.strip, f.readlines())
        values = ','.join(lines)
        values += ",CURRENT_HOST='{}'".format(
            env.active_instance.public_dns_name)
        print values
        return values


def mk_static_and_media_dirs():
    run_command_to_selected_server(_mk_static_and_media_dir)


def _mk_static_and_media_dir():
    sudo('mkdir -p /var/www/static')
    sudo('mkdir -p /var/www/media')


def give_ubuntu_user_static_media_own():
    run_command_to_selected_server(_give_ubuntu_user_static_media_own)


def _give_ubuntu_user_static_media_own():
    sudo('chown -R ubuntu:ubuntu /var/www')


def run_ssh():
    select_instance()
    local('ssh -i ~/.ssh/pk-aws.pem ubuntu@{}'.format(
        env.active_instance.public_dns_name))
