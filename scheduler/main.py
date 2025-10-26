import json
import os
from datetime import datetime
from typing import Dict, List, Tuple

from scheduler.services.search_jobs import get_search_jobs
from scheduler.services.get_job_schedule import get_job_schedule

class Entry:
    def __init__(self, data: str, timestamp: str):
        self.data = data
        self.time = timestamp

    def to_dict(self) -> Dict[str, str]:
        return {"data": self.data, "time": self.time}


def append_to_json_file(filename: str, new_data: str) -> None:
    file_data: Dict[str, List[Dict[str, str]]] = {"data": []}

    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                file_data = json.load(f)
        except Exception:
            pass

    entry = Entry(new_data, datetime.utcnow().isoformat())
    file_data["data"].append(entry.to_dict())

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(file_data, f, indent=2)


def init_jobs() -> Tuple[str, str]:
    jobs = get_search_jobs()
    if not jobs:
        return None, None

    first_job = jobs[0] if isinstance(jobs[0], dict) else None
    if not first_job:
        return None, None

    job_id = first_job.get("jobId")
    state = first_job.get("state")
    employmentType = first_job.get("employmentType")
    if not isinstance(job_id, str):
        return None, None

    schedules = get_job_schedule(job_id)
    if not schedules:
        return None, None

    first_schedule = schedules[0] if isinstance(schedules[0], dict) else None
    if not first_schedule:
        return None, None

    schedule_id = first_schedule.get("scheduleId")
    if not isinstance(schedule_id, str):
        return None, None
    
    job_details = {
        "job_id": job_id,
        "state": state,
        "employmentType": employmentType,
    }

    schedule_details = {
        "schedule_id": schedule_id,
    }
    
    return job_details, schedule_details