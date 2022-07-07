# Copyright (C) 2022 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions
# and limitations under the License.

import os
from abc import abstractmethod
from glob import glob
from typing import List, Union, Dict, Optional

from sc_api_tools.data_models.enums import TaskType
from sc_api_tools.data_models.annotations import Annotation


class AnnotationReader:
    """
    Base class for annotation reading, to handle loading and converting annotations
    to Sonoma Creek format
    """

    def __init__(
            self,
            base_data_folder: str,
            annotation_format: str = ".json",
            task_type: Union[TaskType, str] = TaskType.DETECTION
    ):
        if task_type is not None and not isinstance(task_type, TaskType):
            task_type = TaskType(task_type)
        self.base_folder = base_data_folder
        self.annotation_format = annotation_format
        self.task_type = task_type

    @abstractmethod
    def get_data(
            self, filename: str,
            label_name_to_id_mapping: dict,
            preserve_shape_for_global_labels: bool = False
    ) -> List[Annotation]:
        """
        Get annotation data for a certain filename
        """
        raise NotImplementedError

    def get_data_filenames(self) -> List[str]:
        """
        Returns a list of annotation files found in the `base_data_folder`

        :return: List of filenames (excluding extension) for all annotation files in
            the data folder
        """
        filepaths = glob(
            os.path.join(self.base_folder, f'*{self.annotation_format}')
        )
        return [
            os.path.splitext(os.path.basename(filepath))[0]
            for filepath in filepaths
        ]

    @abstractmethod
    def get_all_label_names(self) -> List[str]:
        """
        Returns a list of unique label names that were found in the annotation data
        folder belonging to this AnnotationReader instance

        :return:
        """
        raise NotImplementedError

    def prepare_and_set_dataset(
            self,
            task_type: Union[TaskType, str],
            previous_task_type: Optional[TaskType] = None
    ):
        """
        Prepares a dataset for uploading annotations for a certain task_type

        :param task_type: TaskType to prepare the dataset for
        :param previous_task_type: Optional type of the (trainable) task preceding
            the current task in the pipeline. This is only used for global tasks

        :return:
        """
        if not isinstance(task_type, TaskType):
            task_type = TaskType(task_type)
        if task_type in [
            TaskType.DETECTION, TaskType.SEGMENTATION, TaskType.CLASSIFICATION
        ]:
            self.task_type = task_type
        else:
            raise ValueError(f"Unsupported task_type {task_type}")

    @property
    def applied_filters(self) -> List[Dict[str, Union[List[str], str]]]:
        """
        Returns a list of dictionaries representing the filter settings that have
        been applied to the dataset, if any.

        Dictionaries in this list contain two keys:
        - 'labels'      -- List of label names which has been filtered on
        - 'criterion'   -- String representing the criterion that has been used in the
                           filtering. Can be 'OR', 'AND', 'XOR' or 'NOT'.

        :return: List of filter settings that have been applied to the dataset. Returns
            an empty list if no filters have been applied.
        """
        return []