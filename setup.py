from setuptools import setup, find_packages

setup(
    name="lovejoy_antiques",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask>=3.0.0',
        'flask-sqlalchemy',
        'flask-login',
        'flask-mail',
        'flask-wtf',
        'pymysql',
        'python-dotenv',
        'werkzeug',
        'email-validator',
        'pillow',
        'pyjwt'
    ]
) 