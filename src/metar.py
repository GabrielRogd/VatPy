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

    wind_direction = 'N/A'
    wind_speed = 'N/A'
    temperature = 'N/A'
    dew_point = 'N/A'
    cloud_info = 'Clouds: CAVOK'
    cloud_altitude = 'N/A'
    altimeter_info = 'N/A'

    for item in split_METAR:
        if item.endswith('KT'):
            wind_info = item[:-2]  # remove 'KT' (knots) from wind data
            wind_direction = wind_info[:3]
            wind_speed = wind_info[3:]

        elif '/' in item:  # temperature and dew point
            parts = item.split('/')
            temperature = parts[0]
            dew_point = parts[1] if len(parts) > 1 else 'N/A'

        elif item.startswith(('SKC', 'CLR', 'FEW', 'SCT', 'BKN', 'OVC', 'NCD', 'CAVOK')):
            cloud_info = item[:3]
            if cloud_info == 'SKC':
                cloud_info = "Scattered @"
            elif cloud_info == 'CLR':
                cloud_info = "Clear skies below 12000 feet"
            elif cloud_info == 'FEW':
                cloud_info = 'Few clouds @'
            elif cloud_info == 'SCT':
                cloud_info = 'Scattered @'
            elif cloud_info == 'BKN':
                cloud_info = 'Broken @'
            elif cloud_info == 'OVC':
                cloud_info = 'Overcast @'
            elif cloud_info == 'NCD':
                cloud_info = 'No significant clouds'
            elif cloud_info == 'CAVOK':
                return cloud_info
            cloud_altitude = item[3:] if len(item) > 3 else 'N/A'

        elif item.startswith('Q'):  # QNH decoding
            altimeter_info = f"QNH: {item[1:]}hpa"

        elif item.startswith('A2') or item.startswith('A3'):  # Altimeter decoding
            altimeter_info = f"Altimeter: {item[1:3]}.{item[3:5]}"

    if cloud_info != 'NCD' and cloud_info != 'CLR' and cloud_info != 'CAVOK' and cloud_altitude != 'N/A':
        cloud_altitude_normalised = str(
            (str(int(cloud_altitude) * 100) if cloud_altitude.isdigit() else 'N/A') + ' feet')
        decoding = f'\n\nWind Direction: {wind_direction} degrees\nWind Speed: {wind_speed} knots\nTemperature: {temperature} C\nDew Point: {dew_point} C\nClouds: {cloud_info} {cloud_altitude_normalised}\n{altimeter_info}'
    else:
        decoding = f'\n\nWind Direction: {wind_direction} degrees\nWind Speed: {wind_speed} knots\nTemperature: {temperature} C\nDew Point: {dew_point} C\nClouds: {cloud_info}\n{altimeter_info}'

    return decoding


def main():
    ICAO = input('Enter the ICAO code: ')
    METAR = get_METAR(ICAO)

    print('METAR:', METAR)
    if METAR is not None and not METAR.startswith("Could not connect") and not METAR.startswith("ICAO code does not"):
        if METAR.startswith("ICAO code does not"):
            quit(-1)
        if METAR.startswith('VATSIM Metar Service'):
            print('No ICAO code entered.')
            main()
            quit()
        decode = input('Would you like this to be decoded? (yes/no): ')
        if decode.lower() != 'no':
            decoded_METAR = decode_METAR(METAR)
            print('Decoded METAR:', decoded_METAR, "\n")
            input("Press any key to continue: ")
        elif decode.lower() == 'no':
            quit(0)


main()  # Execute
