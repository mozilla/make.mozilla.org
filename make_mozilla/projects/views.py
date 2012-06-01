import jingo
import urllib
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
from make_mozilla.projects import models, forms
from make_mozilla import tools


class Index(object):
    def find(self, model, request, field='value'):
        value = request.GET.get(model._meta.verbose_name)
        if value:
            try:
                value = model.objects.get(**dict([[field, value]]))
            except model.DoesNotExist, e:
                value = False
        else:
            value = None
        return value

    def extract_page(self, request):
        return request.GET.get('page', 1)

    def extract_audience(self, request):
        return self.find(models.Audience, request)

    def extract_tool(self, request):
        return self.find(tools.models.Tool, request, 'slug')

    def extract_difficulty(self, request):
        return self.find(models.Difficulty, request)

    def extract_skill(self, request):
        return self.find(models.Skill, request)

    def results(self, audience=None, tool=None, difficulty=None, skill=None):
        query = {}

        if audience is not None:
            query['audience'] = audience
        if tool is not None:
            query['tool'] = tool
        if difficulty is not None:
            query['difficulty'] = difficulty
        if skill is not None:
            query['skills'] = skill

        return models.Project.objects.filter(**query)

    def paginated_results(self, page=1, audience=None, tool=None, difficulty=None, skill=None, results_per_page=8):

        results = self.results(audience, tool, difficulty, skill)
        paginator = Paginator(results, results_per_page)

        try:
            page = paginator.page(page)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)

        return page

    def __call__(self, request):
        page = self.extract_page(request)
        audience = self.extract_audience(request)
        tool = self.extract_tool(request)
        difficulty = self.extract_difficulty(request)
        skill = self.extract_skill(request)

        featured = models.Project.objects.filter(featured=True)
        pagination = self.paginated_results(page, audience, tool, difficulty, skill)

        invitation = models.Project(
            name='Submit your own project',
            url_hash='submit',
            image='/media/img/submit-your-own.png',)

        projects = list(pagination.object_list)
        projects.append(invitation)

        filter_form = forms.FilterForm({
            'audience': audience,
            'tool': tool,
            'difficulty': difficulty,
            'skill': skill,
        })

        query = {}
        if audience:
            query['audience'] = audience.value
        if tool:
            query['tool'] = tool.slug
        if difficulty:
            query['difficulty'] = difficulty.value
        if skill:
            query['skill'] = skill.value

        qs = urllib.urlencode(query) if query else ''

        return jingo.render(request, 'projects/index.html', {
            'featured': featured,
            'projects': projects,
            'pagination': pagination,
            'filter_form': filter_form,
            'query': qs
        })

index = Index()


def submit(request):
    return jingo.render(request, 'projects/submit.html');


def details(request, project_hash):
    project = get_object_or_404(models.Project, url_hash=project_hash)

    return jingo.render(request, 'projects/detail.html', {
        'project': project
    });
