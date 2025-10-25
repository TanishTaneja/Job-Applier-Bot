import json
import re
import pandas as pd

# Load your exported file
with open("result.json", "r", encoding="utf-8") as f:
    data = json.load(f)

messages = data["messages"]

job_entries = []
for msg in messages:
    if msg["type"] != "message" or not isinstance(msg.get("text"), list):
        continue
    
    text_content = "".join([t["text"] if isinstance(t, dict) else t for t in msg["text"]])
    
    # Extract fields
    location = re.findall(r"📍 (.*?)\n", text_content)
    role = re.findall(r"🦺 (.*?)\n", text_content)
    job_type = re.findall(r"🗓 (.*?)\n", text_content)
    schedule_count = re.findall(r"🕒 Schedule Count: (\d+)", text_content)
    link = re.findall(r"https://[^\s]+", text_content)
    
    for i in range(len(location)):
        job_entries.append({
            "date": msg["date"],
            "location": location[i],
            "role": role[i] if i < len(role) else None,
            "type_time": job_type[i] if i < len(job_type) else None,
            "schedule_count": int(schedule_count[i]) if i < len(schedule_count) else None,
            "link": link[i] if i < len(link) else None
        })

df = pd.DataFrame(job_entries)
df["date"] = pd.to_datetime(df["date"])
df.to_csv("cleaned_jobs.csv", index=False)
print(df.head())
