# -*- coding: utf-8 -*-
"""Create application instance."""
from flask.helpers import get_debug_flag
from flask import render_template
from OnlineCV.app import create_app
from OnlineCV.settings import DevConfig, ProdConfig

CONFIG = DevConfig if get_debug_flag() else ProdConfig

app = create_app(CONFIG)

@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, threaded=True, debug=True)
