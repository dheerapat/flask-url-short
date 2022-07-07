from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__)
    app.secret_key = 'secretyouonlyknow' # because we have to sent message in the app
    
    from . import urlshort
    app.register_blueprint(urlshort.bp)
    
    return app