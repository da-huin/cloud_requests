import io
from setuptools import find_packages, setup

# python3 setup.py sdist bdist_wheel && python3 -m twine upload --skip-existing dist/*

def long_description():
    with io.open('README.md', 'r', encoding='utf-8') as f:
        readme = f.read()
    return readme

setup(name='cloud_requests',
      version='1.0.1',
      description='When making a requests to Google Cloud Service, it allows you to make a simple request without complicated authentication.',
      long_description="Please refer to the https://github.com/da-huin/cloud_requests",
      long_description_content_type="text/markdown",
      url='https://github.com/da-huin/cloud_requests',
      download_url= 'https://github.com/da-huin/cloud_requests/archive/master.zip',
      author='da-huin',
      author_email='dahuin000@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=["pyjwt", "requests"],
      classifiers=[
          'Programming Language :: Python :: 3',
    ]
)
