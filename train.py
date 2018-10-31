import os
import requests
from requests_toolbelt import MultipartEncoder

train_path = './train'
HOST = 'http://demo.meerkat.com.br/frapi/'
api_key = '95c21fd452968c09aeb8aff25fa0f427'

if __name__ == "__main__":
    for label_name in os.listdir(train_path):
        output = "Registering: {}".format( label_name )
        for image_name in os.listdir(train_path+'/'+label_name):
            filename = train_path+'/'+label_name+'/'+image_name
            if not os.path.isfile( filename ):
                continue
            output += "\n   Image: {}".format(  image_name )

            m = MultipartEncoder(fields={'image': ('filename', open(filename, 'rb')),
                                         'label': label_name})
            res = requests.post(HOST+'/train/person', data=m,
                        headers={'Content-Type': m.content_type, 'api_key': api_key})
            output += "\n      Result: {}".format( res.ok )
            json = res.json()
            if 'message' in json:
                output += "\n      Message: {}".format( json[ 'message' ] )
            if 'error' in json:
                output += "\n      Error: {}".format( json[ 'error' ] )
            output += '\n'
        print output
