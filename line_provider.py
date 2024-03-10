from fastapi import FastAPI, HTTPException
from typing import List
from models import Event, EventStatus
import requests

app = FastAPI()
events_db: List[Event] = []
BOT_MAKER_URL = "http://0.0.0.0:7000"

@app.post("/events/create")
async def create_event(event: Event):
    events_db.append(event)
    return {"message": "Event created successfully"}

@app.get("/events", response_model=List[Event])
async def get_events():
    return events_db

@app.get("/events/{event_id}", response_model=Event)
async def get_event(event_id: str):
    for event in events_db:
        if event.event_id == event_id:
            return event
    raise HTTPException(status_code=404, detail="Event not found")

@app.put("/events/{event_id}/status/{new_status}")
async def change_event_status(event_id: str, new_status: EventStatus):
    for event in events_db:
        if event.event_id == event_id:
            event.event_status = new_status
            requests.put(f"{BOT_MAKER_URL}/bets/{event_id}/{new_status}")
            return {"message": f"Event status changed to {new_status}"}
    raise HTTPException(status_code=404, detail="Event not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)