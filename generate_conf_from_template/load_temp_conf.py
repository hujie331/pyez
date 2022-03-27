from jnpr.junos import Device
from jnpr.junos.utils.config import Config
import yaml
from pprint import pprint

dev = Device(host='172.19.195.47', user='lab', password='Lab@123', gather_facts=False)
dev.open()

data = yaml.load(open('protocol_data.yml'), Loader=yaml.SafeLoader)
pprint(data)
cu = Config(dev)

cu.load(template_path='protocol_temp.j2', template_vars=data, format='text')
if cu.pdiff():
   cu.commit()

if cu.commit_check():
   cu.commit()
else:
   cu.rollback()

dev.close()