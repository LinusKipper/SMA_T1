class QueueSystem:
    def __init__(self, capacidade: int, num_servidores: int, intervalo_chegada: tuple, intervalo_servico: tuple, prng):
        self.capacidade = capacidade
        self.num_servidores = num_servidores
        self.intervalo_chegada = intervalo_chegada  # Ex: (min, max)
        self.intervalo_servico = intervalo_servico  # Ex: (min, max)
        self.status = 0
        self.perdas = 0
        self.historico_estados = {}  # chave: número de clientes, valor: tempo acumulado
        self.destinos = {}  # destinos possíveis e suas probabilidades
        self.pseudo_random_numbers = prng

    def adicionar_cliente(self):
        if self.status < self.capacidade:
            self.status += 1
        else:
            self.perdas += 1

    def remover_cliente(self):
        if self.status > 0:
            self.status -= 1

    def atualizar_estatisticas(self, tempo_atual: float, tempo_anterior: float):
        delta_tempo = tempo_atual - tempo_anterior
        if self.status in self.historico_estados:
            self.historico_estados[self.status] += delta_tempo
        else:
            self.historico_estados[self.status] = delta_tempo

    def definir_destino(self, destinos: dict):
        self.destinos = destinos

    def escolher_destino(self):
        r = self.pseudo_random_numbers.next()
        acumulado = 0.0
        for destino, prob in self.destinos.items():
            acumulado += prob
            if r <= acumulado:
                return destino
        return None 
    
