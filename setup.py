from distutils.core import setup

setup (
    name = 'win_inet_pton',
    version = '1.0.0',
    py_modules = ['win_inet_pton'],
    url = 'https://github.com/hickeroar/win_inet_pton',
    author = 'Ryan Vennell',
    author_email = 'ryan.vennell@gmail.com',
    description = 'A simple, non-persistent, key-value registry in memory.',
    license = open('LICENSE', 'r').read(),
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',\
        'Operating System :: OS Independent',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 2.7',
        'Topic :: Utilities'
    ]
)