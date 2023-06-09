from PIL import Image
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from .models import Post


def validate_picture(filename):
    try:
        image = Image.open(filename)
        # validate the image
        if image.size[0] > 0 and image.size[1] > 0:
            return True
    except:
        return False


def paginate_posts(request, posts, results):

    page = request.GET.get("page")
    paginator = Paginator(posts, results)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        posts = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        posts = paginator.page(page)

    leftIndex = int(page) - 2

    if leftIndex < 1:
        leftIndex = 1

    rightIndex = int(page) + 2

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    return custom_range, posts


def search(request):
    search_query = ""

    if request.GET.get("search_query"):
        search_query = request.GET.get("search_query")

    posts = Post.objects.filter(
        Q(title__icontains=search_query) |
        Q(content__icontains=search_query) |
        Q(user__name__icontains=search_query)
    )

    return posts, search_query



