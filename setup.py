from distutils.core import setup


setup_kwargs = {
    'name': 'dalianmao',
    'version': '0.07',
    'description': 'A Web Crawling and Web Scraping microframework based on uvloop and aiohttp',
    'long_description': open('README.md', encoding='utf-8').read(),
    'packages': ['dalianmao',],
    'platforms': 'any',
    'license': 'MIT',
    'author': 'Zeng Jianxin',
    'author_email': 'zengjx92@163.com',
    'url': 'https://github.com/ZengJianxin/dalianmao',
    'classifiers': [
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
}

try:
    normal_requirements = [
        'uvloop>=0.5.3',
        'aiohttp>=1.3.3',
        'aiofiles>=0.3.0',
        'beautifulsoup4>=4.2.0',
        'motor>=1.1'
    ]
    setup_kwargs['install_requires'] = normal_requirements
    setup(**setup_kwargs)
except RuntimeError as exception:
    windows_requirements = [
        'aiohttp>=1.3.3'
        'aiofiles>=0.3.0',
        'beautifulsoup4>=4.2.0',
        'motor>=1.1'
    ]
    setup_kwargs['install_requires'] = windows_requirements
    setup(**setup_kwargs)

print('DaLianMao version {} successfully installed.'.format(setup_kwargs['version']))
