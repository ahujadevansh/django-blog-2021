from django import template

register = template.Library()

# @register.filter
# def foo(self):
    
#     return self + ' active'

@register.filter
def active(value, arg):

    if(value == arg):
        return 'active'
    else:
        ''