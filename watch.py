import requests
from bs4 import BeautifulSoup
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def get_csrf_and_cookie():
    """
    Make a GET request to 'https://gaming.amazon.com/home' and extract the 'set-cookie' header and 'csrf-key' value.
    """
    response = requests.get('https://gaming.amazon.com/home')
    set_cookie = response.headers.get('set-cookie')
    soup = BeautifulSoup(response.content, 'html.parser')
    csrf_key = soup.find('input', {'name': 'csrf-key'})['value']
    return set_cookie, csrf_key

def make_graphql_request(set_cookie, csrf_key):
    """
    Make a POST request to 'https://gaming.amazon.com/graphql' with the extracted 'set-cookie' and 'csrf-key'.
    """
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
        "query": """
        query OffersContext_Offers_And_Items($dateOverride: Time, $pageSize: Int) {
          games: items(collectionType: FREE_GAMES, dateOverride: $dateOverride, pageSize: $pageSize) {
            items {
              ...Item
              __typename
            }
            __typename
          }
        }

        fragment Item on Item {
          id
          isFGWP
          isDirectEntitlement
          isRetailLinkItem
          grantsCode
          priority
          category
          ctaButtonText
          isTeaserCard
          showCountdownInHours
          assets {
            id
            title
            externalClaimLink
            shortformDescription
            cardMedia {
              defaultMedia {
                src1x
                src2x
                type
                __typename
              }
              __typename
            }
            __typename
          }
          product {
            id
            __typename
          }
          offers {
            id
            startTime
            endTime
            offerSelfConnection {
              eligibility {
                offerState
                isClaimed
                conflictingClaimAccount {
                  obfuscatedEmail
                  __typename
                }
                __typename
              }
              __typename
            }
            __typename
          }
          game {
            id
            isActiveAndVisible
            assets {
              title
              __typename
            }
            __typename
          }
          __typename
        }
        """
    }

    response = requests.post(graphql_url, headers=headers, json=data)
    return response.json()

def main():
    """
    Main function to get CSRF and cookie, make GraphQL request, and log the results to the console.
    """
    set_cookie, csrf_key = get_csrf_and_cookie()
    print(f"Set-Cookie: {set_cookie}")
    print(f"CSRF-Key: {csrf_key}")
    graphql_response = make_graphql_request(set_cookie, csrf_key)
    print(graphql_response)

if __name__ == "__main__":
    main()
