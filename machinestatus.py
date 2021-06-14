import requests
import json
import logging


FORMAT = '%(asctime)s %(levelname)s: %(message)s'
logging.basicConfig(level=logging.INFO, filename='Log.log', filemode='a', format=FORMAT)


def getmachinestatus(machine_no):
    ip = ''
    url = f'{ip}/api/get_newest_machine_state/?machine_NO={machine_no}'
    try:
        response = requests.get(
            url = url
        )
    except:
        logging.info(f'get machine status error {url}')

    if response.status_code != 200:
        print(f'status is not 200 ({response.status_code})')
        return
    codes = json.loads(response.text)
    moter = codes["moter"]
    injection = codes["injection"]
    # machinestatus = str(moter) + str(injection)
    # print(codes)
    # print(f'moter : {moter}')
    # print(f'injection : {injection}')
    # print(f'machinestatus : {machinestatus}')
    return moter, injection
    


