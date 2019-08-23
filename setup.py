from setuptools import setup, Extension
import os
import glob
import sys
import subprocess
import pkg_resources


def get_version():
    """Get the version info from the mpld3 package without importing it"""
    import ast

    with open(os.path.join("gqt", "__init__.py"), "r") as init_file:
      module = ast.parse(init_file.read())

    version = (ast.literal_eval(node.value) for node in ast.walk(module)
         if isinstance(node, ast.Assign)
         and node.targets[0].id == "__version__")
    try:
      return next(version)
    except StopIteration:
          raise ValueError("version could not be located")

sys.path[0:0] = ['setup-requires']
pkg_resources.working_set.add_entry('setup-requires')

def missing_requirements(specifiers):
    for specifier in specifiers:
        try:
            pkg_resources.require(specifier)
        except pkg_resources.DistributionNotFound:
            yield specifier

def install_requirements(specifiers):
    to_install = list(specifiers)
    if to_install:
        cmd = [sys.executable, "-m", "pip", "install",
            "-t", "setup-requires"] + to_install
        subprocess.call(cmd)

requires = ['cython']
install_requirements(missing_requirements(requires))

excludes = ['irods', 'plugin']

excludes.extend("""lib/gqt/src/gqt.c
lib/gqt/src/gt.c
lib/gqt/src/ihs.c
lib/gqt/src/misc.c
lib/gqt/src/read_binary_uints.c
lib/gqt/src/sandbox.c
lib/gqt/src/sort.c
lib/gqt/src/sum.c""".split())

sources = [x for x in glob.glob('lib/htslib/*.c') if not any(e in x for e in
    excludes)] + glob.glob('lib/htslib/cram/*.c')
sources = [x for x in sources if not x.endswith(('htsfile.c', 'tabix.c', 'bgzip.c'))]
sources.extend([x for x in glob.glob('lib/gqt/src/*.c') if not any(e in x for e in excludes)])


if not os.path.exists("lib/htslib/config.h"):
    import subprocess as sp
    sp.check_call("cd lib/htslib && autoreconf && ./configure --disable-bz2 --disable-lzma --enable-libcurl && make", shell=True)

if not os.path.exists("lib/gqt/src/query.h"):
    import subprocess as sp
    sp.check_call("mv gqt/query.h lib/gqt/src/", shell=True)
    
if not os.path.exists("lib/sqlite-amalgamation-3080701"):
    import subprocess as sp
    sp.check_call("cd lib && wget http://www.sqlite.org/2014/sqlite-amalgamation-3080701.zip && unzip sqlite-amalgamation-3080701 && rm -rf sqlite-amalgamation-3080701.zip", shell=True)

if not os.path.exists("lib/gqt/bin/gqt"):
    import subprocess as sp
    if not (sp.check_output(["flex", "-V"])[:4] == 'flex') or not (sp.check_output(["lex", "-V"])[:3] == 'lex'):
        sp.check_call("wget http://downloads.sourceforge.net/project/flex/flex-2.5.39.tar.bz2 && bunzip2 flex-2.5.39.tar.bz2 && tar xvf flex-2.5.39.tar && cd flex-2.5.39 && ./configure && make && make install", shell=True) 
    sp.check_call("sed -i 's/-lm/-lm -lcurl -lcrypto/g' lib/gqt/src/Makefile && make -C lib/gqt", shell=True)
    
from Cython.Distutils import build_ext

here = os.path.abspath(".")

cmdclass = {'build_ext': build_ext}
extension = [Extension("gqt.gqt",
                        ["gqt/gqt.pyx"] + sources,
                        libraries=['z', 'dl', 'm', 'curl', 'crypto', 'bz2', 'lzma', 'sqlite3'],
                        include_dirs=[here, "lib/gqt/src/", "lib/htslib", "lib/sqlite-amalgamation-3080701"])]
                        

setup(
    name="gqt",
    description="python wrapper to gqt",
    url="https://github.com/kevin-gorman/python-gqt/",
    version=get_version(),
    cmdclass=cmdclass,
    ext_modules=extension,
    packages=['gqt', 'gqt.tests'],
    test_suite='nose.collector',
    tests_require='nose',
    install_requires=[],
    include_package_data=True,
    zip_safe=False,
)
