import apiai
import json

class DialogFlowException(Exception):
    pass

class DialogFlowClient(object):
    CLIENT_ACCESS_TOKEN = "9bc0b7a99eeb4950908a0a29d39a8d4a"

    def __init__(self):
        self.ai = apiai.ApiAI(self.CLIENT_ACCESS_TOKEN)

    def get_results(self, request):
        response = json.loads(request.getresponse().read().decode("utf-8"))
        if response["status"]["code"] != 200:
            raise DialogFlowClient(response["status"]["errorType"])
        return response

    def query(self, msg, session_id=None):
        text_request = self.ai.text_request()
        text_request.query = msg
        if session_id:
            text_request.sessionId = session_id
        response = self.get_results(text_request)
        return response

    def response(self, msg, session_id=None):
        query = self.query(msg, session_id)
        intent = query["result"]['metadata']['intentName']
        slots = query["result"]["parameters"]
        output_message = query["result"]["fulfillment"]["speech"]
        return output_message

if __name__ == "__main__":
    client = DialogFlowClient()
    message = client.response("Weather forecast in San Francisco tomorrow")
    print(message)
