from setuptools import setup, find_packages

setup(
    name="terraform-smart-pack",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "tsp=main:main",
        ],
    },
    python_requires=">=3.6",
)
