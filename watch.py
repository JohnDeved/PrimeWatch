import requests
from bs4 import BeautifulSoup
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime
import configparser

def load_webhook_url():
    """
    Load the Discord webhook URL from the config.ini file.
    """
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['webhook']['url']

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

def create_discord_embeds(games):
    """
    Create Discord embeds for each game in the GraphQL response.
    """
    embeds = []
    for game in games:
        start_time = datetime.fromisoformat(game['offers'][0]['startTime'].replace('Z', '+00:00'))
        end_time = datetime.fromisoformat(game['offers'][0]['endTime'].replace('Z', '+00:00'))
        start_timestamp = int(start_time.timestamp())
        end_timestamp = int(end_time.timestamp())
        time_display = f"Offer available from <t:{start_timestamp}:R> to <t:{end_timestamp}:R>"
        embed = {
            "title": game['assets']['title'],
            "description": f"{game['assets']['shortformDescription']}\n\n{time_display}\n\n[claim now ↗]({game['assets']['externalClaimLink']})",
            "url": game['assets']['externalClaimLink'],
            "image": {
                "url": game['assets']['cardMedia']['defaultMedia']['src2x']
            }
        }
        embeds.append(embed)
    return embeds

def send_to_discord(webhook_url, embeds):
    """
    Send the embeds to the provided Discord webhook URL.
    """
    for i in range(0, len(embeds), 10):
        data = {
            "embeds": embeds[i:i + 10]
        }
        response = requests.post(webhook_url, json=data)
        if response.status_code != 204:
            print(f"Failed to send webhook: {response.status_code}, {response.text}")
    return response.status_code

def main():
    """
    Main function to get CSRF and cookie, make GraphQL request, and send the results to the Discord webhook.
    """
    set_cookie, csrf_key = get_csrf_and_cookie()
    graphql_response = make_graphql_request(set_cookie, csrf_key)
    print(graphql_response)
    games = graphql_response['data']['games']['items']
    embeds = create_discord_embeds(games)
    webhook_url = load_webhook_url()
    send_to_discord(webhook_url, embeds)

if __name__ == "__main__":
    main()
