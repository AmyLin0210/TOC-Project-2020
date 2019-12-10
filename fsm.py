from transitions.extensions import GraphMachine
from utils import send_text_message

import urllib3, json

def GetHighwayInfo(highway_id, direction_id):
    http = urllib3.PoolManager()
    response = http.request('GET', 'https://1968.freeway.gov.tw/api/getRoadInformation?action=road&freewayid=' + highway_id + '&expresswayid=0&from_milepost=0&end_milepost=3780000')
    response = json.loads(response.data)['response']
    highway_info = {
        'from_location':         [ x['from_location'] for x in response if x['directionid'] == direction_id],
        'section_average_speed': [ x['section_average_speed'] for x in response if x['directionid'] == direction_id],
        'end_location':          [ x['end_location'] for x in response if x['directionid'] == direction_id],
    }
    return highway_info

# def GetHighWaySpeed(direction, start_location, end_location, heighway_info):
    
    

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
        self.start_location = ""
        self.end_location   = ""
        self.highway_id     = -1
        self.direction      = ""
        self.highway_info   = []

    def is_going_to_quit(self, event):
        text = event.message.text
        if any(x in text.lower() for x in ['exit', 'quit', '離開']):
            return True
        return False
    
    def is_going_to_start_chatting(self, event):
        text = event.message.text
        return True

    def is_going_to_which_road(self, event):
        text = event.message.text
        return True
    
    def is_going_to_which_direction(self, event):
        text = event.message.text
        self.highway_id = '-1'
        if any(x in text.lower() for x in ['國三', '國道三號', '國道3號', '國3']):
            self.highway_id = '3'
        if any(x in text.lower() for x in ['國一', '國道一號', '國道1號', '國1']):
            self.highway_id = '1'
        if not self.highway_id == '-1':
            return True
        return False

    def is_going_to_ask_road_start(self, event):
        text = event.message.text
        self.direction = '-1'

        if any(x in text.lower() for x in ['北上', '北', '往北']):
            self.direction = '4'
        if any(x in text.lower() for x in ['南下', '南', '往南']):
            self.direction = '3'
        if not self.direction == '-1':   
            self.highway_info = GetHighwayInfo(self.highway_id, self.direction) 
            return True
    
        return False

    def is_going_to_ask_road_end(self, event):
        text = event.message.text
        if text in self.highway_info['from_location']:
            self.from_location = text
            return True
        else:
            return False

    def is_going_to_get_speed(self, event):
        text = event.message.text
        if text in self.highway_info['end_location']:
            self.end_location = text
            return True
        else:
            return False
    
    def on_enter_start_chatting(self, event):
        print("I'm entering which_road") 

        reply_token = event.reply_token
        send_text_message(reply_token, "輸入任意字開始查詢") 

    def on_enter_quit(self, event):
        print("I'm entering which_road")

        reply_token = event.reply_token
        send_text_message(reply_token, "請問你要查詢哪條國道？")

    def on_enter_which_road(self, event):
        print("I'm entering which_road")

        reply_token = event.reply_token
        send_text_message(reply_token, "請問你要查詢哪條國道？")

    def on_enter_which_direction(self, event):
        print("I'm entering which_direction")

        reply_token = event.reply_token
        send_text_message(reply_token, "請問您要北上/南下？")

    def on_enter_ask_road_start(self, event):
        print("I'm entering road_start")

        reply_token = event.reply_token
        send_text_message(reply_token, "請輸入起始交流道") 
    
    def on_enter_ask_road_end(self, event):
        print("I'm entering road_end")

        reply_token = event.reply_token
        send_text_message(reply_token, "請輸入終點交流道")

    def on_enter_get_speed(self, event):
        print("I'm entering road_end")
        from_index = self.highway_info['from_location'].index(self.from_location)
        to_index   = self.highway_info['end_location'].index(self.end_location)

        speed_string = ""

        for i in range( min(from_index, to_index), max(from_index, to_index) + 1):
            speed_string += self.highway_info['from_location'][i] + " -> " 
            speed_string += self.highway_info['end_location'][i] + " : " 
            speed_string += str(self.highway_info['section_average_speed'][i])  + "\n"
        
        speed_string += "查詢結束，輸入任意鍵重新開始"

        reply_token = event.reply_token
        send_text_message(reply_token, speed_string)
        self.go_back()

