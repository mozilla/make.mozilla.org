from django.conf import settings


def app_stage(request):
    """
    As we're using an external service to resize images we need to pipe through
    the FULL domain - https:// and everything
    """
    stage = getattr(settings, 'APP_STAGE', False)
    message = getattr(settings, 'APP_MESSAGE', False)

    return {
        'APP_STAGE': stage,
        'APP_MSG': message
    }
