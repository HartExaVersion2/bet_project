import requests
from fastapi import FastAPI, HTTPException
from typing import List, Dict
from datetime import datetime
from models import Event, EventStatus, BetStatus, Bet

app = FastAPI()
bets_db: Dict[int, Bet] = {}
LINE_PROVIDER_URL = "http://0.0.0.0:8000"

async def get_actual_events() -> List[Event]:
    actual_evetns = []
    response = requests.get(f"{LINE_PROVIDER_URL}/events")
    response.raise_for_status()
    events_data = response.json()
    for event_data in events_data:
        event = Event(
            event_id=event_data['event_id'],
            bet_coefficient=event_data['bet_coefficient'],
            bet_deadline=datetime.fromisoformat(event_data['bet_deadline']),
            event_status=EventStatus(event_data['event_status'])
        )
        if event.bet_deadline > datetime.now() and 'win' not in event.event_status:
            actual_evetns.append(event)
    return actual_evetns

@app.get("/bets/events", response_model=List[Event])
async def get_events():
    actual_events = get_actual_events()
    return actual_events

@app.post("/bets/bet")
async def place_bet(bet: Bet):
    actual_events_db = get_actual_events()
    if not any(event.event_id == bet.event_id for event in actual_events_db):
        raise HTTPException(status_code=404, detail="Event not found")
    bet_id = str(len(bets_db) + 1)
    bets_db[bet_id] = bet
    return {"bet_id": bet_id}


@app.put("/bets/{event_id}/{new_status}")
async def change_event_status(event_id: str, new_status: EventStatus):
    for bet_id, bet in bets_db.items():
        if bet.event_id == event_id:
            if bet.command == new_status and new_status != 'not completed':
                bet.status = BetStatus.victory
            elif bet.command != new_status and new_status != 'not completed':
                bet.status = BetStatus.defeat
            else:
                bet.status = BetStatus.not_played

@app.get("/bets", response_model=List[Bet])
async def get_bets():
    return list(bets_db.values())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7000)
