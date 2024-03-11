# Copyright (C) 2024 Intel Corporation
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
import logging
from typing import Optional, Union

import cv2
import numpy as np

from geti_sdk.data_models import Dataset, Prediction, Project
from geti_sdk.deployment.inference_hook_interfaces import PostInferenceAction
from geti_sdk.http_session import GetiSession
from geti_sdk.rest_clients.dataset_client import DatasetClient
from geti_sdk.rest_clients.media_client.image_client import ImageClient
from geti_sdk.rest_clients.project_client.project_client import ProjectClient


class GetiDataCollection(PostInferenceAction):
    """
    Post inference action that will send an image to a specified `project` and `dataset`
    on the Intel® Geti™ server addressed by `session`.

    :param session: Geti session representing the connecting to the Intel® Geti™ server
    :param workspace_id: unique ID of the workspace in which the project to collect
        the data resides.
    :param project: Project or name of the project to whicht the image data should be
        transferred.
    :param dataset: Optional Dataset or name of the dataset in which to store the
        image data. If not specified, the default training dataset of the project is
        used
    """

    def __init__(
        self,
        session: GetiSession,
        workspace_id: str,
        project: Union[str, Project],
        dataset: Optional[Union[str, Dataset]] = None,
    ):
        project_client = ProjectClient(session=session, workspace_id=workspace_id)
        if isinstance(project, str):
            project_name = project
            project = project_client.get_project_by_name(project_name=project_name)
            if project is None:
                raise ValueError(
                    f"Project `{project_name}` does not exist on the Intel® Geti™ "
                    f"server, unable to initialize the Intel® Geti™ data collection "
                    f"action"
                )
        dataset_client = DatasetClient(
            session=session, workspace_id=workspace_id, project=project
        )
        if dataset is None:
            datasets = dataset_client.get_all_datasets()
            dataset = [ds for ds in datasets if ds.use_for_training][0]
        elif isinstance(dataset, str):
            dataset_name = dataset

            try:
                dataset = dataset_client.get_dataset_by_name(dataset_name)
            except ValueError:
                dataset = dataset_client.create_dataset(dataset_name)
                logging.info(
                    f"Dataset `{dataset_name}` was created in project `{project.name}`"
                )
        self.image_client = ImageClient(
            session=session, workspace_id=workspace_id, project=project
        )
        self.dataset = dataset
        self.__repr_info = (
            f"target_server=`{session.config.host}`, "
            f"target_project={project.name}, "
            f"target_dataset={dataset.name}"
        )

    def __call__(
        self, image: np.ndarray, prediction: Prediction, score: Optional[float] = None
    ):
        """
        Execute the action, upload the given `image` to the Intel® Geti™ server.

        The parameters `prediction` and `score` are not used in this specific action.

        :param image: Numpy array representing an image
        :param prediction: Prediction object which was generated for the image
        :param score: Optional score computed from a post inference trigger
        """
        image_bgr = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # upload_image uses cv2 to encode the numpy array as image, so it expects an
        # image in BGR format. However, `Deployment.infer` requires RGB format, so
        # we have to convert
        self.image_client.upload_image(image=image_bgr, dataset=self.dataset)
        logging.info(
            f"GetiDataCollection inference action uploaded image to dataset "
            f"`{self.dataset.name}`"
        )

    def __repr__(self):
        """
        Return a string representation of the GetiDataCollection action object
        """
        return f"PostInferenceAction `GetiDataCollection`({self.__repr_info})"
