#! /usr/bin/env python3

"""
SPAMCANNON!
"""

import argparse
import collections
import csv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import locale
import smtplib
import sys
import time

locale.setlocale(locale.LC_ALL, '') # for comma formatting

#PROJECTS = ['MC2', 'ERDOS']
PROJECTS = ['Ray']

MAIL_SERVER = "localhost"
EMAIL_FROM_ADDR = "risecamp@cs.berkeley.edu"
EMAIL_REPLY_ADDR = "risecamp@cs.berkeley.edu"

EMAIL_SUBJECT = "IMPORTANT: RISECamp 2020 Tutorial Links"

EMAIL_PREAMBLE = """
Greetings from RISELab!  Here are the links for your online tutorials for Thursday, Oct 29 2020:
"""
# Greetings from RISELab!  Here are the links for your online tutorials for Friday, Oct 30 2020:

def generate_spam(attendee_hash, send_email=True, delay=1):
    """
    for each hash entry in destination, send a corresponding set of project links
    """
    outfile = '/tmp/OUT'

    burst = 60 # 60 emails before pause
    pause = 30 # pause for 30
    count = 0

    of = open(outfile, 'w')

    for email in attendee_hash:
        print(attendee_hash[email])
        message_body = attendee_hash[email]['fname'] + ' ' + attendee_hash[email]['lname'] + ',' + \
	               EMAIL_PREAMBLE + \
                       '\n'

        for project in PROJECTS:
            message_body += project + '\n' + \
                            attendee_hash[email][project.lower() + '-ip'] + '\n\n'

        message_body += """
Please join the RISECamp 2020 Slack workspace for discussion and technical support:
https://join.slack.com/t/risecamp20/shared_invite/zt-i420qexf-o1p~dtY9GntwBYi4AAwNnQ
        """
        of.write('\n' + email)
        of.write(message_body)

        if send_email:
            print('sending email to %s' % email)
            if count == burst:
                print('sleeping for %s' % pause)
                count = 0
                time.sleep(pause)

            message_body = MIMEText(message_body)

            msg = MIMEMultipart()
            msg['Subject'] = EMAIL_SUBJECT
            msg['From'] = EMAIL_FROM_ADDR
            msg['To'] = email
            msg['Reply-To'] = EMAIL_REPLY_ADDR
            msg.attach(message_body)

            s = smtplib.SMTP(MAIL_SERVER)
            s.sendmail(EMAIL_FROM_ADDR,
                       [email],
                       msg.as_string())
            time.sleep(delay)
            count = count + 1


def parse_attendees(input_data):
    """
    read in a CSV, populate a hash
    """
    attendee_hash = collections.defaultdict(dict)
    with open(input_data, 'r') as f:
        attendee_raw = f.read()

    attendee_data = csv.reader(attendee_raw.split('\n'))

    for row in attendee_data:
        if row:
            print(row)
            email = row[2]
            attendee_hash[email]['fname'] = row[0]
            attendee_hash[email]['lname'] = row[1]
            attendee_hash[email]['mc2-ip'] = row[4]
            attendee_hash[email]['ray-ip'] = row[5]
            attendee_hash[email]['erdos-ip'] = row[6]

    return attendee_hash


def parse_args():
    """
    parse CLI args
    """
    desc = """send emails using csv input"""
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument("-i",
                        "--input",
                        help="""csv input data of attendees""",
                        type=str,
                        metavar="INPUT_DATA")
    parser.add_argument("-d",
                        "--delay",
                        help="""delay in seconds between deliveries""",
                        type=float,
                        metavar="DELAY")
    parser.add_argument("-e",
                        "--email",
                        help="""actually send the emails""",
                        action="store_true")

    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    if not args.input:
        print('please provide the path to the csv file')
        sys.exit(-1)

    attendees = parse_attendees(args.input)
    generate_spam(attendees)

if __name__ == "__main__":
    main()
