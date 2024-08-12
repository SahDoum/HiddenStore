from jinja2 import Environment, FileSystemLoader

template_loader = FileSystemLoader("templates")
template_env = Environment(loader=template_loader)


def render_template(template_name: str, *args, **kwargs):
    template = template_env.get_template(template_name)
    return template.render(*args, **kwargs)
