import os

def add(dirconfig, template_directory):
    template_list = [d for d in os.listdir(template_directory) if os.path.isdir(os.path.join(template_directory, d))]
    for template_name in template_list:
        template_module = __import__(f"{template_directory}.{template_name}.main", fromlist=["static"])
        for static in getattr(template_module, "static", []):
            dirconfig.append(static)
