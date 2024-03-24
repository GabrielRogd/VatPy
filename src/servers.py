import requests
from ping3 import ping
import operator

response = requests.get('https://data.vatsim.net/v3/all-servers.json') # Fetch data from VATSIM API (v3)

if response.status_code == 200: # 200 is success code, else throw error.
    data = response.json()

    print(type(data))  # Print the type of data
    print(data)  # Print the content of data

    # Extract the server list and sort by name
    servers = sorted(data, key=operator.itemgetter('name'))

    best_server = None
    best_ping = -1

    # Loop over all servers
    for server in servers:
        print(f"Checking server: {server['name']}")

        if 'sweatbox' in server['name'].lower():
            print('SweatBox server. Moving on...')
            continue

        # Perform a ping check
        try:
            delay = ping(server['hostname_or_ip'])

            # If server responds
            if delay is not None:
                delay_ms = delay * 1000
                print(f"Ping: {delay_ms} milliseconds")

                if best_ping == -1 or delay > best_ping:
                    best_server = server
                    best_ping = delay_ms

        except Exception as e:
            print(f"Could not ping server {server['name']}: {e}")

    if best_server is not None:
        print(f"The best server to play on is: {best_server['name']} with a ping of {int(best_ping)} milliseconds")
    else:
        print("Couldn't find a suitable server.")

# unable to fetch
else:
    print("Failed to fetch data from VATSIM's API.")