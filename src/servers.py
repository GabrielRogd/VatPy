import requests
from ping3 import ping
import operator

HTTP_OK = 200
SWEATBOX = 'sweatbox'
VATSIM_API = 'https://data.vatsim.net/v3/all-servers.json'


def fetch_data(api_url):
    response = requests.get(api_url)
    if response.status_code == HTTP_OK:
        return response.json()
    else:
        log_data("Failed to fetch data from VATSIM's API.")
        return None


def log_data(message):
    print(message)


def get_best_server(server_data):
    servers = sorted(server_data, key=operator.itemgetter('name'))
    best_server = None
    best_ping = -1
    for server in servers:
        log_data(f"Checking server: {server['name']}")
        if SWEATBOX in server['name'].lower():
            log_data('SweatBox server. Moving on...')
            continue
        try:
            delay = ping(server['hostname_or_ip'])
            if delay is not None:
                delay_ms = int(delay * 1000)
                log_data(f"Ping: {delay_ms}ms")
                if best_ping == -1 or delay > best_ping:
                    best_server = server
                    best_ping = delay_ms
        except Exception as e:
            log_data(f"Could not ping server {server['name']}: {e}")
    return best_server, best_ping


def main():
    server_data = fetch_data(VATSIM_API)
    if server_data is not None:
        # Raw API output
        # log_data(type(server_data))
        # log_data(server_data)
        best_server, best_ping = get_best_server(server_data)
        if best_server is not None:
            log_data(
                f"The best server to play on is: {best_server['name']} with a ping of {int(best_ping)} milliseconds")
        else:
            log_data("Couldn't find a suitable server.")


main()
