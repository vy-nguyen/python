#
# Written by Vy Nguyen
#
import os

class DirMgr:
    def __init__(self):
        self.base = os.path.dirname(os.path.abspath(__file__))
        self.base = os.path.normpath(os.path.join(self.base, '..'))

        # Directories relative to patchlib dir.
        #
        self.dirTestCases = 'test-cases'
        self.dirTestData  = '../data'
        self.dirBin       = 'bin'
        self.dirPatchLib  = 'lib'
        self.dirConfig    = 'etc'

        # Resolve to absolute path.
        #
        self.abstTestCases = os.path.join(self.base, self.dirTestCases)
        self.abstTestData  = os.path.join(self.base, self.dirTestData)
        self.abstBin       = os.path.join(self.base, self.dirBin)
        self.abstPatchLib  = os.path.join(self.base, self.dirPatchLib)
        self.abstConfig    = os.path.join(self.base, self.dirConfig)

        self.jsonPath = [
            self.base,
            self.abstConfig,
            self.abstPatchLib
        ]

    def get_base_dir(self):
        return self.base

    def get_bin_dir(self):
        return self.abstBin

    def get_test_cases_dir(self):
        return self.abstTestCases

    def get_test_data_dir(self):
        return self.abstTestCases

    def get_patch_lib_dir(self):
        return self.abstPatchLib

    def get_config_dir(self):
        return self.abstConfig

    def get_json_paths(self):
        return self.jsonPath

    # ---------------------------------------------------------------------
    # Return the first json file from searched paths.
    #
    def get_json_file(self, jsfile):
        searchPath = self.get_json_paths()
        for parent in searchPath:
            tfile = os.path.join(parent, jsfile)
            if os.path.isfile(tfile):
                return tfile

        return None

    # ---------------------------------------------------------------------
    # Add the given list of paths to json searched paths.
    #
    def add_json_path(self, paths):
        pass

