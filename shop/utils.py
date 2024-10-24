
# Creating a 5-digit code
def create_random_code(count):
    import random
    return random.randint(10**4, 10**count-1)

#----------------------------------------------------------------
# send code to user
from kavenegar import *
def send_sms(mobile_number, message):
    try:
        api = KavenegarAPI('325363583567595A4553756556626454366F6131662B502B794A7935347141694B4D59366374566577346F3D')
        params = { 'sender' : '1000689696', 'receptor': mobile_number, 'message': message}
        response = api.sms_send(params)
        return response
    except APIException as error:
        print(f'error1: {error}')
    except HTTPException as error:
        print(f'error2: {error}')

#----------------------------------------------------------------
# class for upload images
import os
from uuid import uuid4  # می تواند رشته های تصادفی منحصر به فرد تولید کند
class FileUpload():
    def __init__(self, dir, prefix):
        self.dir = dir    
        self.prefix = prefix
    
    def upload_to(self, instance, filename):
        filename, ext = os.path.splitext(filename)
        return f'{self.dir}/{self.prefix}/{uuid4()}{ext}'
    
    

#----------------------------------------------------------------
def price_by_delivery_tax(price, discount=0):
    delivery = 25_000
    if price > 200_000:
        delivery = 0
    tax = (price + delivery) * 0.1
    sum = (price + delivery + tax)
    sum = sum - (sum * discount/100)
    return int(sum), delivery, int(tax)