from setuptools import setup

setup(
    name="xor-scrambling",
    version="0.1",
    # py_modules=["inout"],
    # include_package_data=True,
    # install_requires=["click"],
    entry_points="""
        [console_scripts]
        python-xor=main:main
    """,
)
