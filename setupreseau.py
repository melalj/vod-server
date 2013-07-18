import sys, os
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [], excludes = [])

#executables = [
 #   Executable('serveur.py', 'Console', targetName = 'serveur.exe')
#]
# preparation des options 
path = sys.path.append(os.path.join("..", "..", "biblio"))
includes = ["printx", "bibconcours"]
excludes = []
packages = []
 
options = {"path": path,
           "includes": includes,
           "excludes": excludes,
           "packages": packages
           }
 
#############################################################################
# preparation des cibles
base = None
if sys.platform == "win32":
    base = "Win32GUI"
 
cible_1 = Executable(
    script = "main.py",
    base = base,
    compress = True,
    icon = None,
    )
 
cible_2 = Executable(
    script = "catalogue.py",
    base = base,
    compress = True,
    icon = None,
    )

cible_3 = Executable(
    script = "TCP_Push.py",
    base = base,
    compress = True,
    icon = None,
    )
 
cible_4 = Executable(
    script = "TCP_Pull.py",
    base = base,
    compress = True,
    icon = None,
    )

cible_5 = Executable(
    script = "SocketServer.py",
    base = base,
    compress = True,
    icon = None,
    )
 
cible_6 = Executable(
    script = "SocketClient.py",
    base = base,
    compress = True,
    icon = None,
    )

cible_7 = Executable(
    script = "VideoServer.py",
    base = base,
    compress = True,
    icon = None,
    )

cible_8 = Executable(
    script = "UDP_PULL.py",
    base = base,
    compress = True,
    icon = None,
    )

setup(name='serveur.py',
      version = '1.0',
      description = 'none',
      options = dict(build_exe = buildOptions),
      executables = [cible_1, cible_2, cible_3, cible_4, cible_5, cible_6, cible_7, cible_8])
