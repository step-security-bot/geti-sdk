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

from enum import Enum


class ConfigurationEntityType(Enum):
    HYPER_PARAMETER_GROUP = 'HYPER_PARAMETER_GROUP'
    COMPONENT_PARAMETERS = 'COMPONENT_PARAMETERS'

    def __str__(self):
        """
        Returns the string representation of the ConfigurationEntityType instance
        :return:
        """
        return self.value


class ParameterDataType(Enum):
    BOOLEAN = 'boolean'
    FLOAT = 'float'
    STRING = 'string'
    INTEGER = 'integer'

    def __str__(self):
        """
        Returns the string representation of the ParameterDataType instance
        :return:
        """
        return self.value


class ParameterInputType(Enum):
    INPUT = 'input'
    SELECTABLE = 'selectable'

    def __str__(self):
        """
        Returns the string representation of the ParameterInputType instance
        :return:
        """
        return self.value


class ConfigurableParameterType(Enum):
    CONFIGURABLE_PARAMETERS = 'CONFIGURABLE_PARAMETERS'
    PARAMETER_GROUP = 'PARAMETER_GROUP'

    def __str__(self):
        """
        Returns the string representation of the ConfigurableParameterType instance
        :return:
        """
        return self.value