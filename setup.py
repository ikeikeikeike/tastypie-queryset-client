import os
from setuptools import setup, find_packages
# from setuptools.command.test import test

version = '0.6.4'
name = 'tastypie-queryset-client'
short_description = 'Client for Tastypie. Provide operation similar to the Django Model API'
long_description = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()


packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir != '':
    os.chdir(root_dir)
extensions_dir = 'queryset_client'


setup(
    name=name,
    version=version,
    description=short_description,
    long_description=long_description,
    classifiers=[
#       "Development Status :: 3 - Alpha",
       "Development Status :: 4 - Beta",
       "Development Status :: 5 - Production/Stable",
       "Framework :: Django",
#       'Environment :: Console',
       "Environment :: Web Environment",
       "Intended Audience :: Developers",
       'License :: OSI Approved :: MIT License',
       "Programming Language :: Python :: 2.6",
       "Programming Language :: Python :: 2.7",
       'Topic :: Utilities',
       'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords=['tastypie', 'client', 'django', 'rest', 'api', ],
    author='Tatsuo Ikeda',
    author_email='jp.ne.co.jp at gmail',
    url='https://github.com/ikeikeikeike/tastypie-queryset-client',
    license='MIT License',
    packages=find_packages(),
    include_package_data=True,
    data_files=data_files,
    install_requires=["slumber"],
    # cmdclass={'test': pytest_test},
    # tests_require=['pytest'],
)
