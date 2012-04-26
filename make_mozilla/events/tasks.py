from celery.decorators import task
from make_mozilla.bsd import BSDRegisterConstituent

@task
def register_email_address_as_constituent(email_address, group):
    BSDRegisterConstituent.add_email_to_group(email_address, group)
