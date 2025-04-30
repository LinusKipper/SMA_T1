class Stats:
    def __init__(self, sistemas: dict, tempo_total: float):
        self.sistemas = sistemas
        self.tempo_total = tempo_total

    def calcular_distribuicao(self, sistema_nome: str):
        sistema = self.sistemas[sistema_nome]
        distribuicao = {}
        for estado, tempo in sistema.historico_estados.items():
            distribuicao[estado] = tempo / self.tempo_total
        return distribuicao

    def imprimir_relatorio(self):
        print("-" * 68)

        for nome, sistema in self.sistemas.items():
            # Cabeçalho da fila
            descricao = f"{nome} (G/G/{sistema.num_servidores}"
            if sistema.capacidade == float('inf'):
                descricao += "/∞)"
            else:
                descricao += f"/{sistema.capacidade})"

            print(f"Queue:   {descricao}")
            
            # Intervalo de chegada (se existir)
            if sistema.intervalo_chegada != (0, 0):
                print(f"Arrival: {sistema.intervalo_chegada[0]} ... {sistema.intervalo_chegada[1]}")

            # Intervalo de serviço
            print(f"Service: {sistema.intervalo_servico[0]} ... {sistema.intervalo_servico[1]}")
            print("-" * 68)

            # Tabela de estados
            print(f"{'State':<15}{'Time':<20}{'Probability'}")
            distribuicao = self.calcular_distribuicao(nome)
            for estado in sorted(distribuicao.keys()):
                tempo_estado = self.sistemas[nome].historico_estados.get(estado, 0.0)
                probabilidade = distribuicao[estado] * 100
                print(f"{estado:<15}{tempo_estado:<20.4f}{probabilidade:.2f}%")

            # Perdas
            print(f"Number of losses: {sistema.perdas}")
            print("-" * 68)

        # Mostrar tempo médio da simulação no final
        print(f"Simulation average time: {self.tempo_total:.15f}")
        total_losses = sum(sistema.perdas for sistema in self.sistemas.values())
        print(f"Total number of losses in the system: {total_losses}")

