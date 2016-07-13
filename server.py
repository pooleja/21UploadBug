#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import logging
import psutil
import subprocess
import os
import yaml
import ipaddress
import string
import random
import glob
import time

from flask import Flask
from flask import request
from flask import send_from_directory

from two1.commands.util import config
from two1.wallet.two1_wallet import Wallet
from two1.bitserv.flask import Payment
from two1.bitrequests import BitTransferRequests
from two1.bitrequests import BitRequestsError
requests = BitTransferRequests(Wallet(), config.Config().username)

from speedE16 import SpeedE16

app = Flask(__name__)

# Set the max upload size to 2 MB
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024

# setup wallet
wallet = Wallet()
payment = Payment(app, wallet)

# hide logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

dataDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'server-data')

@app.route('/upload', methods=['POST'])
@payment.required(5)
def upload():
    print("Upload requested.")


    # check if the post request has the file part
    if 'file' not in request.files:
        return 'File Upload arg not found', 400

    file = request.files['file']

    # if user does not select file, browser also submits an empty part without filename
    if file.filename == '':
        return 'No selected file', 400

    # Generate a random file name and save it
    filename = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(20))
    file.save(os.path.join(dataDir, filename))

    # Return the file name so the client knows what to request to test download
    return json.dumps({ 'success' : True, 'filename' : filename }, indent=4, sort_keys=True)




if __name__ == '__main__':
    import click

    @click.command()
    @click.option("-d", "--daemon", default=False, is_flag=True,
                  help="Run in daemon mode.")
    def run(daemon):
        if daemon:
            pid_file = './server.pid'
            if os.path.isfile(pid_file):
                pid = int(open(pid_file).read())
                os.remove(pid_file)
                try:
                    p = psutil.Process(pid)
                    p.terminate()
                except:
                    pass
            try:
                p = subprocess.Popen(['python3', 'server.py'])
                open(pid_file, 'w').write(str(p.pid))
            except subprocess.CalledProcessError:
                raise ValueError("error starting server.py daemon")
        else:
            print("Server running...")
            app.run(host='0.0.0.0', port=8021)

    run()
