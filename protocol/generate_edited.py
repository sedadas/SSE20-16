import argparse
import datetime
import hashlib
from jinja2 import Template

def generate_init_password(firstname, lastname, usage, secure_seed, current_date):
    print(current_date)
    result = hashlib.md5()
    result.update(f"{secure_seed}{firstname}{lastname}{usage}{current_date}".encode())
    return result.hexdigest()


def generate_email(data_dict):
    with open('welcome_email.j2') as f:
        template = Template(f.read())
    return template.render(data_dict)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--firstname", help="First name", required=True)
    parser.add_argument("-l", "--lastname", help="Last name", required=True)
    parser.add_argument("-d", "--domain", help="Domain", required=True)
    parser.add_argument("-s", "--secure-seed", help="Secure Seed", required=True)
    parser.add_argument("-c", "--current-date", help="Current Date", required=False)
    args = parser.parse_args()

    firstname = args.firstname
    lastname = args.lastname
    domain = args.domain
    secure_seed = args.secure_seed
    current_date = args.current_date

    if not current_date:
        now = datetime.datetime.now()
        current_date = f"{now.year}{now.month}{now.day}"

    init_password_mail = generate_init_password(firstname, lastname, "mail", secure_seed, current_date)
    init_password_intranet = generate_init_password(firstname, lastname, "intranet", secure_seed, current_date)

    data_dict = { "firstname": firstname, "lastname": lastname, "domain": domain, "init_password_mail": init_password_mail, "init_password_intranet": init_password_intranet }

    print(generate_email(data_dict))
