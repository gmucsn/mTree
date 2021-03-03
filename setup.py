from setuptools import setup, find_packages
setup(
    name="mTree",
    version="0.3-BETA-13",
    packages=find_packages(),
    include_package_data=True,
    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires=['Flask>=1.1.2',
                      'Flask-APScheduler>=1.11.0',
                      'Flask-BasicAuth>=0.2.0',
                      'Flask-Bootstrap>=3.3.7.1',
                      'Flask-SocketIO>=5.0.1',
                      'Flask-SQLAlchemy>=2.4.1',
                      'eventlet>=0.20.1',
                      'numpy>=1.11.1',
                      'PyYaml>=3.12',
                      'thespian>=3.10.3',
                      'pyfiglet==0.8.post1',
                      'python-json-logger==2.0.1',
                      'jsonschema==3.2.0',
                      'requests==2.25.1',
                      'markdown==3.3.4'],
    scripts=['bin/mTree_control', 'bin/mTree_developer', 'bin/mTree_runner', 'bin/mTree_generate', 'bin/mTree_server','bin/mTree_server_backend'],
    # metadata for upload to PyPI
    author="GMU CSN",
    author_email="mtree.email@gmail.com",
    description="This is the base mTree package",
    license="MIT",
    keywords="computational experimental economics",
    url="https://github.com/gmucsn/mTree",   # project home page, if any
)
