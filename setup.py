from setuptools import setup, find_packages

setup(
    name='lobechatservice',
    version='1.0',
    description='LobeChat Service based on Flask framework',
    platforms=['x86_64'],
    include_package_data=True,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'lobechatservice = app:app.run',
        ]
    },
)
