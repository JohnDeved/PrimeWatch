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

# Make a POST request to 'https://gaming.amazon.com/graphql' with the extracted 'set-cookie' and 'csrf-key'
graphql_url = 'https://gaming.amazon.com/graphql'
headers = {
    'Content-Type': 'application/json',
    'Cookie': set_cookie,
    'csrf-token': csrf_key
}
data = {
    "operationName": "OffersContext_Offers_And_Items",
    "variables": {
        "pageSize": 999
    },
    "extensions": {},
    "query": "query OffersContext_Offers_And_Items($dateOverride: Time, $pageSize: Int) {\n  games: items(collectionType: FREE_GAMES, dateOverride: $dateOverride, pageSize: $pageSize) {\n    items {\n      ...Item\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment Item on Item {\n  id\n  isFGWP\n  isDirectEntitlement\n  isRetailLinkItem\n  grantsCode\n  priority\n  category\n  ctaButtonText\n  isTeaserCard\n  showCountdownInHours\n  assets {\n    id\n    title\n    externalClaimLink\n    shortformDescription\n    cardMedia {\n      defaultMedia {\n        src1x\n        src2x\n        type\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  product {\n    id\n    __typename\n  }\n  offers {\n    id\n    startTime\n    endTime\n    offerSelfConnection {\n      eligibility {\n        offerState\n        isClaimed\n        conflictingClaimAccount {\n          obfuscatedEmail\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  game {\n    id\n    isActiveAndVisible\n    assets {\n      title\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n"
}

response = requests.post(graphql_url, headers=headers, json=data)

# Log the results of the POST request to the console
print(response.json())
