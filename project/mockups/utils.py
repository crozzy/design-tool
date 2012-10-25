from ConfigParser import ConfigParser
import os
import glob
import collections

def get_template(id):
    return '{0}.html'.format(id)

def get_data(id):
    default_file_name = 'base.ini'
    file_name = '{0}.ini'.format(id)
    path = os.path.join(os.path.dirname(__file__), 'data/')
    config = ConfigParser()
    config.read(os.path.join(path, default_file_name))
    config.read(os.path.join(path, file_name))
    return config._sections

def get_static_files(id):
    data = get_data(id)
    static_path = os.path.join(os.path.dirname(__file__), 'static/')
    css_file_format = '*.css'
    js_file_format = '*.js'
    css = []
    js = []
    for (p, d, f) in os.walk(os.path.join(static_path, 'css')):
        for fs in f:
            css.append(os.path.join(p, fs).split('/static/')[1])
    for (p, d, f) in os.walk(os.path.join(static_path, 'js')):
        for fs in f:
            js.append(os.path.join(p, fs).split('/static/')[1])
    css = order_css(css)
    return js, css

def order_css(css_list):
    # Get the score of css
    tb_scored = [f for f in css_list if 'any' in f]
    ntb_scored = [f for f in css_list if 'any' not in f]
    score = [os.path.splitext(os.path.basename(css))[0].split('-').count('any')
        for css in tb_scored]
    css_score = dict(zip(score, tb_scored))    
    score.sort(reverse=True)
    sorted_css = []
    for s in score:
        sorted_css.append(css_score[s])
    css = ntb_scored + sorted_css
    return css