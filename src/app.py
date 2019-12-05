from flask import Flask

from src.views.start import start
from src.views.admin import admin

app = Flask(__name__)

app.register_blueprint(start)
app.register_blueprint(admin, url_prefix="/admin")

if __name__ == "__main__":
	app.run(port=8080, host="0.0.0.0", debug=False)
