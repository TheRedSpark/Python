import sys
import time

import requests

from package import variables as v

domain = v.failsave_domain



def failsave() -> bool:
    try:
        response = requests.get(domain, timeout=2)
        if response.status_code == 200:
            return True
        else:
            print(f'Der unbekannte Statuscode lautet: {response.status_code}')
            return False
    except ConnectionError:
        print("Server Offliene ConnectionError")
    except requests.Timeout as err:
        # logger.error({"message": err.message})
        # print(err)
        print("ConnectTimeoutError Server ist wahrscheinlich offline")
    except requests.RequestException as err:
        # handle other errors
        print(err)


def main():
    nicht_erreicht = 0
    while True:
        if not failsave():

            if nicht_erreicht < 86400:
                nicht_erreicht = nicht_erreicht + 1
            time.sleep(nicht_erreicht)
            print(f"Warten zusätzlich nun für {nicht_erreicht} Sekunden")
        else:
            nicht_erreicht = 0
            print(f"Webservice erreichbar ")


if __name__ == '__main__':
    main()
