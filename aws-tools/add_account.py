#! /usr/bin/env python3
import sys
import boto3

if len(sys.argv) == 1:
  print(sys.argv[0], 'needs one arg which is an email adress to invite. \
  optional second argument for a custom welcome message')
  sys.exit(1)

if len(sys.argv) == 3:
  welcome_message = sys.argv[2]
else:
  welcome_message = """
  Welcome to the RISELab AWS consolidated billing family.

  Please read and understand our terms of usage:
  https://rise.cs.berkeley.edu/wiki/resources/aws#usage_policies
  """

c = boto3.client('organizations')
r = c.invite_account_to_organization(
  Target={
    'Id': sys.argv[1],
    'Type': 'EMAIL'
  },
  Notes=welcome_message
)
print('invited account', sys.argv[1], 'to org with message', welcome_message)
