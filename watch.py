import requests
from bs4 import BeautifulSoup

# Make a GET request to 'https://gaming.amazon.com/home'
response = requests.get('https://gaming.amazon.com/home')

# Extract the 'set-cookie' header from the response
set_cookie = response.headers.get('set-cookie')

# Extract the value of the hidden input field 'csrf-key' from the HTML content
soup = BeautifulSoup(response.content, 'html.parser')
csrf_key = soup.find('input', {'name': 'csrf-key'})['value']

# Output both the 'set-cookie' header and the 'csrf-key' value to the console
print(f"Set-Cookie: {set_cookie}")
print(f"CSRF-Key: {csrf_key}")
