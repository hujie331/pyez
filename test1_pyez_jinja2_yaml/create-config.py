from jnpr.junos import Device
from jnpr.junos.utils.config import Config
import
# from jinja2 import Template
from pprint import pprint

dev = Device(host='172.19.195.37', user='lab', password='Lab@123', gather_facts=False)
dev.open()

data = yaml.load(open('configuration.yml'), Loader=yaml.SafeLoader)
pprint(data)


#cu = Config(dev, mode='exclusive')
with Config(dev, mode='exclusive') as cu:
   cu.load(template_path='config-template.j2', template_vars=data, format='text')    # .load has built-in render method
   cu.pdiff()
   cu.commit()
dev.close()

# cu.load(template_path='config-template.j2', template_vars=data, format='text')
# cu.pdiff()
# cu.commit()
# if cu.commit_check():
#    cu.commit()
# else:
#    cu.rollback()

#dev.close()




# # First PyEz test with YAML and jinja2 template engine
# # YAML file should contain juniper devices to configre
#
# # >>> generat_conf_from_template.py:
# # import yaml
# # from jinja2 import Template
# #
# # # https://www.youtube.com/watch?v=PSgSjTeqRX0
# #
# # data = yaml.load(open('protocol_data.yml'))
# # print data
# #
# # #tmpl = Template(open('/var/tmp/pyez_demo/examples/protocol_temp.j2').read())
# # tmpl = Template(open('protocol_temp.j2').read())
# # conf = tmpl.render(data)
# # print conf
#
# # >>> load_temp_conf.py:
# from jnpr.junos import Device
# from jnpr.junos.utils.config import Config
# import yaml
# from pprint import pprint
#
# dev = Device(host='172.19.195.47', user='lab', password='Lab@123', gather_facts=False)
# dev.open()
#
# data = yaml.load(open('configuration.yml'), Loader=yaml.SafeLoader)
# pprint(data)
#
# #dev.bind(cfg=Config)
# cu = Config(dev)
#
# cu.load(template_path='/home/jhu/PycharmProjects/pyez/test1_pyez_jinja2_yaml/config-template.j2', template_vars=data, format='text')
# #dev.cfg.load(template_path='/home/jhu/PycharmProjects/pyez/test1_pyez_jinja2_yaml/config-template.j2', template_vars=data, format='text')
# cu.pdiff()
# if cu.commit_check():
#    cu.commit()
# else:
#    cu.rollback()
#
# dev.close()
#
# #
# # import yaml
# # from pprint import pprint
# # from jnpr.junos import Device
# # from jnpr.junos.utils.config import Config
# # #from jinja2 import Template
# #
# # # create datastructure from YAML file.
# # # yaml.load takes a stream so open file object from yaml file.
# # myvars = yaml.safe_load(open('configuration.yml'))
# #
# # # myvars has become a python dictionary thanx to YAML lib.
# # pprint(myvars)
# #
# # # now create juniper device object from Device class and open this device.
# # for juniper in myvars['juniper_devices']:
# #     print("Configuring % s" % juniper)
# #
# # # from here, the program crushing...
# # device = Device(host=juniper, user='lab', password='Lab@123', gather_facts=False)
# # output = device.open()
# # #data = yaml.safe_load(open('configuration.yml'))
# # #pprint(data)
# # cu = Config(device)
# # # now bind Config class to this device which makes it a property of the :class:Device instance
# # #device.bind(cfg=Config)
# #
# #
# #
# #
# # # load can take our jinja2 template with our myvars from YAML file
# # # The following parameters are needed for the load command:
# # # 1: template_path (str): path to jinja2 template file
# # # 2: template_vars (dict): dictionary build from YAML file, same vars are in jinja2 template
# # # 3: set format to text, otherwise you will see errors
# # #device.cfg.load(template_path='config-template.j2', template_vars=myvars, format='text')
# #
# # #cu.load(template_path='config-template.j2', template_vars=myvars, format='text', ignore_warning=True)
# # cu.load(template_path='config-template.j2', template_vars=myvars, format='text')
# #
# # # print configuration differences
# # cu.pdiff()
# #
# # # now check configuration and if it’s all OK, just commit.
# # if cu.commit_check():
# #     cu.commit()
# # else:
# #     print("something wrong")
# #     cu.rollback()
# #
# # # no close connection to juniper device
# # device.close()
# #
# # print("configuration of devices done")