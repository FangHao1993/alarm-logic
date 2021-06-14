from wearingstatus import getwearingstatus
from machinestatus import getmachinestatus
import time
import datetime
import requests
import os
import random
import vlc
import logging


FORMAT = '%(asctime)s %(levelname)s: %(message)s'
logging.basicConfig(level=logging.INFO, filename='Log.log', filemode='a', format=FORMAT)

class Playmp3(object):
    def __init__(self):
        self.change_time = 1
        #新增紀錄上次偵測結果比較
        self.machine_no_wearing_status = {}
        #2021/05/25 新增判斷上次著裝是否皆為合法 '111'
        self.machine_no_wearing_status_no_glasses = {}

    
    def load_info(self, machine_no):
        print(f'machine_no : {machine_no}')
        try:
            self.getwearingstatus = getwearingstatus(machine_no)
            print(f'Getwearingstatus.staffstatus : {self.getwearingstatus}')

        except:
            logging.info(f'{machine_no} wearingstatus.py reutrn error')
            self.getwearingstatus = ('12222', 0, 0, -1, ' ')
        try:
            self.getmachinestatus = getmachinestatus(machine_no)
            injection_status = self.getmachinestatus[1]
            print(f'Getmachinestatus : {self.getmachinestatus}')
        except:
            if machine_no == 'D17':
                logging.info(f'{machine_no} machinestatus.py reutrn error')   
            self.getmachinestatus = ('1', '1')
            injection_status = self.getmachinestatus[1]

        system_status = self.getwearingstatus[0][0]
        wearing_status = self.getwearingstatus[0][1:]
        #20210527 新增安全帽顏色及紅色馬甲判斷
        helmet_color = self.getwearingstatus[1]
        red_vest = self.getwearingstatus[2]
        who_name = self.getwearingstatus[3]
        time = self.getwearingstatus[4]

        #2021/05/25 新增判斷上次著裝是否皆為合法 '111'
        # wearing_status_no_glasses = self.getwearingstatus[0][1:4]

        #2021/06/04 修改規乖寶機制各裝備各別判斷
        wearing_status_no_glasses = {}
        wearing_status_no_glasses['helmet'] = self.getwearingstatus[0][1]
        wearing_status_no_glasses['shoes'] = self.getwearingstatus[0][2]
        wearing_status_no_glasses['gloves'] = self.getwearingstatus[0][3]
        wearing_status_no_glasses['time'] = time

        if not os.path.exists(f'note{os.sep}{machine_no}{os.sep}'):
            os.makedirs(f'note{os.sep}{machine_no}{os.sep}')

        # with open(f"note{os.sep}{machine_no}{os.sep}test_output.txt", "a") as f:
        #         f.write(f'real_data {time} {wearing_status_no_glasses} {helmet_color} {red_vest}\n')
        
        if machine_no not in self.machine_no_wearing_status_no_glasses:
            self.machine_no_wearing_status_no_glasses[machine_no] = wearing_status_no_glasses
            
        elif self.machine_no_wearing_status_no_glasses[machine_no]['time'] == time:
            return

        wearing_status_new = ''
        for i  in range(len(wearing_status)):
            if wearing_status[i] == '2':
                wearing_status_new += '1'
            else:
                wearing_status_new += wearing_status[i]
        print(f'before wearing_status_new no "2" : {wearing_status_new}')

        #20210527 新增安全帽顏色及紅色馬甲判斷
        if helmet_color == 2:
            with open(f"note{os.sep}{machine_no}{os.sep}helmet_color.txt", "a") as f:
                f.write(f'white before {time} {wearing_status_new}\n')
            wearing_status_new = wearing_status_new[0] + '1' + wearing_status_new[2:]
            with open(f"note{os.sep}{machine_no}{os.sep}helmet_color.txt", "a") as f:
                f.write(f'white after {time} {wearing_status_new}\n')
            if red_vest == 1:
                with open(f"note{os.sep}{machine_no}{os.sep}helmet_color.txt", "a") as f:
                    f.write(f'white and red before {time} {wearing_status_new}\n')
                # wearing_status_new = wearing_status_new[0:2] + '1' + wearing_status_new[-1]
                wearing_status_new = '1111'
                with open(f"note{os.sep}{machine_no}{os.sep}helmet_color.txt", "a") as f:
                    f.write(f'white and red after {time} {wearing_status_new}\n')

        #2021/06/04 修改規乖寶機制各裝備各別判斷()
        if self.machine_no_wearing_status_no_glasses[machine_no]['helmet'] == '1':
            with open(f"note{os.sep}{machine_no}{os.sep}helmet.txt", "a") as f:
                f.write(f'before {time} {wearing_status_new}\n')
            wearing_status_new = '1' + wearing_status_new[1:]
            with open(f"note{os.sep}{machine_no}{os.sep}helmet.txt", "a") as f:
                f.write(f'after {time} {wearing_status_new}\n')
        if self.machine_no_wearing_status_no_glasses[machine_no]['shoes'] == '1':
            with open(f"note{os.sep}{machine_no}{os.sep}shoes.txt", "a") as f:
                f.write(f'after {time} {wearing_status_new}\n')
            wearing_status_new = wearing_status_new[0] + '1' + wearing_status_new[2:]
            with open(f"note{os.sep}{machine_no}{os.sep}shoes.txt", "a") as f:
                f.write(f'before {time} {wearing_status_new}\n')
        if self.machine_no_wearing_status_no_glasses[machine_no]['gloves'] == '1':
            with open(f"note{os.sep}{machine_no}{os.sep}gloves.txt", "a") as f:
                f.write(f'before {time} {wearing_status_new}\n')
            wearing_status_new = wearing_status_new[0:2] + '1' + wearing_status_new[-1]
            with open(f"note{os.sep}{machine_no}{os.sep}gloves.txt", "a") as f:
                f.write(f'after {time} {wearing_status_new}\n')

        # with open(f"note{os.sep}{machine_no}{os.sep}test_output.txt", "a") as f:
        #         f.write(f'before {time} {machine_no} {self.machine_no_wearing_status_no_glasses[machine_no]}\n')
        if injection_status == '0':
            wearing_status_new = wearing_status_new[:-1] + '1'
        # print(f'wearing_status_new think about injection_status {machine_no} : {wearing_status_new}')
        print(f'after wearing_status_new no "2" : {wearing_status_new}')
        if system_status == '1':

            #新增判斷紀錄上次偵測結果比較
            if machine_no in self.machine_no_wearing_status:
                #新增紀錄上次偵測結果比較
                if self.machine_no_wearing_status[machine_no] != wearing_status_new:
                    self.machine_no_wearing_status[machine_no] = wearing_status_new
                    
                    if wearing_status_new != '1111':
                        #播放二進制01轉換寫進資料庫
                        int_wearing_status_new = pow(2, len(wearing_status_new)) - 1 - int(wearing_status_new,2)
                        emp_id_str = str(who_name)
                        message = {
                            "TIME":time,
                            #"IMAGE":image,
                            "MACHINE": machine_no,
                            "EMP_ID": emp_id_str,
                            "VOILATION_CODE": int_wearing_status_new,
                            "HELMET_COLOR":helmet_color,
                            "RED_VEST":red_vest,
                            "TEST":0,
                        }
                        ip = '' 
                        try:
                            req = requests.post(f'{ip}/api/machine_VIO/', data=message)
                            print(req)
                        except:
                            logging.info(f'write data error') 

            else:
                self.machine_no_wearing_status[machine_no] = wearing_status_new

            
            self.machine_no_wearing_status_no_glasses[machine_no] = wearing_status_no_glasses
            # with open(f"note{os.sep}{machine_no}{os.sep}test_output.txt", "a") as f:
            #     f.write(f'after {time} {machine_no} {self.machine_no_wearing_status_no_glasses[machine_no]}\n')

            notice_playkey = {}
            if wearing_status_new != '1111':
                self.change_time = 2
                notice_playkey = {
                    "0000":"output14.mp3",
                    "0001":"output10.mp3", 
                    "0010":"output11.mp3", 
                    "0011":"output4.mp3",
                    "0100":"output12.mp3", 
                    "0101":"output5.mp3",
                    "0110":"output6.mp3",
                    "0111":"output0.mp3",
                    "1000":"output13.mp3",
                    "1001":"output7.mp3",
                    "1010":"output8.mp3",
                    "1011":"output1.mp3",
                    "1100":"output9.mp3",
                    "1101":"output2.mp3",
                    "1110":"output3.mp3"
                    }
                notice_sound = notice_playkey[wearing_status_new]
                name_playkey = {
                    "-1":"output.mp3",
                    "0":"output0.mp3",
                    "1":"output1.mp3", 
                    "2":"output2.mp3", 
                    "3":"output3.mp3",
                    "4":"output4.mp3", 
                    "5":"output5.mp3",
                    }
                name_sound = name_playkey[str(who_name)]
        
                print(f'notice_sound : {notice_sound}')
                return name_sound, notice_sound, wearing_status_new, time

            else:
                self.change_time = 1

    def playmp3(self, machine_dict):
            print(f'{machine_dict["machine_name"]}')
            notice_media = f'noticeoutput{os.sep}output.mp3'
            machine_media = f'machine_name{os.sep}{machine_dict["machine_name"]}.mp3'
            name_media = f'nameoutput{os.sep}{machine_dict["name_sound"]}'
            wearing_notice_media = f'noticeoutput{os.sep}{machine_dict["notice_sound"]}'
            # wearing_notice_media = f'noticeoutput{os.sep}output_final.mp3'
            media_list = [notice_media, machine_media, name_media, wearing_notice_media]
            for i in media_list:
                media = vlc.MediaPlayer(i)
                media.play()
                while True:
                    if media.get_state() == 6:
                        media.stop()
                        break


machine_list = ['D17', 'D18']

Play = Playmp3()

while True:
    trigger_list = []
    for machine_name in machine_list:
        sound_dict = {}
        load_info = Play.load_info(machine_name)
        print(f'Play.change_time : {Play.change_time}')
        if Play.change_time == 2:
            sound_dict['machine_name'] = machine_name
            sound_dict['name_sound'] = load_info[0]
            sound_dict['notice_sound'] = load_info[1]
            trigger_list.append(sound_dict.copy())
            with open("voice_ouput.txt", "a") as f:
                f.write(f'{load_info[3]}  {machine_name}  {load_info[2]}\n')
    if len(trigger_list) > 0:
        machine_dict = random.choice(trigger_list)
        Play.playmp3(machine_dict)
    time.sleep(Play.change_time)  

