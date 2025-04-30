import yaml

class ConfigReader:
    def __init__(self, filepath: str):
        with open(filepath, 'r') as file:
            self.config = yaml.safe_load(file)

    def get_arrivals(self):
        return self.config.get('arrivals', {})

    def get_queues(self):
        return self.config.get('queues', {})

    def get_network(self):
        return self.config.get('network', [])
    
    def get_random_numbers(self):
        return self.config.get('rndnumbersPerSeed', 0), self.config.get('seeds', [])

