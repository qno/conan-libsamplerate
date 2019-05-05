from conans import ConanFile, CMake, tools
from conans.errors import ConanInvalidConfiguration
import re, os


class LibSampleRateConan(ConanFile):
    name = "libsamplerate"
    version = "latest"
    license = "BSD-2-Clause"
    author = "Erik de Castro Lopo"
    homepage = "http://www.mega-nerd.com/libsamplerate"
    url = "https://github.com/qno/conan-libsamplerate"
    description = "libsamplerate (also known as Secret Rabbit Code) is a library for performing sample rate conversion of audio data."

    settings = "os", "compiler", "build_type", "arch"

    options = {
        "shared": [True, False],
        "fPIC": [True, False]
        }
    default_options = {
        "shared": False,
         "fPIC": True
         }

    generators = "cmake"

    _pkg_name = "libsamplerate-master"
    _libname = "samplerate"

    def source(self):
        url = "https://github.com/erikd/libsamplerate/archive/master.zip"
        self.output.info("Downloading {}".format(url))
        tools.get(url)
        # the conan_basic_setup() must be called, otherwise the compiler runtime settings won't be setup correct,
        # which then leads then to linker errors if recipe e.g. is build with /MT runtime for MS compiler
        # see https://github.com/conan-io/conan/issues/3312
        self._patchCMakeListsFile(self._pkg_name)

    def configure(self):
        del self.settings.compiler.libcxx

        if self._isVisualStudioBuild():
            del self.options.fPIC
            if self.options.shared:
                raise ConanInvalidConfiguration("This library doesn't support dll's on Windows")

    def build(self):
        cmake = CMake(self)
        cmake.definitions["LIBSAMPLERATE_TESTS"] = "OFF"
        cmake.configure(source_dir=self._pkg_name)
        cmake.build()

    def package(self):
        self.copy("src/samplerate.h", dst="include", keep_path=False, src=self._pkg_name)
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="lib", keep_path=False)
        self.copy("*.so*", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = []

        if self.settings.os == "Linux":
            self.cpp_info.libs.append("m")

        self.cpp_info.libs.append(self._libname)

    def _isVisualStudioBuild(self):
        return self.settings.os == "Windows" and self.settings.compiler == "Visual Studio"

    def _patchCMakeListsFile(self, src_dir):
        cmake_project_line = ""
        cmake_file = "{}{}CMakeLists.txt".format(src_dir, os.sep)
        self.output.warn("patch '{}' to inject conanbuildinfo".format(cmake_file))
        for line in open(cmake_file, "r", encoding="utf8"):
            if re.match("^PROJECT.*\\(.*\\).*", line.strip().upper()):
                cmake_project_line = line.strip()
                self.output.warn("found cmake project declaration '{}'".format(cmake_project_line))
                break

        tools.replace_in_file(cmake_file, "{}".format(cmake_project_line),
                              '''{}
include(${{CMAKE_BINARY_DIR}}/conanbuildinfo.cmake)
conan_basic_setup()'''.format(cmake_project_line))

