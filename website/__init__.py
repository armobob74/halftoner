from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'yzUZg1aELL1DGYoU9yHEFRZy' #some random string here

    #app.jinja_env.globals.update(some_global = some_global) #can be used for variables or functions



    from .views import views
    app.register_blueprint(views, url_prefix='/')

    return app
