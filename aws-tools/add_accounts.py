#! /usr/bin/env python3
import sys
import boto3

if len(sys.argv) == 1:
  print(sys.argv[0], 'needs one arg which is a file of AWS ids. \
  optional second argument for a custom welcome message')
  sys.exit(1)

if len(sys.argv) == 3:
  welcome_message = sys.argv[2]
else:
  welcome_message = 'welcome to the AWS consolidated billing family'

with open(sys.argv[1], 'r') as f:
  ids = f.readlines()
ids = [x.strip() for x in ids]

c = boto3.client('organizations')

for id in ids:
  r = c.invite_account_to_organization(
    Target={
      'Id': id,
      'Type': 'ACCOUNT'
      },
    Notes=welcome_message
    )
  print('invited account', id, 'to org with message', welcome_message)
