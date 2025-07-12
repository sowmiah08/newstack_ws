from setuptools import find_packages, setup

package_name = 'stacker_bot'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/simple.launch.py' , 'launch/gz_world.launch.py' , 'launch/spawn_robot.launch.py', 'launch/bringup.launch.py']),
        ('share/' + package_name + '/worlds', ['worlds/gz_world.world']),
        ('share/' + package_name + '/config', ['config/franka_controllers.yaml']),
    ],
    install_requires=['setuptools'],    
    zip_safe=True,
    maintainer='zozo',
    maintainer_email='snknitheesh@gmail.com',
    description='TODO: Package description',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'simple_node = stacker_bot.simple_node:main',
        ],
    },
)
