from datetime import datetime
from multiprocessing import context
from os import environ
from faker import Faker
from jinja2 import Environment, PackageLoader, select_autoescape
from jinja2.runtime import Context
import argparse
from google.cloud import storage

#[START template read]
def read_file(bucketname, blobname):
    print('Reading the full file contents:\n')
    client = storage.Client()

    bucket = client.get_bucket(bucketname)
    blob = bucket.get_blob(blobname)
    contents = blob.download_as_string()
    print(contents)
    return contents
#[END template read]

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--template', required=True, help='name of the template file')
    parser.add_argument('--output', help='pubsub, gcs')
    parser.add_argument('--rate', type=int, default=100, help='req/sec e.g. 100')
    args = parser.parse_args()

    env = Environment(
    loader=PackageLoader("main"),
    autoescape=select_autoescape()
    )
    template = env.get_template(args.template)

    fake = Faker()
    rs = template.render(fake=fake)
    print(rs)

if __name__ == '__main__':
    main()