import django
from django.template import Template, Context
from django.conf import settings
settings.configure(TEMPLATES=[{'BACKEND': 'django.template.backends.django.DjangoTemplates'}])
django.setup()
t = Template('{{ backend_history|escapejs|default:"[]" }}')
print('OUTPUT:', t.render(Context({})))
