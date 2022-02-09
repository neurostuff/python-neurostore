from setuptools import setup, find_packages
PACKAGES = find_packages()

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='python-neurostore',
      version='0.1',
      description='NeuroStore API wrapper',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='http://github.com/neurostuff/python-neurostore',
      author='Alejandro de la Vega',
      author_email='aleph4@gmail.com',
      install_requires=['requests>=2.21', 'pyjwt~=1.7.1', 'requests-oauthlib'],
      license='MIT',
      packages=PACKAGES,
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ],
      zip_safe=False)
