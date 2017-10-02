from typing import Tuple, List

from pip.download import PipSession
from pip.req import parse_requirements
from setuptools import setup, find_packages


def get_requirements(file: str = "requirements.txt") -> Tuple[List[str], List[str]]:
    install_requires, dependency_links = [], []
    requirements = parse_requirements(file, session=PipSession())
    for i in requirements:
        install_requires.append(str(i.req))
        if i.link:
            dependency_links.append(i.link.url)
    return install_requires, dependency_links



install_requirements, dependencies = get_requirements("requirements.txt")

setup(
    name="BackendAPI",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    dependency_links=dependencies,
    install_requires=install_requirements)
