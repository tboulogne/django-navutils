from django import template

register = template.Library()


@register.simple_tag
def render_node(node, user, max_depth=999, current_depth=None, start_depth=None):

    start_depth = start_depth or node.depth
    current_depth = current_depth or node.depth - start_depth

    viewable_children = []
    if current_depth + 1 <= max_depth:
        for child in node.children:
            if child.is_viewable_by(user):
                viewable_children.append(child)

    t = template.loader.get_template(node.template)

    return t.render(template.Context({
        'node': node,
        'viewable_children': viewable_children,
        'user': user,
        'max_depth': max_depth,
        'current_depth': current_depth,
        'start_depth': start_depth,
    }))