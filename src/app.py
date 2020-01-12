from flask import Flask

from src.views.start import start_blueprint
from src.views.admin import admin_blueprint
from src.views.api import api_blueprint

app = Flask(__name__)

app.register_blueprint(start_blueprint)
app.register_blueprint(admin_blueprint, url_prefix="/admin")
app.register_blueprint(api_blueprint, url_prefix="/api")

if __name__ == "__main__":
    app.run(debug=True)