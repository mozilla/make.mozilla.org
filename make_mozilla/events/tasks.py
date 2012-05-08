from celery.task import task
from make_mozilla.bsd import BSDRegisterConstituent
import commonware.log
import funfactory.log_settings # Magic voodoo required to make logging work.

log = commonware.log.getLogger('mk.tasks')

@task
def register_email_address_as_constituent(email_address, group):
    log.info('Running register_email_address_as_constituent')
    BSDRegisterConstituent.add_email_to_group(email_address, group)
