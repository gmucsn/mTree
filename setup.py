from setuptools import setup, find_packages
setup(
    name="mTree",
    version="0.3-BETA-13",
    packages=find_packages(),
    include_package_data=True,
    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires=['thespian==3.10.6',
                      'Flask==2.0.3',
                      'Flask-SocketIO==5.1.1',
                      'Flask-APScheduler==1.12.3',
                      'Flask-BasicAuth==0.2.0',
                      #'Flask-Bootstrap==3.3.7.1',
                      'Flask-SQLAlchemy==2.5.1',
                      'eventlet==0.33.0',
                      'numpy==1.22.2',
                      'python-socketio==5.5.2',
                    #   'PyYaml==5.3',
                      'pyfiglet==0.8.post1',
                      'jsonschema==4.4.0',
                      'requests==2.27.1',
                      'markdown==3.3.6',
                      'python-json-logger==2.0.2',
                      'python-engineio==4.3.1',
                      'simple-term-menu==1.3.0',
                      'sympy==1.9',
                        'terminaltables==3.1.10'
                    #   'socketio'
                    ],
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
