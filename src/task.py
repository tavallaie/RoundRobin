from typing import List

class Task:
    def __init__(self, id=0, ex_time=1, ar_time=0):
        self.id = id
        self.ex_time = ex_time    ## execution time
        self.ar_time = ar_time    ## arrival time  
        self.r_time = ex_time    ## remaining execution time
        self.prev_time = 0      ## previous time task was executed
        self.wait_time = 0      ## total time task was waiting

    def execute(self, quant, cur_time):
        delta = min(quant, self.r_time)
        if delta > 0:
            self.wait_time += cur_time - self.prev_time
            self.prev_time = cur_time + delta
        self.r_time -= delta
        return delta

    def stats(self):
        return {
            'execution_time': self.ex_time,
            'arrival_time': self.ar_time,
            'total_waiting_time': self.wait_time,
            'remaining_time' : self.r_time
        }


class Batch:

    def __init__(self, tasks: List[Task] = None):
        self._task_queue = sorted(tasks, key=lambda x: (x.ar_time, x.id))
        self._active_tasks = []
        self.profile = dict()
        self.time = 0
        self.curr_idx = 0

    @staticmethod
    def from_timings(timings : List):
        tasks = []
        for i, time in enumerate(timings):
            tasks += [Task(i, time[0], time[1])]
        tasks = sorted(tasks, key=lambda x: (x.ar_time, x.id))
        return Batch(tasks)

    def check_arrivals(self, time):
        drop = []
        for task in self._task_queue:
            if task.ar_time <= time:
                self._active_tasks += [task]
                drop += [task]
            else:
                break
        for task in drop:
            self._task_queue.remove(task)


    def add_task(self, task : Task):
        self._task_queue = sorted(self._task_queue + [task], key=lambda x: (x.ar_time, x.id))

    def cycle(self, quant):
        self.check_arrivals(self.time)
        total = 0
        while total < quant:
            step = quant - total
            task = self._active_tasks[self.curr_idx]
            delta = task.execute(step, self.time)
            print("time: " + str(self.time))
            print(str(task.id) +"  " + str(task.stats()))
            if delta == 0:
                self.profile[task.id] = task.stats()
                self._active_tasks.remove(task)
                self.curr_idx -= 1

            total += delta
            self.time += delta
            self.curr_idx += 1
            if self.curr_idx >= len(self._active_tasks):
                self.curr_idx = 0
            if len(self._active_tasks) == 0:
                return 0
        return len(self._active_tasks)