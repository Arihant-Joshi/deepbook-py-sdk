from setuptools import setup, find_packages

setup(
    name='deepbook-python-sdk',
    version='0.1.0',
    author='Arihant Joshi',
    author_email='joshi11.arihant@gmail.com',
    description='A Python SDK for interacting with the Deepbook Contracts/',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/my-python-sdk',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        # List your dependencies here
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)