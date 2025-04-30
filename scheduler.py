import heapq
from event import Event

class Scheduler:
    def __init__(self):
        self.event_queue = []

    def adicionar_evento(self, evento: Event):
        heapq.heappush(self.event_queue, (evento.tempo, evento))

    def pegar_proximo_evento(self) -> Event:
        if self.event_queue:
            _, evento = heapq.heappop(self.event_queue)
            return evento
        return None  # Se não houver eventos
