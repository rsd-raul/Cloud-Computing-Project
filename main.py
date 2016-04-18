from application import Application
from boto import config

print "Credentials:"
print '\t', config.get('Credentials', 'aws_access_key_id')
print '\t', config.get('Credentials', 'aws_secret_access_key')

app = Application()
