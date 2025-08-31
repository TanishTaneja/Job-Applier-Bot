data = dict()

def set_data(cookies: str, accessToken: str, candidateId: str):
    data["cookies"] = cookies
    data["accessToken"] = accessToken
    data["candidateId"] = candidateId

def get_data() -> dict:
    return data