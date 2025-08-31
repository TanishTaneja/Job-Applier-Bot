import requests
import json
from data import get_data

def make_request(jobId, scheduleId):
    cookies = get_data().get("cookies")
    accessToken = get_data().get("accessToken")
    candidateId = get_data().get("candidateId")
    url = "https://hiring.amazon.ca/application/api/candidate-application/ds/create-application"
    
    try:
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-CA,en;q=0.9,en-IN;q=0.8",
            "authorization": accessToken,
            "bb-ui-version": "bb-ui-v2",
            "content-type": "application/json;charset=UTF-8",
            "origin": "https://hiring.amazon.ca",
            "referer": f"https://hiring.amazon.ca/application/ca/?CS=true&jobId={jobId}&locale=en-CA&scheduleId={scheduleId}&ssoEnabled=1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0",
            "cookie": cookies,
        }
        payload = {
            "jobId": jobId,
            "dspEnabled": True,
            "scheduleId": scheduleId,
            "candidateId": candidateId,
            "activeApplicationCheckEnabled": True
        }
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        print(f"Appilication Response: {response}")
        try:
            if response.status_code == 200:
                res = response.json()
                return res.get('data', {}).get('applicationId')
            return None
        except json.JSONDecodeError:
            return {"error": "Invalid JSON response", "raw_text": response.text}
    except requests.exceptions.Timeout:
        return {"error": "Request timed out"}
    except requests.exceptions.ConnectionError as e:
        return {"error": "Connection failed", "details": str(e)}
    except requests.exceptions.HTTPError as e:
        return {"error": "HTTP error", "status_code": response.status_code, "details": str(e)}
    except Exception as e:
        return {"error": "Unexpected error", "details": str(e)}
    
def update_application(applicationId, jobId, scheduleId):
    cookies = get_data().get("cookies")
    accessToken = get_data().get("accessToken")
    url = "https://hiring.amazon.ca/application/api/candidate-application/update-application"
    
    try:
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-CA,en;q=0.9,en-IN;q=0.8",
            "authorization": accessToken,
            "bb-ui-version": "bb-ui-v2",
            "content-type": "application/json;charset=UTF-8",
            "origin": "https://hiring.amazon.ca",
            "referer": f"https://hiring.amazon.ca/application/ca/?CS=true&jobId={jobId}&locale=en-CA&scheduleId={scheduleId}&ssoEnabled=1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0",
            "cookie": cookies,
        }
        payload = {
            "applicationId": applicationId,
            "payload": {
                "jobId": jobId,
                "scheduleId": scheduleId,
            },
            "dspEnabled": True,
            "type":"job-confirm"
        }
        response = requests.put(url, headers=headers, json=payload, timeout=15)
        try:
            if response.status_code == 200:
                return response.json()
            return None
        except json.JSONDecodeError:
            return {"error": "Invalid JSON response", "raw_text": response.text}
    except requests.exceptions.Timeout:
        return {"error": "Request timed out"}
    except requests.exceptions.ConnectionError as e:
        return {"error": "Connection failed", "details": str(e)}
    except requests.exceptions.HTTPError as e:
        return {"error": "HTTP error", "status_code": response.status_code, "details": str(e)}
    except Exception as e:
        return {"error": "Unexpected error", "details": str(e)}

def update_application_flow(applicationId, jobId, scheduleId):
    cookies = get_data().get("cookies")
    accessToken = get_data().get("accessToken")
    url = "https://hiring.amazon.ca/application/api/candidate-application/update-workflow-step-name"

    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-CA,en;q=0.9,en-IN;q=0.8",
        "authorization": accessToken,
        "bb-ui-version": "bb-ui-v2",
        "content-type": "application/json;charset=UTF-8",
        "origin": "https://hiring.amazon.ca",
        "referer": f"https://hiring.amazon.ca/application/us/?CS=true&jobId={jobId}&locale=en-US&scheduleId={scheduleId}&ssoEnabled=1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0",
        "Cookie": cookies
    }

    payload = {
        "applicationId": applicationId,
        "workflowStepName": "general-questions"
    }

    try:
        response = requests.put(url, headers=headers, json=payload, timeout=20)
        response.raise_for_status()  # raises an error for 4xx/5xx
    except requests.exceptions.RequestException as e:
        print("❌ Error:", e)

    
def init_application(jobId: str, scheduleId: str):
    applicationId = make_request(
        jobId=jobId,
        scheduleId=scheduleId,
    )
    if applicationId != None:
        response = update_application(
            applicationId=applicationId,
            jobId=jobId,
            scheduleId=scheduleId,
        )
        if response and not response.get('error'):
            update_application_flow(
                applicationId=applicationId,
                jobId=jobId,
                scheduleId=scheduleId
            )
        print(f"Response: {response}")