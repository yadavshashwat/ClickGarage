#!/usr/bin/env python
import os
import sys
paths = ['/Users/shashwatyadav/Desktop/Coding/ClickGarage/','/Users/shashwatyadav/Desktop/Coding/ClickGarage/clickgarage']
for path in paths:
    sys.path.append(path)

import socket
if __name__ == "__main__":


    # print 'paths'
    # print '\n'.join(sys.path)
    if '.local' in socket.gethostname():
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "clickgarage.settings")


    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
