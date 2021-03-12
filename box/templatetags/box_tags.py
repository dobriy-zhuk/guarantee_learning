from django import template

register = template.Library()


@register.filter(name='times')
def times(from_number, to_number):
    return range(from_number,to_number)


@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()
