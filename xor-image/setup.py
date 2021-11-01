from setuptools import setup

setup(
    name="xor-scrambling",
    # package_dir={"": "src"},
    packages=["src"],
    version="0.1",
    entry_points="""
        [console_scripts]
        python-xor=src.main:main
    """,
)
