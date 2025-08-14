import logging
from abc import ABC, abstractmethod

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Task:
    def __init__(self, name):
        self.name = name
        self.completed = False

    def __repr__(self):
        status = "Completed" if self.completed else "Pending"
        return f"Task(name='{self.name}', status='{status}')"

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass

class CreateTaskCommand(Command):
    def __init__(self, task_list, task_name):
        self.task_list = task_list
        self.task_name = task_name
        self.task = None

    def execute(self):
        self.task = Task(self.task_name)
        self.task_list.append(self.task)

    def undo(self):
        if self.task in self.task_list:
            self.task_list.remove(self.task)

class CompleteTaskCommand(Command):
    def __init__(self, task):
        self.task = task
        self.previous_status = task.completed

    def execute(self):
        self.task.completed = True

    def undo(self):
        self.task.completed = self.previous_status

class DeleteTaskCommand(Command):
    def __init__(self, task_list, task):
        self.task_list = task_list
        self.task = task
        self.index = None

    def execute(self):
        if self.task in self.task_list:
            self.index = self.task_list.index(self.task)
            self.task_list.remove(self.task)

    def undo(self):
        if self.index is not None:
            self.task_list.insert(self.index, self.task)

class TaskManager:
    def __init__(self):
        self.task_list = []
        self.history = []

    def execute_command(self, command):
        command.execute()
        self.history.append(command)

    def undo_last_command(self):
        if self.history:
            command = self.history.pop()
            command.undo()
            return True
        return False

if __name__ == "__main__":
    manager = TaskManager()

    create1 = CreateTaskCommand(manager.task_list, "Write a report")
    manager.execute_command(create1)
    
    create2 = CreateTaskCommand(manager.task_list, "Prepare presentation")
    manager.execute_command(create2)

    task_to_complete = manager.task_list[0]
    complete1 = CompleteTaskCommand(task_to_complete)
    manager.execute_command(complete1)

    logger.info("Current tasks:")
    for task in manager.task_list:
        logger.info(task)

    manager.undo_last_command()
    logger.info("\nAfter undoing complete task:")
    for task in manager.task_list:
        logger.info(task)
    
    delete1 = DeleteTaskCommand(manager.task_list, manager.task_list[0])
    manager.execute_command(delete1)

    logger.info("\nAfter deleting first task:")
    for task in manager.task_list:
        logger.info(task)

    manager.undo_last_command()
    logger.info("\nAfter undoing delete task:")
    for task in manager.task_list:
        logger.info(task)