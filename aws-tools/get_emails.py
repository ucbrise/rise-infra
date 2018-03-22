#! /usr/bin/env python3
import sys
import boto3

c = boto3.client('organizations')

r = c.list_accounts()
while True:
  for acct in r['Accounts']:
    if acct['Status'] == 'ACTIVE':
      print(acct['Email'], acct['Id'])
    else:
      print('suspended/other:', acct['Email'], acct['Id'])
  if 'NextToken' in r:
    r = c.list_accounts(NextToken=r['NextToken'])
  else:
    break

