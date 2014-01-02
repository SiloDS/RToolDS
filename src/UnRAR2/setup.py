# setup.py, config file for distutils

#@PydevCodeAnalysisIgnore

import UnRAR

from distutils.core import setup
from distutils.command.install_data import install_data
import os


class smart_install_data(install_data):
    def run(self):
        #need to change self.install_dir to the actual library dir
        install_cmd = self.get_finalized_command('install')
        self.install_dir = getattr(install_cmd, 'install_lib') #IGNORE:W0201
        return install_data.run(self)


data_files = []
for dirpath, dirnames, filenames in os.walk(r'..\UnRAR'):
    for dirname in ['build', 'dist', '_sgbak']:
        try:
            dirnames.remove(dirname)
        except ValueError: #IGNORE:W0704
            pass
    for filename in [fn for fn in filenames if os.path.splitext(fn)[-1].lower() in ('.pyc', '.pyo', '.scc')]:
        filenames.remove(filename)
    data_files.append((dirpath.lstrip('.').lstrip('\\'), [os.path.join(dirpath, fn) for fn in filenames]))


setup(name='pyUnRAR',
      version=UnRAR.__version__,
      description='A ctypes based wrapper around the free UnRAR.dll',
      long_description=UnRAR.__doc__.strip(),
      author='Jimmy Retzlaff',
      author_email='jimmy@retzlaff.com',
      url='http://www.averdevelopment.com/python',
      download_url='http://www.averdevelopment.com/python/pyUnRAR-%s.win32.exe' % UnRAR.__version__,
      license='MIT',
      platforms='Windows',
      classifiers=[
                   'Development Status :: 5 - Production/Stable',
                   'Environment :: Win32 (MS Windows)',
                   'License :: OSI Approved :: MIT License',
                   'Natural Language :: English',
                   'Operating System :: Microsoft :: Windows',
                   'Programming Language :: Python',
                   'Topic :: Software Development :: Libraries :: Python Modules',
                   'Topic :: System :: Archiving :: Compression',
                  ],
      packages=['UnRAR'],
      package_dir={'UnRAR' : ''},
      data_files=data_files,
      cmdclass = {'install_data': smart_install_data},
     )
