# From https://djangosnippets.org/snippets/1441/

from django import template
from core.models import Prompt

register = template.Library()


@register.filter
def prompts(date):
    prompts = Prompt.objects.filter(day=date)
    if len(prompts) == 0:
        return "Freeform responses"
    return " / ".join([prompt.text for prompt in prompts])
