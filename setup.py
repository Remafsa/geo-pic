from setuptools import find_packages
from setuptools import setup

with open("requirements.txt") as f:
    content = f.readlines()
requirements = [x.strip() for x in content if "git+" not in x]

setup(name='geo-pic',
      version="0.0.12",
      description="geo-pic Model (api_pred)",
      license="MIT",
      author="Rema",
      author_email="remaalnssiry@gmail.com",
      install_requires=requirements,
      packages=find_packages(),
      test_suite="tests",
      include_package_data=True,
      zip_safe=False)
