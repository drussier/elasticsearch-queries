# packaging.python.org/tutorials/packaging-projects/
# https://amir.rachum.com/blog/2017/07/28/python-entry-points/
# https://docs.pytest.org/en/3.0.2/goodpractices.html#integrating-with-setuptools-python-setup-py-test-pytest-runner
# no dash in module name : https://stackoverflow.com/a/30284007
from setuptools import setup, find_packages

setup(
    name="es-queries",
    version="0.1",
    description="API diseases extractor",
    author="Damien RUSSIER",
    author_email="damien.russier@360medics.com",
    # url="https://github.com/360medics/ds-api-diseases-extractor.git",
    packages=find_packages(),
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    classifiers=[
        "Programming language :: Python :: 3",
        "Operating System :: macOS Catalina 10.15.7",
    ],
    # entry_points={
    # "console_scripts": [
    # "api-diseases-extractor = api_diseases_extractor.main:main",
    # ],
    # },
    python_requires=">=3.6",
)
