#
# Written by Vy Nguyen
#
from Import     import Import
from Script     import Script, Exec
from Replace    import Replace
from GlobalId   import GlobalId

class SymTab:
    def __init__(self, glob):
        self.glob = glob
        self.symbols = {
            # Use one globalId for global vars.
            #
            'globalId': glob.get_id_mgr(),

            # These keywords have run method to handle exec calls.
            #
            'import' : Import(self.glob),
            'script' : Script(self.glob),
            'exec'   : Exec(self.glob),
            'replace': Replace(self.glob)
        }
        # Assign keywords for items in the table.
        #
        for key, value in self.symbols.iteritems():
            value.assign_keyword(key)


    def get_handler(self, kw):
        if kw in self.symbols:
            return self.symbols[kw]
        return None

    def get_parsing_file(self):
        handler = self.symbols['import']
        return handler.get_parsing_file()
