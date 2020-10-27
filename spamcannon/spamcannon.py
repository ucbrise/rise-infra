#! /usr/bin/env python3

"""
SPAMCANNON!
"""

import argparse
import collections
import csv
import datetime
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from io import StringIO
import locale
import os
import smtplib
import socket
import sys

locale.setlocale(locale.LC_ALL, '') # for comma formatting

PROJECTS = ['test1', 'foo', 'bar']

TODAY = datetime.date.today()
DAY = TODAY.strftime('%d')
MONTH = TODAY.strftime('%m')
MONTH_NAME = TODAY.strftime('%B')
YEAR = TODAY.strftime('%Y')

MAIL_SERVER = "watson"
EMAIL_FROM_ADDR = "risecamp@cs.berkeley.edu"
EMAIL_REPLY_ADDR = "sknapp+spamcannon@berkeley.edu"

EMAIL_SUBJECT = "IMPORTANT: RISECamp Tutorial Links"

EMAIL_PREAMBLE = """
Greetings from RISELab!  Here are the details for your online tutorials:


"""

def send_email(links, destination):
    """
    for each hash entry in destination, send a corresponding set of project links
    """

def parse_links():
    """
    read in links for each file, store in a dict and return
    """
    link_hash = collections.defaultdict(dict)

    for file in PROJECTS:
        file = file + '-links.txt'
        with open(file, 'r') as f:
            for line in f:
                link = line[:1]
                link_hash[project] = link

    return link_hash

def parse_attendees(input_data):
    """
    read in a CSV, populate a hash
    """
    attendee_hash = collections.defaultdict(dict)
    with open(input_data, 'r') as f:
        attendee_raw = f.read()

    attendee_data = csv.reader(attendee_raw.split('\n'))

    for line in attendee_data:
        
def parse_args():
    """
    parse CLI args
    """
    desc = """send emails using csv input"""
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument("-i",
                        "--input-data",
                        help="""csv input data of attendees""",
                        type=str,
                        metavar="INPUT_DATA")
    parser.add_argument("-d",
                        "--delay"
                        """delay in seconds between deliveries""",
                        type=float,
                        metavar="DELAY")


def main():
    args = parse_args()


if __name__ == "__main__":
    main()
