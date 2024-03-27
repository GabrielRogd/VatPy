import requests
import json

def menu():
    print("1. Choose Division (default is EUD for VATEUD)")
    print("2. Choose Type (default is 'booking')")
    print("3 (or enter). Fetch Bookings")
    print("4. Exit")

def result(cid,type,callsign,start,end,division,subdivision):
        print(f"\nCID: {cid}, Type: {type}, Callsign: {callsign}, Starts @: {start}, Ends @: {end}, Division: {division}, Subdivision: {subdivision} \n")

def get_bookings(divisions, types):
    url = "https://atc-bookings.vatsim.net/api/booking"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        for book in data:
            if (not divisions and not types) or (book['division'] in divisions and book['type'] in types):
                result(book['cid'],book['type'],book['callsign'],book['start'],book['end'],book['division'],book['subdivision'])

    else:
        print("Couldn't fetch from atc-bookings.vatsim.net/api")
    menu()

def main():
    menu()
    chosen_divisions = ['EUD']
    chosen_types = ['booking']
    while True:
        choice = input("\nSelect an option: ")
        if choice == "1":
            division = input("Enter division (e.g. EUD, EUR): ")
            chosen_divisions.append(division)
        elif choice == "2":
            type = input("Enter type (like event, booking): ")
            chosen_types.append(type)
        elif choice == "3":
            print("Fetching bookings...")
            get_bookings(chosen_divisions, chosen_types)
        elif choice == "4":
            quit(0)
        else:
            get_bookings(chosen_divisions, chosen_types)

main()