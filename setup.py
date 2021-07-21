from setuptools import setup, find_packages
setup(
    name="mTree",
    version="0.3-BETA-13",
    packages=find_packages(),
    include_package_data=True,
    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires=['Flask==1.1.2',
                      'Flask-APScheduler==1.11.0',
                      'Flask-BasicAuth==0.2.0',
                      'Flask-Bootstrap==3.3.7.1',
                      'Flask-SocketIO==5.0.1',
                      'Flask-SQLAlchemy==2.4.4',
                      'eventlet==0.30.0',
                      'numpy==1.18.1',
                      'PyYaml==5.3',
                      'thespian==3.10.3',
                      'pyfiglet==0.8.post1',
                      'jsonschema==3.2.0',
                      'requests==2.22.0',
                      'markdown==3.3.3',
                      'python-json-logger==2.0.1'],
    #scripts=['bin/mTree_control', 'bin/mTree_developer', 'bin/mTree_runner', 'bin/mTree_generate', 'bin/mTree_server','bin/mTree_server_backend'],
    entry_points={
        'console_scripts':['mTree_runner=mTree.scripts.mTree_runner:main',
            'mTree_developer_server=mTree.scripts.mTree_developer_server:main']
    },
    # metadata for upload to PyPI
    author="GMU CSN",
    author_email="mtree.email@gmail.com",
    description="This is the base mTree package",
    license="MIT",
    keywords="computational experimental economics",
    url="https://github.com/gmucsn/mTree",   # project home page, if any
)
