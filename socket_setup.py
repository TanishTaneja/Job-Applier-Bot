import websocket
from data import get_data
from urllib.parse import quote
import json
from data import set_application_data

websocket.enableTrace(True)

def getSocketUrl(applicationId, candidateId, authToken):
  return f"wss://ufatez9oyf.execute-api.us-east-1.amazonaws.com/prod?applicationId={applicationId}&candidateId={candidateId}&authToken={authToken}"

def on_message(ws, message):
    try:
        decoded_message = json.loads(message)
        if decoded_message.get("stepName") == "job-opportunities":
            applicationId = get_data().get("applicationId")
            candidateId = get_data().get("candidateId")
            jobId = get_data().get("jobId")
            generalQuestions = {
                "action": "completeTask",
                "applicationId": applicationId,
                "candidateId": candidateId,
                "requisitionId": "",
                "jobId": jobId,
                "domainType": "CS",
                "state": "MA",
                "employmentType": "Seasonal",
                "eventSource": "HVH-CA-UI",
                "jobSelectedOn": "2025-10-01T20:29:51.280Z",
                "currentWorkflowStep": "job-opportunities",
                "workflowStepName": "",
                "partitionAttributes": {
                    "countryCodes": [
                        "US"
                    ]
                },
                "filteringSeasonal": False,
                "filteringRegular": False
            }
            ws.send(json.dumps(generalQuestions))
    except:
        print(message)

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    candidateId = get_data().get("candidateId")
    applicationId = get_data().get("applicationId")
    jobId = get_data().get("jobId")
    scheduleId = get_data().get("scheduleId")
    data = {
        "action": "startWorkflow",
        "applicationId": applicationId,
        "candidateId": candidateId,
        "jobId": jobId,
        "scheduleId": scheduleId,
        "partitionAttributes": {
            "countryCodes": [
                "US"
            ]
        },
        "filteringSeasonal": False,
        "filteringRegular": False,
        "domainType": "CS"
    }
    ws.send(json.dumps(data))
    print("Opened connection")

def connect(applicationId, jobId, scheduleId):
    accessToken = get_data().get("accessToken")
    auth_token = quote(accessToken, safe='')
    candidateId = get_data().get("candidateId")
    set_application_data(applicationId, jobId, scheduleId)
    ws = websocket.WebSocketApp(getSocketUrl(applicationId, candidateId, auth_token),
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close)
    ws.run_forever(reconnect=5)