#!/usr/bin/env python3
# Local Imports =============|
from ovl.utils.__internals import InternalPlumbing, Eval, TypeLibraryDispatch, Path, Any, Generator, Iterator

# Exports ===================|
__all__ = ["loads", "loadsarray", "loadsiter"]
    
# Exported Functions  ======================================|
def loads(o:str|Path, /, freeze:bool=True) -> frozendict[str,Any]|dict[str,Any]: #type:ignore
    _ret = {}
    for _type, _name, _class, _data in InternalPlumbing(o):
        _ret.setdefault(_class, dict()) #type:ignore
        _ret[_class][_name] = Eval(*TypeLibraryDispatch(_type), _data)
    else:
        if '' in _ret: _ret.update(_ret.pop('')) #type:ignore
    return frozendict(_ret) if freeze else _ret #type:ignore

def loadsiter(o:str|Path, /, keys:bool=True, freeze:bool=False) -> Generator[Any]|Iterator[Any]:
    return (iter if freeze else lambda x:x)((_class, _name, Eval(*TypeLibraryDispatch(_type), _data)) if keys else Eval(*TypeLibraryDispatch(_type), _data) for _type, _name, _class, _data in InternalPlumbing(o)) #type:ignore

def loadsarray(o:str|Path, /, freeze:bool=True) -> tuple[Any]|list[Any]:
    return (tuple if freeze else list)(Eval(*TypeLibraryDispatch(_type), _data) for _type, *_, _data in InternalPlumbing(o))