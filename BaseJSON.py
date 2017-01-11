#
# Written by Vy Nguyen
#
from string import Template
from pprint import pprint

class BaseJSON:
    def __init__(self, glob):
        self.glob    = glob
        self.keyword = None
        self.js_dict = {
            'idName': None
        }

    # -------------------------------------------------------------------
    # Allocate a new instance for this obj.
    #
    def alloc(self):
        obj_type = self.__class__
        obj_inst = obj_type(self.glob)
        obj_inst.keyword  = self.keyword
        obj_inst.jsonFile = self.glob.get_parsing_file()

        return obj_inst

    def assign_keyword(self, kw):
        self.keyword = kw

    def debug_id(self):
        return "{} - ({}@{:x})".format(self['idName'], str(self.__class__), id(self))

    def get_owner_json(self):
        if hasattr(self, 'jsonFile'):
            return self.jsonFile
        return self.glob.get_parsing_file()

    # -------------------------------------------------------------------
    # Return the string form for debugging
    #
    def toString(self):
        out = []
        out.append(self.debug_id())
        out.append("\n")

        for k in self.js_dict:
            out.append("\t{0}: {1}\n".format(k, str(self.js_dict[k])))

        if hasattr(self, 'array'):
            out.append("\tArray: {0}\n".format(str(self.array)))

        return ''.join(out)


    def __setitem__(self, key, value):
        self.js_dict[key] = value


    def __getitem__(self, key):
        if key in self.js_dict:
            return self.js_dict[key]
        return None


    def get_id(self):
        return self.js_dict['idName']

    # -------------------------------------------------------------------
    # Return string value for the key after resolving variables.
    #
    def get_value(self, key, subst = False, save = False):
        if key not in self.js_dict:
            return None

        value = self.js_dict[key]
        if key == 'idName' or subst is False:
            return value

        return self.subst_var(key, value, save)

    # -------------------------------------------------------------------
    # Perform variable substitution at the basic string.
    #
    def subst_var(self, key, value, save):
        if isinstance(value, basestring):
            s = Template(value)
            id_mgr = self.glob.get_id_mgr()
            subst = s.safe_substitute(id_mgr.get_var_dict())

            if save is True and key is not None:
                self.js_dict[key] = subst

            return subst

        if isinstance(value, list):
            i = 0
            for elm in value:
                ret = self.subst_var(None, elm, save)
                if save is True:
                    value[i] = ret
                    i += 1

        return value

    # -------------------------------------------------------------------
    # Resolve variables through global substitution.
    #
    def resolve_vars(self, *args, **kvargs):
        for key, value in self.js_dict.iteritems():
            self.get_value(key, True, True)

    # -------------------------------------------------------------------
    # Resolve name to object handlers.
    #
    # @BaseMethod
    def resolve_handler(self, *args, **kvargs):
        id_mgr = self.glob.get_id_mgr()
        symtab = self.glob.get_symtab()

        for key, value in self.js_dict.iteritems():
            if key == 'idName':
                continue
            if isinstance(value, basestring):
                handler = id_mgr.get_obj(value)
                if handler is not None:
                    # Replace string id with the actual handler
                    #
                    self[key] = handler
                    print("Replace id " + value + " with " + handler.keyword)
                else:
                    if symtab.get_handler(key):
                        self.glob.warn_bad_obj_id(self.get_owner_json(), key, value)

    # -------------------------------------------------------------------
    # Internal method to invoke each Python object parsed.
    #
    def invoke(self, *args, **kvargs):
        self.run(args, kvargs)

    # -------------------------------------------------------------------
    # Subclass must override this method.
    #
    # @BaseMethod
    #
    def run(self, *args, **kvargs):
        print("Default run " + self.toString())

    @staticmethod
    def is_complex_type(obj):
        return (isinstance(obj, dict) or isinstance(obj, list))

    # -------------------------------------------------------------------
    # This method is best to leave it alone.
    #
    # Parse JSON structure to Python object and add it to the global Id
    # table.
    #
    def parse(self, json_obj, order):
        obj_inst = None
        id_mgr = self.glob.get_id_mgr()
        symtab = self.glob.get_symtab()

        # Get the correct instance or allocate for the correct type.
        #
        if 'idName' in json_obj:
            obj_inst = id_mgr.get_obj(json_obj['idName'])

        if obj_inst is None:
            obj_inst = self.alloc()

        # The whole json_obj is an array.
        #
        if isinstance(json_obj, list):
            i = 0
            array = []
            for elm in json_obj:
                if BaseJSON.is_complex_type(elm):
                    array.append(self.parse(elm, i))
                    i += 1
                else:
                    array.append(elm)

            obj_inst.array = array
            id_mgr.add_obj(obj_inst, order)
            return obj_inst

        # Check for expected built-in keys from the parsing object.
        #
        for key in self.js_dict:
            if key == 'idName':
                continue
            if not key in json_obj:
                self.glob.warn_missing_key(self.get_owner_json(), self.keyword, key)

        # Process each keyword entries in the JSON object.
        #
        if isinstance(json_obj, dict):
            for key, value in json_obj.iteritems():
                if not BaseJSON.is_complex_type(value):
                    obj_inst[key] = value
                    continue

                if key == 'import':
                    # Important: avoid calling the 'run' method on self so that the
                    # import kw can't be used to inject exec during parsing.
                    #
                    imp = symtab.get_handler('import')
                    imp.do_import(value)
                    continue

                handler = symtab.get_handler(key)
                if isinstance(value, list):
                    i = 0
                    for elm in value:
                        if BaseJSON.is_complex_type(elm):
                            if handler is not None:
                                elm = handler.parse(elm, i)
                            elif i == 0:
                                self.glob.warn_unknown_obj(self.get_owner_json(), key)
                                continue

                        if obj_inst[key] is None:
                            obj_inst[key] = []

                        i += 1
                        obj_inst[key].append(elm)
                else:
                    if handler is not None:
                        obj_inst[key] = handler.parse(value, None)
                    else:
                        self.glob.warn_unknown_obj(self.get_owner_json(), key)

        else:
            obj_inst[key] = json_obj

        id_mgr.add_obj(obj_inst, order)
        return obj_inst
