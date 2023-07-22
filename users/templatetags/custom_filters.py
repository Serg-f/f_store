from django import template

register = template.Library()


@register.filter
def add_label_class(label_tag, css_class):
    index = label_tag.find('>')
    updated_label_tag = label_tag[:index] + f' class="{css_class}"' + label_tag[index:]
    return updated_label_tag
