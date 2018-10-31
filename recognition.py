import os
import requests
from requests_toolbelt import MultipartEncoder

recognition_path = './recognition'
HOST = 'http://demo.meerkat.com.br/frapi/'
api_key = '95c21fd452968c09aeb8aff25fa0f427'

if __name__ == "__main__":
    for label_name in os.listdir(recognition_path):
        filename = recognition_path+'/'+label_name
        if not os.path.isfile( filename ):
            continue
        m = MultipartEncoder(fields={'image': ('image', open(filename, 'rb'))})

        res = requests.post(HOST+'/recognize/people', data=m,
                    headers={'Content-Type': m.content_type, 'api_key': api_key})
        people = res.json()[ 'people' ]

        output = "Result for {}:".format( label_name )
        for person in people:
            label = person[ 'recognition' ][ 'predictedLabel' ]
            confidence = person[ 'recognition' ][ 'confidence' ]
            if label != 'None' and confidence:
                output = output + "\n   Found label {} with confidence {}".format(
                        label, confidence )
            else:
                output = output + "\n   Face not recognized"
            output = output + "\n"

        if not people:
            output = output + "\n   No face found."
            output = output + "\n"

        print output
