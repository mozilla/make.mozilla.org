from celery.decorators import task
from make_mozilla.bsd import BSDClient

@task
def register_email_address_as_constituent(email_address):
    BSDClient.register_email_address_as_constituent(email_address)
