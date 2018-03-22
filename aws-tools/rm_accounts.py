#! /usr/bin/env python3
import sys
import boto3

if len(sys.argv) == 1:
  print(sys.argv[0], 'needs one arg which is a file of AWS ids')
  sys.exit(1)

with open(sys.argv[1], 'r') as f:
  ids = f.readlines()
ids = [x.strip() for x in ids]

c = boto3.client('organizations')

for id in ids:
  r = c.remove_account_from_organization(AccountId=id)
  print('removed account', id, 'from org')
