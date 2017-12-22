from nhs_dos import User, Case, SoapApiClient, config

# Create a new User object, passing in your API username and password
u = User(config.API_USERNAME, config.API_PASSWORD)

# Create a new Case object to represent the case for which you would
# like to search
c = Case()

# Set the case attributes on the Case object
c.disposition = '1020'
c.age = '1'
c.age_format = 'AgeGroup'

sa = SoapApiClient(u)

response = sa.check_capacity_summary(c)
print(response)
