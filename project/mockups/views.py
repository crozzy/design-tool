from mockups import app
from mockups import utils
from flask import render_template

@app.route('/mockup/<mock_id>')
def multi_use_view(mock_id):
    template = utils.get_template(mock_id)
    data = utils.get_data(mock_id)
    print data
    return render_template(template, data=data)