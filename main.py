from config_reader import ConfigReader
from pseudo_random_numbers import PseudoRandomNumbers
from queue_system import QueueSystem
from simulation import Simulation
from stats import Stats
from event import Event, EventType

def main():
    # 1. Ler o YAML de configuração
    config = ConfigReader('config.yml')

    # 2. Criar gerador de números aleatórios
    qtd_aleatorios, seeds = config.get_random_numbers()
    prng = PseudoRandomNumbers(seeds[0]) 

    # 3. Criar filas (QueueSystem)
    sistemas = {}
    for nome, dados in config.get_queues().items():
        servidores = dados['servers']
        capacidade = dados.get('capacity', float('inf'))
        intervalo_chegada = (dados.get('minArrival', 0), dados.get('maxArrival', 0))
        intervalo_servico = (dados['minService'], dados['maxService'])
        
        fila = QueueSystem(capacidade, servidores, intervalo_chegada, intervalo_servico, prng)
        sistemas[nome] = fila

   # 4. Definir para onde os clientes vão após o serviço
    for link in config.get_network():
        origem = link['source']
        destino = link['target']
        probabilidade = link['probability']
        
        if destino == "exit":
            destino = None
        
        sistemas[origem].destinos[destino] = probabilidade

    # 5. Criar simulação
    sim = Simulation(prng=prng, max_randoms=qtd_aleatorios)

    # Adicionar os sistemas na simulação
    for nome, sistema in sistemas.items():
        sim.adicionar_sistema(nome, sistema)

    # 6. Agendar primeiras chegadas
    for nome, arrival_time in config.get_arrivals().items():
        evento = Event(
            tipo=EventType.ARRIVE,
            tempo=arrival_time,   
            origem=None,
            destino=nome
        )
        sim.scheduler.adicionar_evento(evento)

    # 7. Rodar a simulação
    sim.run()

    # 8. Mostrar estatísticas
    Stats(sim.sistemas, sim.tempo_atual).imprimir_relatorio()

if __name__ == "__main__":
    main()
