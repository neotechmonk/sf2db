import yaml
from simple_salesforce import Salesforce

# Load Salesforce credentials
# salesforce_instance = 'pcm--cebdbdev.sandbox.my.salesforce.com'


# Read the login credentials from login.yaml file
with open('login.yaml', 'r') as file:
    credentials = yaml.safe_load(file)

# Extract the credentials
username = credentials["username"]
password = credentials["password"]
security_token = credentials["security_token"]
consumer_key = credentials["consumer_key"]
consumer_secret = credentials["consumer_secret"]
domain = credentials["domain"]

# Create a Salesforce instance
sf = Salesforce(
    username=credentials["username"],
    password=credentials["password"],
    security_token=credentials["security_token"],
    consumer_key=credentials["consumer_key"],
    consumer_secret=credentials["consumer_secret"],
    domain=credentials["domain"]
)

# Example: Query data from a Salesforce object
query_result = sf.query("SELECT Id, Name FROM Account LIMIT 10")
records = query_result['records']
for record in records:
    print(record['Id'], record['Name'])
