from src.task import Task

class Scheduler:
    def __init__(self, quant : int = 1):
        self.quant = quant

    def schedule(self, batch):
        steps = 0
        while batch.cycle(self.quant) > 0:
            pass
        print('Finished executing!\nStats:')
        for task in batch.profile:
            print('task', task, ' :', batch.profile[task])
    
