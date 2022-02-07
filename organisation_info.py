import requests

api_key = 'dda3ddba-c9ea-4ead-9010-f43fbc15c6e3'


def get_organisation_info(ll):
    search_api_server = "https://search-maps.yandex.ru/v1/"

    search_params = {
        "apikey": api_key,
        "lang": "ru_RU",
        "ll": ll,
        "text": ll
    }

    response = requests.get(search_api_server, params=search_params)

    if not response:
        print("Invalid request", response.content)
        return

    json_response = response.json()
    organization = json_response["features"][0]
    org_name = organization["properties"]["CompanyMetaData"]["name"]
    org_address = organization["properties"]["CompanyMetaData"]["address"]

    info = {
        "name": org_name,
        "address": org_address
    }

    return info


if __name__ == '__main__':
    print(get_organisation_info('37.530887,55.703118'))
