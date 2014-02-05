from django.db import models


class ProjectsManager(models.Manager):

    # only return projects that are set to be visible
    def public_projects(self):
        return self.filter(public=True)
