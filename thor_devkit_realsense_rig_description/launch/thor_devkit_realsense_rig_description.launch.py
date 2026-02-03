# SPDX-FileCopyrightText: NVIDIA CORPORATION & AFFILIATES
# Copyright (c) 2025 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0
import isaac_ros_launch_utils as lu
from launch import LaunchDescription


def generate_launch_description() -> LaunchDescription:
    args = lu.ArgumentContainer()
    args.add_arg('urdf_override_file', default='None', cli=True)
    args.add_arg('calibrated_urdf_file', default='None')
    args.add_arg('camera_model', default='d455',
                 description='RealSense model for determining nominals calibration file',
                 choices=['d435', 'd455'], cli=True)
    actions = args.get_launch_actions()

    nominals_file = lu.if_else_substitution(
        lu.is_equal(args.camera_model, 'd435'),
        'urdf/thor_devkit_realsense_rig_d435.urdf.xacro',
        'urdf/thor_devkit_realsense_rig_d455.urdf.xacro')

    actions.append(lu.log_info(f'Using nominals file: {nominals_file}'
                               f'given camera model: {args.camera_model}'))
    actions.append(
        lu.add_robot_description(nominals_package='thor_devkit_realsense_rig_description',
                                 nominals_file=nominals_file,
                                 override_path=args.urdf_override_file,
                                 robot_calibration_path=args.calibrated_urdf_file))

    return LaunchDescription(actions)
