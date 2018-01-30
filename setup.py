from setuptools import setup, find_packages
from pip.req import parse_requirements

# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements('requirements.txt', session='hack')

# reqs is a list of requirement
# e.g. ['django==1.5.1', 'mezzanine==1.4.6']
reqs = [str(ir.req) for ir in install_reqs]

setup(name='ocbot',
      version='1.0dev',
      packages=find_packages(),
      description='Python slack bot with external api support',
      long_description=open('README.md').read(),
      classifiers=[
        "License :: OSI Approved :: MIT License",
        "Topic :: Utilities",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Natural Language :: English",
    ],
      install_requires=reqs, # not the best to set requirements.txt and setup.py equal
      keywords='operation-code slack',
      author='operation code',
      author_email='william.montgomery-1@colorado.edu',
      url='https://github.com/OperationCode/operation_code_pybot',
      license='MIT License',
      include_package_data=True,
      zip_safe=True
      )