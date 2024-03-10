from enum import Enum
from pydantic import BaseModel
from datetime import datetime

# Модель для данных о событиях
class EventStatus(str, Enum):
    not_completed = "not completed"
    win1 = "win1"
    win2 = "win2"

# Модель данных для события
class Event(BaseModel):
    event_id: str
    bet_coefficient: float
    bet_deadline: datetime
    event_status: EventStatus

# Определение перечисления для статуса события
class BetStatus(str, Enum):
    victory = "victory"
    defeat = "defeat"
    not_played = "not played"

class BetCommand(str, Enum):
    victory = "win1"
    defeat = "win2"

class Bet(BaseModel):
    event_id: str
    amount: float
    command: BetCommand
    status: BetStatus