import logging

class Executor:
    def __init__(self, task_queue):
        self.task_queue = task_queue
        self.logger = logging.getLogger(__name__)

    def execute(self):
        while not self.task_queue.empty():
            task = self.task_queue.get()
            try:
                self.logger.info(f"Executing task: {task}")
                task.run()
                self.logger.info(f"Task completed: {task}")
            except Exception as e:
                self.logger.error(f"Error executing task {task}: {e}")
            finally:
                self.task_queue.task_done()