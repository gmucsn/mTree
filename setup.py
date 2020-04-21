from setuptools import setup, find_packages
setup(
    name="mTree",
    version="0.3-BETA-12",
    packages=find_packages(),
    include_package_data=True,
    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires=['Flask>=1.1.2',
                      'Flask-APScheduler>=1.11.0',
                      'Flask-BasicAuth>=0.2.0',
                      'Flask-Bootstrap>=3.3.7.1',
                      'Flask-SocketIO>=4.3.0',
                      'Flask-SQLAlchemy>=2.4.1',
                      'eventlet>=0.20.1',
                      'numpy>=1.11.1',
                      'PyYaml>=3.12',
                      'thespian>=3.10.0',
                      'pyfiglet==0.8.post1'],
    scripts=['bin/mTree_control', 'bin/mTree_developer', 'bin/mTree_runner'],
    # metadata for upload to PyPI
    author="GMU CSN",
    author_email="mtree.email@gmail.com",
    description="This is the base mTree package",
    license="MIT",
    keywords="computational experimental economics",
    url="https://github.com/gmucsn/mTree",   # project home page, if any
)
