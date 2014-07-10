try:
    from setuptools import setup
except:
    from distutils.core import setup

setup(
    name="mo_t",
    version="0.1.0",
    author="mo",
    author_email="mohitleo9@gmail.com",
    description=" simple todo with deadlines",
    licesse="BSD",
    install_requires=[
        "arrow==0.4.2",
        "parsedatetime==1.2"
    ],
    py_modules=['t'],
    entry_points={
        'console_scripts': ['t = t:main']
    }
)
