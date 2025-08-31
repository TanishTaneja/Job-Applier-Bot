from typing import List

EVENTS=list()

def get_events():
    TEMP_EVENTS = []
    TEMP_EVENTS.extend(EVENTS)
    return TEMP_EVENTS

def set_events(urls:List[dict]):
    for url in urls:
        is_new = True
        for event in EVENTS:
            if event["url"] == url["url"]:
                is_new = False
                break
        if is_new:
            EVENTS.append(url)

def clear_events():
    EVENTS.clear()

def remove_event(index=0):
    if(len(EVENTS) > 0):
        EVENTS.pop(index)