from fabric import task, Connection, Config
# from invoke import Collection

conn = Connection(
    host='209.38.232.16',
    user='root',
    connect_kwargs={
        'key_filename': '/home/petra/.ssh/id_rsa'
    }
)

@task
def reload_gunicorn(c):
    conn.run('sudo systemctl restart gunicorn', pty=True)
    print("Gunicorn reloaded successfully.")

@task
def deploy(c):
    conn.run("cd /var/relayfox/rf-back && git pull origin main")
    conn.run("source /var/relayfox/rf-back/venv/bin/activate && pip install -r /var/relayfox/rf-back/requirements.txt")
    conn.run("cd /var/relayfox/rf-back && /var/relayfox/rf-back/venv/bin/python manage.py migrate")
    conn.run("sudo systemctl restart gunicorn")
    print("Deployment completed and Gunicorn reloaded successfully.")

@task
def manage_crontabs(c):
    conn.run("crontab -r", warn=True)
    conn.run("/var/relayfox/rf-back/venv/bin/python /var/relayfox/rf-back/manage.py crontab add")
    
    new_cron = """
# m h dom mon dow command
0 3 * * * /var/relayfox/rf-back/venv/bin/python /var/relayfox/rf-back/manage.py clearsessions
"""
    conn.run(f'echo "{new_cron}" | crontab -')
    print("Crontabs updated successfully.")

# ns = Collection()
# ns.add_task(reload_gunicorn)
# ns.add_task(deploy)
# ns.add_task(manage_crontabs)

# config = Config(default_collection=ns)