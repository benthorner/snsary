from pathlib import Path

import setuptools

setuptools.setup(
    name="snsary",
    version="0.0.1",
    author="Ben Thorner",
    author_email="benthorner@users.noreply.github.com",
    description="A framework for sensor metrics",
    url="https://github.com/benthorner/snsary",
    project_urls={
        "Bug Tracker": "https://github.com/benthorner/snsary/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=[
        *open('requirements/default.txt').read().splitlines(),
    ],
    extras_require={
        **{
            path.parent.stem: open(path).read().splitlines()
            for path in Path('requirements/').glob('*/extra.txt')
        },
        'all': set(
            line for path in Path('requirements/').glob('*/extra.txt')
            for line in open(path).read().splitlines()
        )
    }
)
