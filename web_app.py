from flask import Flask, Blueprint, render_template, redirect, url_for, request
from werkzeug.middleware.proxy_fix import ProxyFix
import sys
from argparse import ArgumentParser

from spotify_classifier import *

appweb = Blueprint('hello', __name__)

@appweb.route('/')
def home():
    return render_template("index.html")

@appweb.route('/send', methods=['POST'])
def send():
    danceability = request.form['danceability']
    energy= request.form['energy']
    loudness = request.form['loudness']
    key = request.form['key']
    acousticness = request.form['acousticness']
    instrumentalness = request.form['instrumentalness']
    valence = request.form['valence']
    
    predict_real =  best_model.predict([[danceability, energy, key , loudness,acousticness, instrumentalness, valence]])

    if(predict_real == [0]):
        predict = "The song is from an album and we are certain with an accuracy of " + str(round(model_accuracy,2)*100) +"%"
    elif(predict_real == [1]):
        predict = "The song is a single and we are certain with an accuracy of " + str(round(model_accuracy,2)*100)+"%"
    else:
        predict = "The song is from a compilation album and we are certain with an accuracy of " + str(round(model_accuracy,2)*100)+"%"

    return render_template('index.html', predict = predict)


@appweb.route('/about')
def about():
    return render_template("about.html")

if __name__ == '__main__':

    # arg parser for the standard anaconda-project options
    parser = ArgumentParser(prog="home",
                            description="Simple Flask Application")
    parser.add_argument('--anaconda-project-host', action='append', default=[],
                        help='Hostname to allow in requests')
    parser.add_argument('--anaconda-project-port', action='store', default=8086, type=int,
                        help='Port to listen on')
    parser.add_argument('--anaconda-project-iframe-hosts',
                        action='append',
                        help='Space-separated hosts which can embed us in an iframe per our Content-Security-Policy')
    parser.add_argument('--anaconda-project-no-browser', action='store_true',
                        default=False,
                        help='Disable opening in a browser')
    parser.add_argument('--anaconda-project-use-xheaders',
                        action='store_true',
                        default=False,
                        help='Trust X-headers from reverse proxy')
    parser.add_argument('--anaconda-project-url-prefix', action='store', default='',
                        help='Prefix in front of urls')
    parser.add_argument('--anaconda-project-address',
                        action='store',
                        #default='0.0.0.0',
                        help='IP address the application should listen on.')

    args = parser.parse_args()

    app = Flask(__name__)
    app.register_blueprint(appweb, url_prefix = args.anaconda_project_url_prefix)

    app.config['PREFERRED_URL_SCHEME'] = 'https'

    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.run(host=args.anaconda_project_address, port=args.anaconda_project_port)