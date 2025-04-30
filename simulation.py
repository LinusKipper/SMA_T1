from event import Event, EventType
from pseudo_random_numbers import PseudoRandomNumbers
from scheduler import Scheduler
from queue_system import QueueSystem

class Simulation:
    def __init__(self, prng: PseudoRandomNumbers, max_randoms: int):
        self.scheduler = Scheduler()
        self.prng = prng
        self.max_randoms = max_randoms
        self.tempo_atual = 0.0
        self.tempo_anterior = 0.0
        self.sistemas = {}

    def adicionar_sistema(self, nome: str, sistema: QueueSystem):
        self.sistemas[nome] = sistema

    def historico(self):
        # para cada fila, acumula delta_tempo em histórico
        for sistema in self.sistemas.values():
            sistema.atualizar_estatisticas(self.tempo_atual, self.tempo_anterior)

    def run(self):
        # enquanto houver eventos e não tivermos estourado o número de aleatórios
        while self.scheduler.event_queue and self.prng.count < self.max_randoms:
            evento = self.scheduler.pegar_proximo_evento()

            # 1 guarde tempos
            self.tempo_anterior = self.tempo_atual
            self.tempo_atual = evento.tempo

            # 2 atualiza estados de todas filas
            self.historico()

            # 3 dispara o evento
            if evento.tipo == EventType.ARRIVE:
                self.executar_arrival(evento)
            elif evento.tipo == EventType.EXIT:
                self.executar_exit(evento)
            elif evento.tipo == EventType.MOVE:
                self.executar_move(evento)

    def executar_arrival(self, evento: Event):
        sistema = self.sistemas[evento.destino]
        sistema.adicionar_cliente()

        # Se esse sistema gera chegadas (só Q1 terá intervalo_chegada != (0,0))
        if sistema.intervalo_chegada != (0, 0):
            t_chec = sistema.pseudo_random_numbers.uniform(*sistema.intervalo_chegada)
            e_arr = Event(
                tipo=EventType.ARRIVE,
                tempo=self.tempo_atual + t_chec,
                origem=None,
                destino=evento.destino
            )
            self.scheduler.adicionar_evento(e_arr)

        # Se ocupou um servidor, agende o serviço desse mesmo cliente
        if sistema.status <= sistema.num_servidores:
            t_srv = sistema.pseudo_random_numbers.uniform(*sistema.intervalo_servico)
            e_srv = Event(
                tipo=EventType.EXIT,
                tempo=self.tempo_atual + t_srv,
                origem=evento.destino
            )
            self.scheduler.adicionar_evento(e_srv)

    def executar_exit(self, evento: Event):
        sistema = self.sistemas[evento.origem]
        # 1) cliente sai
        sistema.remover_cliente()

        # 2) Roteia o cliente que acabou de sair
        destino = sistema.escolher_destino()
        if destino is not None:
            e_move = Event(
                tipo=EventType.MOVE,
                tempo=self.tempo_atual,
                origem=evento.origem,
                destino=destino
            )
            self.scheduler.adicionar_evento(e_move)

        # 3) SE ainda havia gente esperando, agende
        #    o próximo serviço para a fila origem
        if sistema.status >= sistema.num_servidores:
            # sorteia novo tempo de serviço
            t_serv = sistema.pseudo_random_numbers.uniform(*sistema.intervalo_servico)
            e_next = Event(
                tipo=EventType.EXIT,
                tempo=self.tempo_atual + t_serv,
                origem=evento.origem
            )
            self.scheduler.adicionar_evento(e_next)

    def executar_move(self, evento: Event):
        s = self.sistemas[evento.destino]
        s.adicionar_cliente()
        if s.status <= s.num_servidores:
            atendimento = s.pseudo_random_numbers.uniform(*s.intervalo_servico)
            e = Event(EventType.EXIT, self.tempo_atual + atendimento, origem=evento.destino)
            self.scheduler.adicionar_evento(e)
