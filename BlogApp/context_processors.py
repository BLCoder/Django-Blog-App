from .models import article

def posts(request):
    return {
        'all_posts': article.objects.order_by('posted_on'),
    }