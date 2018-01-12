# -*- coding: utf-8 -*-

import os


isTest = os.environ.get("TEST", "test")

if isTest == "online":
    print('Use online config')
    from .online import configs, log_config
else:
    print('Use test config')
    from .test import configs, log_config


__all__ = [configs, log_config]
