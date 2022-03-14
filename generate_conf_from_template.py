import yaml
from jinja2 import Template

# https://www.youtube.com/watch?v=PSgSjTeqRX0

data = yaml.load(open('protocol_data.yml'))
print data

#tmpl = Template(open('/var/tmp/pyez_demo/examples/protocol_temp.j2').read())
tmpl = Template(open('protocol_temp.j2').read())
conf = tmpl.render(data)
print conf