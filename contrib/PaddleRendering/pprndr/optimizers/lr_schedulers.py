#  Copyright (c) 2023 PaddlePaddle Authors. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License")
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import math

from paddle.optimizer.lr import LambdaDecay

from pprndr.apis import manager

__all__ = ["CustomExponentialDecay"]


@manager.LR_SCHEDULERS.add_component
class CustomExponentialDecay(LambdaDecay):
    """Exponential learning rate decay function.
        Refer to https://github.com/google-research/google-research/blob/fd2cea8cdd86b3ed2c640cbe5561707639e682f3/jaxnerf/nerf/utils.py#L360
        for details.

        Args:
            lr_init: The initial learning rate.
            lr_final: The final learning rate.
            max_steps: The maximum number of steps.
            lr_delay_steps: The number of steps to delay the learning rate.
            lr_delay_mult: The multiplier for the learning rate after the delay.
    """

    def __init__(self,
                 lr_init,
                 lr_final,
                 max_steps,
                 lr_delay_steps=0,
                 lr_delay_mult=1.0):
        def lr_lambda(step):
            if lr_delay_steps > 0:
                delay_rate = lr_delay_mult + (1 - lr_delay_mult) * math.sin(
                    0.5 * math.pi * max(min(step / lr_delay_steps, 1), 0))
            else:
                delay_rate = 1.0
            t = max(min(step / max_steps, 1), 0)
            log_lerp = math.exp(
                math.log(lr_init) * (1 - t) + math.log(lr_final) * t)
            multiplier = (
                log_lerp / lr_init
            )  # divided by lr_init because the multiplier is with the initial learning rate
            return delay_rate * multiplier

        super(CustomExponentialDecay, self).__init__(
            lr_init, lr_lambda=lr_lambda)
