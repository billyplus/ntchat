from setuptools import setup, Extension, find_packages
from distutils.errors import *
from distutils.dep_util import newer_group
from distutils import log
from distutils.command.build_ext import build_ext

import os
import sys
import platform
import re
import pathlib
from distutils.ccompiler import CCompiler
from multiprocessing.pool import ThreadPool as Pool
import setup_conf


def compile(self, sources, output_dir=None, macros=None, include_dirs=None, debug=0, extra_preargs=None,
            extra_postargs=None, depends=None):
    macros, objects, extra_postargs, pp_opts, build = self._setup_compile(output_dir, macros, include_dirs, sources,
                                                                          depends, extra_postargs)
    cc_args = self._get_cc_args(pp_opts, debug, extra_preargs)

    def f(x):
        try:
            src, ext = build[x]
        except KeyError:
            return

        self._compile(x, src, ext, cc_args, extra_postargs, pp_opts)

    pool = Pool(processes=6)
    pool.map(f, objects)

    return objects


# Overwrite to enable multiprocess compilation
CCompiler.compile = compile

target_os = 'none'
if sys.platform == 'darwin':
    target_os = 'darwin'
elif os.name == 'posix':
    target_os = 'posix'
elif platform.system() == 'Windows':
    target_os = 'win32'

target_os_arch = 'x64' if sys.maxsize > 2 ** 32 else 'x86'


def filter_sources(sources):
    """Filters sources into c, cpp and objc"""
    cpp_ext_match = re.compile(r'.*[.](cpp|cxx|cc|hpp)\Z', re.I).match
    c_ext_match = re.compile(r'.*[.](c|C)\Z', re.I).match
    objc_ext_match = re.compile(r'.*[.]m\Z', re.I).match

    c_sources = []
    cpp_sources = []
    objc_sources = []
    other_sources = []
    for source in sources:
        if c_ext_match(source):
            c_sources.append(source)
        elif cpp_ext_match(source):
            cpp_sources.append(source)
        elif objc_ext_match(source):
            objc_sources.append(source)
        else:
            other_sources.append(source)
    return c_sources, cpp_sources, objc_sources, other_sources


def build_extension(self, ext):
    """Modified version of build_extension method from distutils.
       Can handle compiler args for different files"""

    sources = ext.sources
    if sources is None or not isinstance(sources, (list, tuple)):
        raise DistutilsSetupError(
            "in 'ext_modules' option (extension '%s'), "
            "'sources' must be present and must be "
            "a list of source filenames" % ext.name)

    sources = list(sources)
    ext_path = self.get_ext_fullpath(ext.name)
    depends = sources + ext.depends
    if not (self.force or newer_group(depends, ext_path, 'newer')):
        log.debug("skipping '%s' extension (up-to-date)", ext.name)
        return
    else:
        log.info("building '%s' extension", ext.name)

    sources = self.swig_sources(sources, ext)

    extra_args = ext.extra_compile_args or []
    extra_c_args = getattr(ext, "extra_compile_c_args", [])
    extra_cpp_args = getattr(ext, "extra_compile_cpp_args", [])
    extra_objc_args = getattr(ext, "extra_compile_objc_args", [])
    macros = ext.define_macros[:]
    for undef in ext.undef_macros:
        macros.append((undef,))

    c_sources, cpp_sources, objc_sources, other_sources = filter_sources(sources)

    def _compile(src, args):
        return self.compiler.compile(src,
                                     output_dir=self.build_temp,
                                     macros=macros,
                                     include_dirs=ext.include_dirs,
                                     debug=self.debug,
                                     extra_postargs=extra_args + args,
                                     depends=ext.depends)

    objects = []
    objects += _compile(c_sources, extra_c_args)
    objects += _compile(cpp_sources, extra_cpp_args)
    objects += _compile(objc_sources, extra_objc_args)
    objects += _compile(other_sources, [])

    self._built_objects = objects[:]
    if ext.extra_objects:
        objects.extend(ext.extra_objects)

    extra_args = ext.extra_link_args or []

    language = ext.language or self.compiler.detect_language(sources)
    self.compiler.link_shared_object(
        objects, ext_path,
        libraries=self.get_libraries(ext),
        library_dirs=ext.library_dirs,
        runtime_library_dirs=ext.runtime_library_dirs,
        extra_postargs=extra_args,
        export_symbols=self.get_export_symbols(ext),
        debug=self.debug,
        build_temp=self.build_temp,
        target_lang=language)


# patching
build_ext.build_extension = build_extension

definitions = {
    'win32': [("HPSOCKET_STATIC_LIB", None), ("UNICODE", None), ("_UNICODE", None)],
}

libs = {
    'win32': ["kernel32", "user32", "gdi32", "winspool",
              "comdlg32", "advapi32", "shell32", "ole32",
              "oleaut32", "uuid", "odbc32", "odbccp32"],
}

extra_libs = {
    'win32': setup_conf.extra_libs
}

extra_libs_dir = {
    'win32': [f"{setup_conf.extra_libs_dir_prefix}\\{target_os_arch}"]
}

extra_link = {
    'win32': [],
}

extra_compile_args = {
    'darwin': [],
    'posix': [],
    'win32': ['/MT', "/EHsc", "/bigobj"],
}

extra_compile_cpp_args = {
    'darwin': ['-std=c++11'],
    'posix': ['-std=c++11'],
    'win32': [],
}

cpp_code_sources = [str(path) for path in pathlib.Path(setup_conf.cpp_source_dir).rglob("*.cpp")]


def add_prefix(l, prefix):
    return [os.path.join(prefix, x) for x in l]


extension = Extension("ntchat.wc.wcprobe",
                      cpp_code_sources,
                      define_macros=definitions[target_os],
                      include_dirs=setup_conf.include_dirs,
                      extra_compile_args=extra_compile_args[target_os],
                      extra_link_args=extra_link[target_os],
                      libraries=libs[target_os],
                      extra_objects=extra_libs[target_os],
                      library_dirs=extra_libs_dir[target_os])

extension.extra_compile_cpp_args = extra_compile_cpp_args[target_os]

setup(
    name='ntchat',
    version='0.1.16',
    description='About Conversational RPA SDK for Chatbot Makers',
    long_description="",
    long_description_content_type='text/markdown',
    url='https://github.com/smallevilbeast/ntchat',
    author='evilbeast',
    author_email='784615627@qq.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10'
    ],
    package_data={"": ["py.typed", "*.pyi", "helper*.dat"]},
    include_package_data=False,
    packages=find_packages(include=['ntchat', 'ntchat.*']),
    keywords='wechat ntchat pywechat rebot',
    install_requires=['pyee', 'xcgui'],
    ext_modules=[extension]
)
