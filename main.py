from datetime import datetime
from multiprocessing import context
from os import environ
from faker import Faker
from jinja2 import Environment, PackageLoader, select_autoescape
from jinja2.runtime import Context

def main():

    # env = jinja2.Environment()
    env = Environment(
    loader=PackageLoader("main"),
    autoescape=select_autoescape()
    )
    # template = env.from_string("Hello {{ name }}")
    template = env.get_template("mytemplate.html")

    # ctx = Context(environment=env, parent=None, name="main", blocks={})
    fake = Faker()
    # print(fake.name())
    # print(fake.random.randint(10,50))
    rs = template.render(fake=fake)
    print(rs)

if __name__ == '__main__':
    main()