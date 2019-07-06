import os

try:
    token = os.environ['TOKEN']
    DATABASE_host = os.environ['DATABASE_URL']
except KeyError:
    token = 'bf876c2e8b5ea6ad3922fb2a5f0122da964bd55b097a1d2d80a850ce15dd4ff66d366fda4308bddbee1bf'
    DATABASE_host = 'ec2-54-246-84-100.eu-west-1.compute.amazonaws.com'
    print('Connecting  by PC')
else:
    print('Connecting  by Heruko')

DATABASE_name = 'd122m0li79605d'
DATABASE_user = 'smrvrtzblbgwaq'
DATABASE_password = 'bd142b079573686974fac87d914f609b1355dd3b8cab7e51d407c446c23851b9'
group_id = 182132769
