#
# Written by Vy Nguyen
#
from pprint   import pprint

from SymTab   import SymTab
from TestEnv  import DirMgr
from GlobalId import GlobalId

class Global():
    def __init__(self):
        self.dirMgr   = DirMgr()
        self.globalId = GlobalId(self)

    # Return singleton managers
    #
    def get_dir_mgr(self):
        return self.dirMgr

    def get_id_mgr(self):
        return self.globalId

    # Get for symbol table.
    #
    def get_symtab(self):
        return self.symtab


    def get_import_handler(self):
        return self.symtab.get_handler('import')


    def toString(self):
        return 'Global'


    def get_parsing_file(self):
        return self.symtab.get_parsing_file()


    # --------------------------------------------------------------------------------
    # Get list of json files to parse.
    #
    def run_file(self, in_file):
        self.symtab = SymTab(self)
        handler = self.symtab.get_handler('import')
        handler.run(in_file)

    # --------------------------------------------------------------------------------
    # The main entry after parsing.
    #
    def main(self):
        self.globalId.resolve_vars()
        self.globalId.resolve_handler()

        self.globalId.for_each('resolve_vars')
        self.globalId.for_each('resolve_handler')
        self.globalId.for_each('invoke')

    def debug_dump(self):
        print("------- Global ID Table ----------")
        self.globalId.debug_dump()

    # --------------------------------------------------------------------------------
    # Wire up all warning/error reporting here.
    #
    def warn_missing_key(self, js_file, obj, key):
        print("Warning: {0}\nObject {1} doesn't have expected key {2}"
                .format(js_file, obj, key))

    def warn_unknown_obj(self, js_file, obj):
        print("Warning: {0}\nDon't know how to parse {1}" .format(js_file, obj))

    def warn_bad_obj_id(self, js_file, key, obj):
        print("Warning: {0}\nDon't have id {1} for object {2}".format(js_file, key, obj))
