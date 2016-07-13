#!/usr/bin/python3

import hashlib
import time
import os
import random
import string

from two1.commands.util import config
from two1.wallet import Wallet
from two1.bitrequests import BitTransferRequests
from two1.bitrequests import BitRequestsError
requests = BitTransferRequests(Wallet(), config.Config().username)

mb = 1024 * 1024


def upload(base_url, file):

    # Set the source and dest paths
    dest_url = base_url + '/upload'

    # Upload the file and time it
    with open(file, 'rb') as f:
        r = requests.post(dest_url, files={ 'file': (file, f)}, max_price=5)

    print("Result from upload: " + r.text)

def testClient(target):
    try:

        # Figure out the base paths
        dataDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'client-data')
        baseUrl = 'http://' + target + ':8021'

        # Generate a 1 MB file with random data in it with a random name
        filename = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(20))
        fullFilePath = os.path.join(dataDir, filename)
        with open(fullFilePath, 'wb') as fout:
            fout.write(os.urandom(mb))

        print("Created temp file: " + fullFilePath)

        upload(baseUrl, fullFilePath)


    except Exception as err:
        print('Client test failed')
        print("Failure: {0}".format(err))

if __name__ == '__main__':
    import click

    @click.command()
    @click.option("-t", "--target", default="0.0.0.0", help="Target host to run against.")
    def run(target):

        print("Running upload test against: " + target)
        testClient(target)

    run()
