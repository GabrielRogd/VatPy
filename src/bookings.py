import requests
import json


def get_bookings(divisions, types):
    url = "https://atc-bookings.vatsim.net/api/booking"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        for book in data:
            if (not divisions and not types) or (book['division'] in divisions and book['type'] in types):
                booking_info = ("\nCID: " + str(book['cid']) +
                ", Type: " + str(book['type']) +
                ", Callsign: " + str(book['callsign']) +
                ", Starts @: " + str(book['start']) +
                ", Ends @: " + str(book['end']) +
                ", Division: " + str(book['division']) +
                ", Subdivision: " + str(book['subdivision']))
                print(booking_info)
    else:
        print("Couldn't fetch from atc-bookings.vatsim.net/api")


def main():
    print("1. Choose Division (default is EUD for VATEUD)")
    print("2. Choose Type (default is 'booking')")
    print("3 (or enter). Fetch Bookings")
    print("4. Exit")

    chosen_divisions = ['EUD']
    chosen_types = ['booking']

    while True:
        choice = input("\nSelect an option: ")
        if choice == "1":
            division = input("Enter division (like EUD, EUR): ")
            chosen_divisions.append(division)
        elif choice == "2":
            type_ = input("Enter type (like event, booking): ")
            chosen_types.append(type_)
        elif choice == "3":
            print("Fetching bookings...")
            get_bookings(chosen_divisions, chosen_types)
        elif choice == "4":
            print("Returning to main.py")
            quit(0)
        else:
            get_bookings(chosen_divisions, chosen_types)


if __name__ == "__main__":
    main()