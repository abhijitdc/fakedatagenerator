from datetime import datetime
from multiprocessing import context
from os import environ
from time import time
from faker import Faker
from jinja2 import Environment, PackageLoader, select_autoescape
from jinja2.runtime import Context
import argparse
from google.cloud import storage
from ratelimit import limits, sleep_and_retry
import datetime


#[START template read]
def read_file(bucketname, blobname):
    print('Reading the full file contents:\n')
    client = storage.Client()

    bucket = client.get_bucket(bucketname)
    blob = bucket.get_blob(blobname)
    contents = blob.download_as_string()
    # print(contents)
    return contents
#[END template read]

RATE =  environ.get("RATE", 10)
PERIOD = environ.get("PERIOD", 1)

@sleep_and_retry
@limits(calls=int(RATE), period=int(PERIOD))
def writedata(data, id):
    print(f'{data} {datetime.datetime.now().time()} id:{id}')

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--template', required=True, help='name of the template file')
    parser.add_argument('--output', help='pubsub, gcs')
    args = parser.parse_args()

    env = Environment(
    loader=PackageLoader("main"),
    autoescape=select_autoescape()
    )

    template = env.get_template(args.template)
    fake = Faker()
    template.globals['now'] = datetime.datetime.utcnow
    
    counter = 0
    while(True):
         rs = template.render(fake=fake)
        #  print(rs)
         counter += 1
         writedata(rs, counter)

if __name__ == '__main__':
    main()