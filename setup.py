from distutils.core import setup


setup_kwargs = {
    'name': 'dalianmao',
    'version': '0.09',
    'description': 'A Web Crawling and Web Scraping microframework based on aiohttp',
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
    'requirements': [
        'aiohttp>=1.3.3'
        'aiofiles>=0.3.0',
        'beautifulsoup4>=4.2.0',
        'motor>=1.1'
    ]
}

setup(**setup_kwargs)

print('DaLianMao version {} successfully installed.'.format(setup_kwargs['version']))
