from ConfigParser import ConfigParser
import os


def get_template(id):
    return '{0}.html'.format(id)

def get_data(id):
    file_name = '{0}.ini'.format(id)
    path = os.path.join(os.path.dirname(__file__), 'data/')
    config = ConfigParser()
    config.read(os.path.join(path, file_name))
    return config._sections
    
def get_static_files(id):
    pass

def get_default_content():
    pass