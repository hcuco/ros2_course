import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/labra/cuco_ros2_ws/src/install/my_py_pkg'
