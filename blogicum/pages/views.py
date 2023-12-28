from django.views.generic import TemplateView


class AboutView(TemplateView):
    """Page with information about the site."""

    template_name = 'pages/about.html'


class RulesView(TemplateView):
    """Page with site rules."""

    template_name = 'pages/rules.html'


def page_not_found(request, exception):
    return render(request, 'pages/404.html', status=404)

def csrf_failure(request, reason=''):
    return render(request, 'pages/403csrf.html', status=403)

def server_error(request):
    return render(request, 'pages/500.html', status=500)
