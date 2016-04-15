from application import Application
from boto import config

print config.get('Credentials', 'aws_access_key_id')
print config.get('Credentials', 'aws_secret_access_key')
print
app = Application()
