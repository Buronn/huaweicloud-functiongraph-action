import json
import os
from flask import Flask

app = Flask(__name__)

@app.route('/invoke', methods=['POST'])
def invoke():
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Your API Key is: " + os.environ['API_KEY'] + " and your other value is: " + os.environ['OTHER_VALUE']
        }),
    }

def handler(event, context):
    return invoke()

if __name__ == '__main__':
    app.run( host='0.0.0.0', port=8000)