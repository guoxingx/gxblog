
from . import main


@main.route('/')
def index():
    return 'I am index of main.'
