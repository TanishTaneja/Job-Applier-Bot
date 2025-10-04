data = dict()

def set_data(cookies: str, accessToken: str, candidateId: str, sessionToken: str):
    data["cookies"] = cookies
    data["accessToken"] = accessToken
    data["candidateId"] = candidateId
    data["sessionToken"] = sessionToken

def set_application_data(applicationId: str, jobId: str, scheduleId: str):
    data["applicationId"] = applicationId
    data["jobId"] = jobId
    data["scheduleId"] = scheduleId
    
def get_data() -> dict:
    return data