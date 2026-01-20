from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'image_processing'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'msg'), glob('msg/*.msg')), # message files
    ],
    install_requires=['setuptools', 'image_processing_msgs', 'opencv-python-headless<4.9', 'torch', 'torchvision', 'torchaudio', 'numpy<2'],
    zip_safe=True,
    maintainer='cjabrantes',
    maintainer_email='cjabrantes@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': ['image_subscriber = image_processing.image_subscriber:main',
                            'image_labeler = image_processing.image_labeler:main',
                            'yolo_subscriber = image_processing.yolo_subscriber:main',
                            'yolov11_subscriber = image_processing.yolov11_subscriber:main',
                            'behavior_controller = image_processing.behavior_controller:main',
                            'drone_pose_publisher = image_processing.drone_pose_publisher:main',
                            'drone_behavior_node = image_processing.drone_behavior_node:main',
                            'distance_predictor_xyz = image_processing.distance_predictor_xyz:main',
        ],
    },
)
