#!/usr/bin/env python3
# Local Imports =============|
from ovl.utils.__internals import ClassFactory, InternalPlumbing, Eval, TypeLibraryDispatch, Path, Any, Generator, Iterator, DictLike

# Exports ===================|
__all__ = ["loads", "loadsarray", "loadsiter"]
    
# Exported Functions  ======================================|
def loads(o:str|Path, /, update:DictLike = {}, freeze:bool=True) -> DictLike: #type:ignore
    Root, Constructed = ClassFactory(dict(update))
    return frozendict(Root) if Constructed(InternalPlumbing(Path(o))) and freeze else Root #type:ignore

def loadsiter(o:str|Path, /, keys:bool=True, freeze:bool=False) -> Generator[Any]|Iterator[Any]:
    return (iter if freeze else lambda x:x)((_class, _name, Eval(*TypeLibraryDispatch(_type), _data)) if keys else Eval(*TypeLibraryDispatch(_type), _data) for _type, _name, _class, _data in InternalPlumbing(o)) #type:ignore

def loadsarray(o:str|Path, /, freeze:bool=True) -> tuple[Any]|list[Any]:
    return (tuple if freeze else list)(Eval(*TypeLibraryDispatch(_type), _data) for _type, *_, _data in InternalPlumbing(o))