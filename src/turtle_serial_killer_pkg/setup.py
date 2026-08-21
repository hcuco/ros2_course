from setuptools import find_packages, setup

package_name = 'turtle_serial_killer_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='labra',
    maintainer_email='henriquecuco04@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            "turtle_spawner = turtle_serial_killer_pkg.turtle_spawner:main",
            "tsk_controller = turtle_serial_killer_pkg.tsk_controller:main"
        ],
    },
)
