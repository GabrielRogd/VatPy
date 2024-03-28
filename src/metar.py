import requests


def get_METAR(ICAO):
    url = f'https://metar.vatsim.net/{ICAO}'
    response = requests.get(url)

    if response.status_code == 200:
        if not response.text.strip():
            return "ICAO code either does not exist or there's no connection with metar.vatsim.net"
        else:
            return response.text
    else:
        return "Could not connect to the METAR service."

def decode_METAR(METAR):
    split_METAR = METAR.split(' ')  # Breaks between METAR data

    ICAO = METAR[:4]
    wind_direction = 'N/A'
    wind_speed = 'N/A'
    temperature = 'N/A'
    dew_point = 'N/A'
    cloud_info = 'Clouds: CAVOK'
    cloud_categories = ['SKC', 'CLR', 'FEW', 'SCT', 'BKN', 'OVC', 'NCD', 'CAVOK']
    cloud_info_list = []
    cloud_altitude = 'N/A'
    baro = 'N/A'

    for item in split_METAR:
        if item.endswith('KT'):
            wind_info = item[:-2]  # remove 'KT' (knots) from wind data
            wind_direction = wind_info[:3]
            wind_speed = wind_info[3:]

        elif '/' in item:  # temperature and dew point
            parts = item.split('/')
            temperature = parts[0]
            dew_point = parts[1] if len(parts) > 1 else 'N/A'
        for i in cloud_categories:
            if item.startswith(i):
                cloud_info = item[:3]
                cloud_altitude = item[3:] if len(item) > 3 else 'N/A'
                if cloud_altitude.startswith("0"):
                    cloud_altitude = item[4:]
                if cloud_info == 'SKC':
                    cloud_info = 'Scattered'
                elif cloud_info == 'CLR':
                    cloud_info = "Clear skies below 12000 feet"
                elif cloud_info == 'FEW':
                    cloud_info = 'Few clouds'
                elif cloud_info == 'SCT':
                    cloud_info = 'Scattered'
                elif cloud_info == 'BKN':
                    cloud_info = 'Broken'
                elif cloud_info == 'OVC':
                    cloud_info = 'Overcast'
                elif cloud_info == 'NCD':
                    cloud_info = 'No significant clouds'
                elif cloud_info == 'CAVOK':
                    cloud_info = 'CAVOK - No clouds'
                full_cloud_info = f"{cloud_info} @ {cloud_altitude}00 feet" if cloud_altitude.isdigit() else cloud_info
                cloud_info_list.append(full_cloud_info)
                combined_cloud_info = ', '.join(cloud_info_list)

        if item.startswith('Q'):  # QNH decoding
            baro = f"QNH: {item[1:]}hpa"

        elif item.startswith('A2') or item.startswith('A3'):  # Altimeter decoding
            baro = f"Altimeter: {item[1:3]}.{item[3:5]}"

    if cloud_info != 'NCD' and cloud_info != 'CLR' and cloud_info != 'CAVOK' and cloud_altitude != 'N/A':
        #decoding = f'\n\nWind Direction: {wind_direction} degrees\nWind Speed: {wind_speed} knots\nTemperature: {temperature} C\nDew Point: {dew_point} C\nClouds: {combined_cloud_info}\n{baro}'
    #return decoding
        print(f"\nMETAR for {ICAO}:\n")
        print(f"Wind Direction: {wind_direction} degrees")
        print(f"Wind Speed: {wind_speed} knots")
        print(f"Clouds: {combined_cloud_info}")
        print(f"Temperature: {temperature}°C")
        print(f"Dew Point: {dew_point}°C")
        print(baro)
        if "NOSIG" in item:
            print("NOSIG - No significant change")

def main():
    ICAO = input('Enter the ICAO code: ')
    METAR = get_METAR(ICAO)
    print('METAR:', METAR)
    if METAR is not None and not METAR.startswith("Could not connect") and not METAR.startswith("ICAO code either does not"):
        if METAR.startswith("ICAO code either does not"):
            quit(-1)
        if METAR.startswith("VATSIM Metar Service"):
            print('No ICAO code entered.')
            main()
            quit()
        decode = input('Would you like this to be decoded? (yes/no): ')
        if decode.lower() != 'no':
            decoded_METAR = decode_METAR(METAR)
            input("\nPress any key to continue: ")
        elif decode.lower() == 'no':
            quit(0)

main()
