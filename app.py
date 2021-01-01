from flask import Flask, request
from flask_classy import FlaskView, route
from EmailVerificationView import EmailVerificationView

app = Flask(__name__)


EmailVerificationView.register(app, route_base='/')

if __name__ == '__main__':
    app.run()
