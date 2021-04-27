from src.schedule import Scheduler
from src.task import Task, Batch


timings = [
    [4, 0],         ## execution time, arrival time
    [3, 0],
    [5, 0],
    [3,2]
]
batch = Batch.from_timings(timings)

sched = Scheduler(quant=2)
sched.schedule(batch)
