from django import template
import itertools

register = template.Library()

#@register.filter(name='tag_name')



#@register.filter(name='show_type')
def show_type(data):
    return str(type(data))

register.filter('show_type',show_type)
#register.tag('current_time', do_current_time)



@register.filter(name='chop_formset')
def chop_formset(form_set):
    form_list = []
    for form in formset:
        form_list.append(form)
    return form_list

@register.filter(name='dj_iter')
def dj_iter(gen):
    #gen = (i for i in range(100000000000000))
    try:
       return next(gen)
    except StopIteration:
       return 'Completed Iteration'


class CycleNode(template.Node):
    def __init__(self, cyclevars):
        self.cyclevars = template.Variable(cyclevars)

    def render(self, context):
        names = self.cyclevars.resolve(context)
        if self not in context.render_context:
            context.render_context[self] = itertools.cycle(names)
        cycle_iter = context.render_context[self]
        return next(cycle_iter)

@register.tag
def cycle_list(parser, token):
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires an argument" % token.contents.split()[0]
        )
    node = CycleNode(arg)
    return node
