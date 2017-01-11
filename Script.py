#
# Written by Vy Nguyen
#
from BaseJSON import BaseJSON

class Script(BaseJSON):
    def __init__(self, glob):
        BaseJSON.__init__(self, glob)


class Exec(BaseJSON):
    def __init__(self, glob):
        BaseJSON.__init__(self, glob)
