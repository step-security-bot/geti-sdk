from enum import Enum

from sc_api_tools.data_models.enums.task_type import TaskType


class Domain(Enum):
    """
    This enum represents the different domains in SC
    """
    DETECTION = "DETECTION"
    SEGMENTATION = "SEGMENTATION"
    CLASSIFICATION = "CLASSIFICATION"
    ANOMALY_CLASSIFICATION = "ANOMALY_CLASSIFICATION"
    ANOMALY_DETECTION = "ANOMALY_DETECTION"
    ANOMALY_SEGMENTATION = "ANOMALY_SEGMENTATION"
    INSTANCE_SEGMENTATION = "INSTANCE_SEGMENTATION"
    ROTATED_DETECTION = "ROTATED_DETECTION"

    def __str__(self) -> str:
        """
        Returns the string representation of the Domain instance

        :return: string containing the domain
        """
        return self.value

    @classmethod
    def from_task_type(cls, task_type: TaskType) -> 'Domain':
        """
        Returns the Domain corresponding to a certain task type

        :param task_type: TaskType to retrieve the domain for
        :return:
        """
        return cls[task_type.name]
