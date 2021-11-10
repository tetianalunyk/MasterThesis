from flask import Flask, current_app as app
from flask_assets import Environment, Bundle


def compile_static_assets(assets):
    app = Flask(__name__)
    assets = Environment(app)
    assets.auto_build = True
    assets.debug = False
    common_less_bundle = Bundle('src/less/*.less',
                                filters='less,cssmin',
                                output='sidebar.css',
                                extra={'rel': 'stylesheet/less'})
    home_less_bundle = Bundle('home_bp/less/home.less',
                              filters='less,cssmin',
                              output='home.css',
                              extra={'rel': 'stylesheet/less'})

    assets.register('common_less_bundle', common_less_bundle)
    assets.register('home_less_bundle', home_less_bundle)
    if app.config['ENV'] == 'development':  # Only rebuild bundles in development
        common_less_bundle.build()
        home_less_bundle.build()
    return assets

