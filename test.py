from django.template import Template, Context
t = Template('{{ backend_history|escapejs|default:"[]" }}')
print("OUTPUT:", t.render(Context({})))
