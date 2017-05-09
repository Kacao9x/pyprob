# automatically generated by the FlatBuffers compiler, do not modify

# namespace: protocol

import flatbuffers

class ObservesInitRequest(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsObservesInitRequest(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = ObservesInitRequest()
        x.Init(buf, n + offset)
        return x

    # ObservesInitRequest
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # ObservesInitRequest
    def Observes(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            x = self._tab.Indirect(o + self._tab.Pos)
            from .NDArray import NDArray
            obj = NDArray()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

def ObservesInitRequestStart(builder): builder.StartObject(1)
def ObservesInitRequestAddObserves(builder, observes): builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(observes), 0)
def ObservesInitRequestEnd(builder): return builder.EndObject()