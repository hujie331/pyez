from jnpr.junos import Device
from jnpr.junos.utils.config import Config
import yaml
# from jinja2 import Template
from pprint import pprint

dev = Device(host='172.19.195.37', user='lab', password='Lab@123', gather_facts=False)
dev.open()

data = yaml.load(open('dot1x_vars_hh.yml'), Loader=yaml.SafeLoader)
#pprint(data)



# with Config(dev, mode='exclusive') as cu:   # exclusive mode is working !!!
with Config(dev) as cu:       # without exclusive, you will be able to see diff when run 'show | compare'
   cu.load(template_path='dot1x_jinja2_template.j2', template_vars=data, format='text')    # 'load' has built-in render method
#   cu.load(template_path='dot1x_jinja2_template_set.j2', template_vars=data, format='set')    # this line doesn't work
   cu.pdiff()
   cu.commit()
dev.close()
