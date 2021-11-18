'''
    You have created a simple template tag that returns the number of posts published
so far. Each module that contains template tags needs to define a variable called
register to be a valid tag library. This variable is an instance of template.Library,
and it's used to register your own template tags and filters.
    In the code above, you define a tag called total_posts with a Python function and
use the @register.simple_tag decorator to register the function as a simple tag.
Django will use the function's name as the tag name. If you want to register it using
a different name, you can do so by specifying a name attribute, such as @register.
simple_tag(name='my_tag').
    After adding a new template tags module, you will need to restart
the Django development server in order to use the new tags and
filters in templates.
    Before using custom template tags, you have to make them available for the template
using the {% load %} tag. As mentioned before, you need to use the name of the
Python module containing your template tags and filters.
'''

from django.utils.safestring import mark_safe
from django.db.models import Count
from django import template
from ..models import Post
import markdown

register = template.Library()


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))


@register.simple_tag
def total_posts():
    return Post.published.count()


@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(
        total_comments=Count('comments')
    ).order_by('-total_comments')[:count]


@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}
