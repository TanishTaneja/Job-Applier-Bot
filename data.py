from typing import Optional
data = dict()

def set_data(cookies: str, accessToken: str, candidateId: str, sessionToken: str):
    data["cookies"] = cookies
    data["accessToken"] = accessToken
    data["candidateId"] = candidateId
    data["sessionToken"] = sessionToken

def set_application_data(applicationId: str, jobId: str, scheduleId: str, state: Optional[str], employmentType: Optional[str]):
    data["applicationId"] = applicationId
    data["jobId"] = jobId
    data["scheduleId"] = scheduleId
    data["state"] = state
    data["employmentType"] = employmentType
    
def get_data() -> dict:
    return data