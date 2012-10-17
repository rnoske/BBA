from distutils.core import setup
import py2exe
import matplotlib

#setup(console=['guiHandler.py'])
setup(windows=['guiHandler.py'],
      data_files=matplotlib.get_py2exe_datafiles(),
      options={"py2exe": {"includes": ["sip", "PyQt4.QtGui", 'PyQt4.QtCore']}})

