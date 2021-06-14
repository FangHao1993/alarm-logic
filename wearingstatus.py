import requests
import json
import logging


FORMAT = '%(asctime)s %(levelname)s: %(message)s'
logging.basicConfig(level=logging.INFO, filename='Log.log', filemode='a', format=FORMAT)

def getwearingstatus(machine_no):
    ip = ''
    url = f'{ip}/overview/security/machineOD/?machine_NO={machine_no}'
    try:
        response = requests.get(
            url = url
        )
    except:
        logging.info(f'get waring status error {url}')
    if response.status_code != 200:
        print(f'status is not 200 ({response.status_code})')
        return 
    codes = json.loads(response.text)

    human_count = codes["human_count"] 

    status = codes["status"]
    
    helmet = codes["helmet"]
    # if helmet == 2:
    #     helmet = 1
    shoes = codes["shoes"]
    # if shoes == 2:
    #     shoes = 1
    gloves = codes["gloves"]
    # if gloves == 2:
    #     gloves = 1
    glasses = codes["glasses"]
    # if glasses == 2:
    #     glasses = 1
    staffstatus = str(status) + str(helmet) + str(shoes) + str(gloves) + str(glasses)
    #image = codes["image"]

    helmet_color = codes["helmet_color"]
    red_vest = codes["red_vest"]

    time = codes["time"]
    # print(codes)
    # print(f'status : {status}')
    # print(f'helmet : {helmet}')
    # print(f'shoes : {shoes}')
    # print(f'gloves : {gloves}')
    # print(f'glasses : {glasses}')
    # print(f'human_count : {human_count}')
    # #print(f'image : {image}')
    # print(f'helmet_color : {helmet_color}')   
    # print(f'red_vest : {red_vest}')
    # print(f'time : {time}')
    # print(f'staffstatus : {staffstatus}')

    #return staffstatus,human_count,image,time
    
    return staffstatus,helmet_color,red_vest,human_count,time