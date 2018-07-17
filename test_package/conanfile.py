import os

from conans import ConanFile, CMake, tools

class Tinyxml2TestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def imports(self):
        self.copy("*.dll", dst="bin", src="bin")
        self.copy("*.dylib*", dst="bin", src="lib")
        self.copy('*.so*', dst='bin', src='lib')
        # Not very elegant solution:
        # need to copy from the folder that contains this conan file to bin folder to be able
        # to execute tests
        self.copy("resources/*", src=os.path.join(os.getcwd(), "..", ".."), dst="bin")

    def test(self):
        if not tools.cross_building(self.settings):
            os.chdir("bin")
            self.run(".{}test".format(os.sep))