from setuptools import setup, find_packages

setup(
    name="livereload_server",
    version='0.1',
    description="A livereloading HTTP server for static files",
    keywords='http,server,livereload',
    author='Prashanth Ellina',
    author_email="Use the github issues",
    url="https://github.com/prashanthellina/livereload_server",
    license='MIT License',
    install_requires=[
        'tornado',
        'watchdog',
    ],
    package_dir={'livereload_server': 'livereload_server'},
    packages=find_packages('.'),
    include_package_data=True,

    entry_points = {
        'console_scripts': [
            'livereload_server = livereload_server:main',
        ],
    },
)
