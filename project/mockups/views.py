from mockups import app
from mockups import utils
from flask import render_template

@app.route('/mockup/<mock_id>')
def multi_use_view(mock_id):
    template = utils.get_template(mock_id)
    data = utils.get_data(mock_id)
    js, css = utils.get_static_files(mock_id)
    data['css'] = css
    data['js'] = js
    data['mock_id'] = mock_id
    return render_template(template, data=data)