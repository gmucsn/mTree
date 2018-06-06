from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
import jinja2

admin_area = Blueprint('admin_area', __name__, template_folder='templates')

admin_area.jinja_loader = jinja2.ChoiceLoader([
    admin_area.jinja_loader,
    jinja2.PackageLoader('mTree', 'base/admin_templates'),
    jinja2.PackageLoader(__name__) # in the same folder will search the 'templates' folder
])

@admin_area.route('/', defaults={'page': 'index'})
@admin_area.route('/<page>')
def show(page):
    #try:
        print("TRYING TO DO SOMETHING")
        print(page)
        print(admin_area.jinja_loader)
        return render_template('admin_base.html')
    #except TemplateNotFound:
    #    abort(404)