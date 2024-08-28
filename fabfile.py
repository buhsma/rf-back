from fabric import task
from invoke import run


@task
def deploy(c):
    c.run("cd /var/relayfox/rf-back && git pull origin main")
    c.run("source /var/relayfox/rf-back/venv/bin/activate && pip install -r /var/relayfox/rf-back/requirements.txt")
    c.run("cd /var/relayfox/rf-back && /var/relayfox/rf-back/venv/bin/python manage.py migrate")
    c.run("sudo systemctl reload gunicorn")
    print("Deployment completed and Gunicorn reloaded successfully.")


@task
def reload_gunicorn(c):
    c.run("sudo systemctl restart gunicorn")
    print("Gunicorn reloaded successfully.")


@task
def manage_crontabs(c):
    c.run("crontab -r", warn=True)
    c.run("/var/relayfox/rf-back/venv/bin/python /var/relayfox/rf-back/manage.py crontab add")
    
    new_cron = """
# m h dom mon dow command
0 3 * * * /var/relayfox/rf-back/venv/bin/python /var/relayfox/rf-back/manage.py clearsessions
"""
    c.run(f'echo "{new_cron}" | crontab -')
    print("Crontabs updated successfully.")
