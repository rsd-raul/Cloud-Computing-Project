from application import Application
from boto import config

print "\nBoto.config test:"

print "\tCredentials"
print '\t\t', config.get('Credentials', 'aws_access_key_id')
print '\t\t', config.get('Credentials', 'aws_secret_access_key')
print '\t\t', config.get('Credentials', 'region')

print "\tBoto"
print '\t\t', config.get('Boto', 'cloudwatch_region_name')
print '\t\t', config.get('Boto', 'cloudwatch_region_endpoint')
print '\t\t', config.get('Boto', 'autoscale_endpoint')

print "\tLibCloud"
print '\t\t', config.get('LibCloud', 'username')
print '\t\t', config.get('LibCloud', 'secret_key')
print '\t\t', config.get('LibCloud', 'auth_url')

app = Application()
