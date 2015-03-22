from flask import Blueprint, render_template

spa = Blueprint("spa", __name__)

@spa.route('/', methods=['GET'])
def index():
    return render_template('index.html')
