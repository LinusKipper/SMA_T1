from enum import Enum

class EventType(Enum):
    ARRIVE = "ARRIVE"
    EXIT = "EXIT"
    MOVE = "MOVE"

class Event:
    def __init__(self, tipo: EventType, tempo: float, origem: str = None, destino: str = None):
        self.tipo = tipo
        self.tempo = tempo
        self.origem = origem
        self.destino = destino

    def __repr__(self):
        return (f"Event(tipo={self.tipo}, tempo={self.tempo}, "
                f"origem={self.origem}, destino={self.destino})")
