from django import template
register = template.Library()

def linkline():
    return (request.session['LINE'])
linkline = register.tag(linkline)
