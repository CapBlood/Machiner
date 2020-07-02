from setuptools import setup


setup(name='Machiner', maintainer='CapBlood',
      author_email='stalker.anonim@mail.ru',
      packages=['machiner',
                'machiner.app',
                'machiner.app.widgets'],
      package_data={'machiner.app': ['design.qss']},
      include_package_data=True,
      install_requires=['PySide2', 'sklearn', 'pandas'])
