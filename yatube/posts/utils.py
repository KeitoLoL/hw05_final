from django.conf import settings
from django.core.paginator import Paginator


def page_setup(request, posts):
    """Настраивает количество отображаемого контента на странице"""
    paginator = Paginator(posts, settings.DISPLAYS_NUMBER)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)
