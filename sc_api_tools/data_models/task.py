from typing import List, Optional, ClassVar

import attr

from sc_api_tools.data_models import TaskType
from sc_api_tools.data_models.label import Label
from sc_api_tools.data_models.utils import deidentify, str_to_task_type


@attr.s(auto_attribs=True)
class Task:
    """
    Class representing a Task in SC

    :var title: Title of the task
    :var task_type: Type of the task
    :var labels: List of labels belonging to the task
    :var id: unique database ID of the task
    :var label_schema_id: unique database ID of the label schema for the task
    """
    _identifier_fields: ClassVar[List[str]] = ["id", "label_schema_id"]

    title: str
    task_type: str = attr.ib(converter=str_to_task_type)
    labels: Optional[List[Label]] = None
    label_schema_id: Optional[str] = None
    id: Optional[str] = None

    @property
    def type(self) -> TaskType:
        """
        Returns the type of the task.

        This property is here to make sure that the type of task_type is derived
        correctly. The attribute self.task_type can be instantiated both as a string
        and as a TaskType

        :return: type of the task
        """
        task_type = self.task_type
        if not isinstance(task_type, TaskType):
            task_type = TaskType(task_type)
        return task_type

    @property
    def is_trainable(self):
        """
        Returns True if this Task represents a trainable task

        :return: True if the task is trainable, False otherwise
        """
        return self.type.is_trainable

    def deidentify(self):
        deidentify(self)
        if self.is_trainable:
            for label in self.labels:
                deidentify(label)

    @property
    def label_names(self) -> List[str]:
        """
        Returns a list of label names for the task

        :return:
        """
        return [label.name for label in self.labels]
