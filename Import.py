#
# Writeen by Vy Nguyen
#
import json
import traceback

from pprint import pprint
from BaseJSON import BaseJSON

class Import(BaseJSON):
    def __init__(self, glob):
        BaseJSON.__init__(self, glob)
        self.parsing_file = None


    def do_import(self, value):
        # XXX todo: check for value is array of strings
        #
        self.run(value)

    # ---------------------------------------------------------------------------
    # Do nothing for invoke to disable running it globally.
    #
    # @Override
    def invoke(self, *args, **kvargs):
        pass

    def run(self, *args, **kvargs):
        dir_mgr = self.glob.get_dir_mgr()
        for in_file in args:
            for f in in_file:
                jsfile = dir_mgr.get_json_file(f)
                if not jsfile:
                    print('Warning: failed to open json file ' + f)
                    continue

                try:
                    with open(jsfile) as fd:
                        self.parsing_file = jsfile
                        try:
                            js_raw = json.load(fd)
                            self.parse(js_raw, None)
                        except:
                            print('Failed to parse file ' + jsfile)
                            traceback.print_exc()

                    self.parsing_file = jsfile
                except:
                    print('Failed to open json file ' + jsfile)


    # ---------------------------------------------------------------------------
    # Return the file is in parsing in current import statemeht.
    #
    def get_parsing_file(self):
        return self.parsing_file

