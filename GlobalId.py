#
# Written by Vy Nguyen
#
from BaseJSON import BaseJSON

class GlobalId(BaseJSON):
    def __init__(self, glob):
        BaseJSON.__init__(self, glob)
        self.globalId = {}

    # -----------------------------------------------------------------------------
    # @Override
    def alloc(self):
        return self

    # -----------------------------------------------------------------------------
    #
    def add_obj(self, obj, order):
        oid = obj.get_id()
        if oid is None:
            if order is None:
                oid = "{:#x}".format(id(obj))
            else:
                oid = "{:#x}-{:d}".format(id(obj), order)

            obj['idName'] = oid

        self.globalId[oid] = obj

    # -----------------------------------------------------------------------------
    # Return the object matching id_name
    #
    def get_obj(self, id_name):
        if id_name in self.globalId:
            return self.globalId[id_name]
        return None

    # -----------------------------------------------------------------------------
    # Return global dictionary.
    #
    def get_var_dict(self):
        return self.js_dict

    # -----------------------------------------------------------------------------
    # Iter through all elements in global id table and invoke the 'method' in each.
    #
    def for_each(self, method, *args, **kvargs):
        for k, obj in self.globalId.iteritems():
            if obj == self:
                continue
            getattr(obj, method)(args, kvargs)

    # -----------------------------------------------------------------------------
    #
    def debug_dump(self):
        for k in self.globalId:
            print(self.globalId[k].toString())
