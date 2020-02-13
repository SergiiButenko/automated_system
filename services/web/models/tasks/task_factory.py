from .irrigation_task import IrrigationTask

class _TaskFactory():
    def __init__(self):
        self._creators = {}

    def register_task(self, task, creator):
        self._creators[task] = creator

    def get_serializer(self, task):
        creator = self._creators.get(task)
        if not creator:
            raise ValueError(task)
        return creator()

TaskFactory = _TaskFactory()
TaskFactory.register_task('irrigation', IrrigationTask)
