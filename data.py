data = dict()

def set_data(cookies: str, accessToken: str, candidateId: str, sessionToken: str):
    data["cookies"] = cookies
    data["accessToken"] = accessToken
    data["candidateId"] = candidateId
    data["sessionToken"] = sessionToken
    
def get_data() -> dict:
    return data