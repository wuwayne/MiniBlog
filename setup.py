import io

from setuptools import find_packages, setup

with io.open('README.md', 'r', encoding='utf8') as f:
    readme = f.read()

setup(
    name='KBS',
    version='0.0.1',
    license='MIT',
    maintainer='kms19',
    maintainer_email='wulove5@gmail.com',
    description='A basic KMS app',
    long_description=readme,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)
