#
# -*- coding: utf-8 -*-
#
# This file is part of reclass
#

from item import Item
from reclass.utils.dictpath import DictPath
from reclass.errors import UndefinedVariableError

class RefItem(Item):

    def __init__(self, items, delimiter):
        self.type = Item.REFERENCE
        self._delimiter = delimiter
        self._items = items
        self._refs = []
        self._allRefs = False
        self.assembleRefs()

    def assembleRefs(self, context={}):
        self._refs = []
        self._allRefs = True
        for item in self._items:
            if item.has_references():
                item.assembleRefs(context)
                self._refs.extend(item.get_references())
                if item.allRefs() == False:
                    self._allRefs = False
        try:
            strings = [ str(i.render(context, None)) for i in self._items ]
            value = "".join(strings)
            self._refs.append(value)
        except UndefinedVariableError as e:
            self._allRefs = False

    def contents(self):
        return self._items

    def allRefs(self):
        return self._allRefs

    def has_references(self):
        return len(self._refs) > 0

    def get_references(self):
        return self._refs

    def _resolve(self, ref, context):
        path = DictPath(self._delimiter, ref)
        try:
            return path.get_value(context)
        except KeyError as e:
            raise UndefinedVariableError(ref)

    def render(self, context, exports):
        if len(self._items) == 1:
            return self._resolve(self._items[0].render(context, exports), context)
        strings = [ str(i.render(context, exports)) for i in self._items ]
        return self._resolve("".join(strings), context)

    def __repr__(self):
        return 'RefItem(%r)' % self._items
