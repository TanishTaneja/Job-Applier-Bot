import websocket
from data import get_data
from urllib.parse import quote
import json
from data import set_application_data
import datetime

# websocket.enableTrace(True)

def getSocketUrl(applicationId, candidateId, authToken):
  return f"wss://ufatez9oyf.execute-api.us-east-1.amazonaws.com/prod?applicationId={applicationId}&candidateId={candidateId}&authToken={authToken}"

def on_message(ws, message):
    try:
        decoded_message = json.loads(message)
        stepName = decoded_message.get("stepName")
        if stepName == "job-opportunities":
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
                "state": "ON",  # TODO: Make it dynamic
                "employmentType": "Seasonal",
                "eventSource": "HVH-CA-UI",
                "jobSelectedOn": datetime.datetime.now().isoformat(),
                "currentWorkflowStep": "job-opportunities",
                "workflowStepName": "",
                "partitionAttributes": {
                    "countryCodes": [
                        "CA"
                    ]
                },
                "filteringSeasonal": False,
                "filteringRegular": False
            }
            ws.send(json.dumps(generalQuestions))
        elif stepName == "general-questions":
            ws.close()
        else:
            print(f"Unknown message: {message}")
            ws.close()
    except Exception as e:
        print("Error occured with message: " + message)
        print(e)

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    pass

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
                "CA"
            ]
        },
        "filteringSeasonal": False,
        "filteringRegular": False,
        "domainType": "CS"
    }
    ws.send(json.dumps(data))

def connect(applicationId, jobId, scheduleId):
    accessToken = "AQICAHidzPmCkg52ERUUfDIMwcDZBDzd+C71CJf6w0t6dq2uqwGsseu8li7IKoV8Z5SwAMb9AAAEUjCCBE4GCSqGSIb3DQEHBqCCBD8wggQ7AgEAMIIENAYJKoZIhvcNAQcBMB4GCWCGSAFlAwQBLjARBAxAmb1x5nDLow+BFR8CARCAggQFgRPbdMhJFnq9xVO0kq4Oaz6/fVZ4zHgqUEXKWlkqwsulie0hA/PL0Hgh0THnC5Muk+u8rDehBdH+dHLlYq5/EBp+VcPCsSLLDZMBUe4SXnI5A0sAoDExMk+gxmpgauheGMK+aSDpNVrJmrqyxcR9hy7bKCMzRk9Kl2PYgQH62lwO5H5BfBUVFzgMUTDoSLNgN0xdjmxMz0S6aqHbFIMHLF+M7KZqPAhyicpzwbEmO44D4sR6ZO4QW3ggv35D+juzoJi/J2rvw+4GgcJEGfJu0G7S5SfWziV9yDIBl/ACApd93L0egRtFG+HoaOtlTTFwig+F/B1u0WJvhhpAaYGiPHdapqSIb7LqatRyeOmepFk/0QXj6IQEBju+YdfU/g+Bz5sTNZqPOwIypwUoXYk82vEcLJGGX9tSUF8VVxHw8RQL0hysBGqZOl3erdPQezVsC/qmxnmpbmDmH2+MPjxxszcoM3ym71a8K+JiRF3UZncMdba5g8KTeLgDBH9rmdUmCl63lcfNoG1Ki77N33PiXAPlRvKCO6yTwadlUqagnuRhz0B/2KFk9FH1cw+GqeCRMKim309pSbkUj3AQ+tWqNRJsPttyvlgWRVzQgaSxarRf+lGUU63kj3zACfWMwduRHNoEcBHC9EVqfuYTEwDRuU8THspJjjumsnHWg0ywcPv5QfiTous1a29Y82EfsaiDJVTzcRbQ5u541phfSG62Mp8HtkGQrQvTKmjXoShk9PnTVHN98pauv6hF3LOuSNPKc2TTwQ5/BpKOSsNtw5LeyqKZo09tQxiUPG6ue8ZxMD7cXcy6Pz5XXk4gvO1x4uamohtRE99m9Sf2QOaLpPcl2H7p15+YFpz9hzC97ZxUuAVBT9ruBMaoPH78isfkyNX5/Z/1hvw6NiTaBoOy2bplA9tV9DzLEGkEvXz6fsIs2hdHDcRGJLUMKCeuOvBZca+Su6gvGr95inkJrZTE/CjDQetp3/JMC1vFHK7l5ThEXnlrJE6S94XDiSU+KmD3dmybQh0iqpaneyVMCn6muHd4oXOpiZWdu4iOOkDMeZcUvlcoP83az1u4p4SJWlZ/YDB3FDTCdZsldgoNG2fXI16fSITd8fwcoB5oHeadbdNh3KnPv+X11o7UF9jVCiwnf1sT7d0oB6i2mnhx1vqWuuwaWkcxyjmZP9gLrljm4vBYit0AUWBrSjS1EJD0Khzqs5inyjyB/1QOd/WbC7mpYrFnHE6rXPPMD3l9SwTiCNzlU/bBOBB8cPpP1v9Bc4zPAfwO2thMchfulRnj/2jF2M6kj4jhOnTDVokaz9KTpXITinmaZWIWQkkgztiNmPcU3SudiLnatCxV07BiOhQqbHi5eo/rwZMQ"
    auth_token = quote(accessToken, safe='')
    candidateId = "00a0e7b0-7f7d-11f0-8589-2f61f62a73e4"
    set_application_data(applicationId, jobId, scheduleId)
    ws = websocket.WebSocketApp(getSocketUrl(applicationId, candidateId, auth_token),
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close)
    ws.run_forever()

connect("b385546a-1258-43a5-bf8e-f9416dfcdcf3", "JOB-CA-0000000373", "SCH-CA-0000004498")