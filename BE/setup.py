from setuptools import setup
"""in case torch install fails
        #finding a way to use  pip install torch===1.6.0 torchvision===0.7.0 -f
         https://download.pytorch.org/whl/torch_stable.html might be necessary"""
setup(
    name = 'sticker_backend',
    packages = ['app'],
    include_package_data = True,
    install_requires=[
        'flask',
        'flask_restx',
        'torch',
        'rembg',
        'flask_marshmallow',
        'flask_bcrypt',
        'flask_sqlalchemy',
        'flask_jwt_extended',
        'flask_migrate',
        'flask_cors',
        'pyopenssl',

    ],
)