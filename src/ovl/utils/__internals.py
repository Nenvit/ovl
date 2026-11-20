from pathlib import Path
from re import compile as RegExp
from typing import Literal, Generator, Any, Iterator, Iterable, Callable #type:ignore
import os
# Global Constants ===========|
ACCEPTED_OVL_SUFFIXES = (".ovl", ".oval", ".oconf", ".ov", ".conf", ".ovlconf")
META_REGEXP = RegExp(rb"^\w+\]\s[\w]+(\$[\w]+(?:\.[\w]+)*)?:\s")

type DictLike = dict[str|int, Any]|frozendict[str|int, Any]

# Helper Functions ===========|
def _ihAssert(path: Path) -> Literal[True]:
    """Asserts the following assumptions of a given file:
    1. The Path Exists.
    2. The Path Points to a File.
    3. The Path ends with a valid OVL suffix.
    4. The Program has appropriate permissions to read the file.
    """
    if not path.exists(): raise FileNotFoundError(f"Path {path.absolute()} does not exist.")
    if not path.is_file(): raise IsADirectoryError(f"Path {path.absolute()} is not a file.")
    if not path.suffix.lower() in ACCEPTED_OVL_SUFFIXES: raise NotImplementedError(f"Unsupported file type ({path.suffix}).")
    if not os.access(path, os.R_OK): raise PermissionError(f"Permission denied to read file {path.absolute()}.")
    return True

def _ihGenerateSrc(o:Path, /) -> Generator[bytes]:
    """Especiallized function to read lines from an acceptable `.ovl` file."""
    _ihAssert(o)
    with open(o, 'rb') as Source: 
        return (line for line in Source)

def _ihBlobber(stream:Generator[bytes], /) -> Generator[bytes]:
    """Cleans up the blobbing from the `_ihGenerateSrc`."""
    BUF = bytearray()
    for chunk in stream:
        if META_REGEXP.match(chunk) and BUF: yield bytes(BUF); del BUF[:]
        elif chunk.startswith(b'...'): continue
        BUF.extend(chunk)
    else:
        if META_REGEXP.match(BUF): yield bytes(BUF); del BUF[:]

def _ihMeta(stream:Generator[bytes], /) -> Generator[tuple[bytes, bytes, bytes, bytes]]:
    for blob in stream:
        _meta, _blob = blob.split(b': ', 1)
        _type, _meta = _meta.split(b'] ', 1)
        _name, _class = _meta.split(b'$', 1)
        yield _type, _name, _class, _blob
        
# Internal Functions =========|
def InternalPlumbing(o: str|Path) -> Generator[tuple[bytes, bytes, bytes, bytes]]:
    SourceGenerator = _ihGenerateSrc(Path(o))
    BlobGenerator   = _ihBlobber(SourceGenerator)
    return _ihMeta(BlobGenerator)

def TypeLibraryDispatch(o:bytes, /) -> tuple[str|bytes, str|bytes]:
    """Maps the object type to a standard library, and the method used."""
    o = o.lower()
    match(o):
        case b'html'|b'html5'|b'htm': return 'html5lib', 'html5lib.parse(%s)'
        case b'path': return  'pathlib', b'pathlib.Path(%b)' #Pathlib is already imported.
        case b'url'| b'email'| b'card'| b'uuid' | b'iban': return  'validators', f'validators.{o.decode('utf-8')}(%s)'
        case b'ipv4'| b'ipv6': return  'validators', f'validators.ip_address.{o.decode('utf-8')}(%s)'
        case b'mac': return  'validators', 'validators.mac_address(%s)'
        case b'cusip' | b'isin' | b'sedol': return  'validators', f'validators.finance.{o.decode('utf-8')}(%s)'
        case b'blob': return  '', b'blob'
        case b'json': return  'json', b'json.loads(%b)'
        case b'yaml': return  'yaml', b'yaml.load(%b)'
        case b'pckl'|b'pkl': return  'pickle', b'pickle.loads(%b)'
        case b'csv'|b'tsv'|b'wsv': return  '', o
        case b'md': return  "markdown", "markdown.markdown(%s)"
        case b'int'|b'float': return  b'', o + b'(%b)'
        case b'cplx'|b'complex'|b'imag': return b'', b'complex(%b)'
        case b'bool': return  "boolean_parser", "boolean_parser.parse(%s)"
        case b'date': return  "dateutil.parser", b"dateutil.parser.parse(%b).date()"
        case b'datetime'|b'dt': return  "dateutil.parser", b"dateutil.parser.parse(%b)"
        case b'time': return  "dateutil.parser", b"dateutil.parser.parse(%b).time()"
        case b'toml': return 'tomllib', b'tomllib.parse(%b)'
        case _: return '', ''

def Eval(library: str|bytes, command: str|bytes, data:bytes) -> Any:
    if library and isinstance(library, str): 
        __import__(library)
        if isinstance(command, bytes): return eval(command % (data), globals(), locals())
        else: return eval(command % (data.decode('utf-8')), globals(), locals())
    elif isinstance(library, bytes): return eval(command % (data), globals(), locals())
    elif command:
        if command == b'blob': return data
        elif command == b'csv': return [_.strip().decode('utf-8') for _ in data.split(b',') if _]
        elif command == b'tsv': return [_.strip().decode('utf-8') for _ in data.split(b'\t') if _]
        else: return [_.strip().decode('utf-8') for _ in data.split(b' ') if _]
    else: return data.decode('utf-8')

def ClassFactory(Root: DictLike= {}):
    if not isinstance(Root, (dict)): raise TypeError(F"IncorrectDatatype: {type(Root)}") #type:ignore
    ClassCounterDatabase:DictLike = {} #Intentionally Flat because this is a table.
    Node = Root
    _LastClass = ''
    def _lCounter(_cls: str) -> int:
        ClassCounterDatabase.setdefault(_cls, -1)
        ClassCounterDatabase[_cls] += 1
        return (ClassCounterDatabase[_cls])
    def _lWalkObject(_cls:Iterable[str|int]) -> DictLike:
        """Recurses through the local `_Object` to get to a specific node. Returns the last legal node."""
        nonlocal Node; Node = Root
        for node in _cls: Node = Node.get(node, Node)
        else: return Node
    def _lRegisterSubClass(_cls: str) -> None: 
        nonlocal _LastClass
        if _cls == _LastClass: return
        _ = _cls.split('.')
        _lWalkObject(_).setdefault(_[-1], DictLike) #type:ignore
        _LastClass = _cls
    def _lRegisterItemName(_name: bytes) -> str|int:
        nonlocal _LastClass; return _lCounter(_LastClass) if _name == b'nil' else _name.decode()
    def _lConstruct(o: Generator[tuple[bytes, bytes, bytes, bytes]]) -> Literal[True]:
        nonlocal Node
        for _type, _name, _class, _data in o:
            _lRegisterSubClass(_class.decode())
            _name = _lRegisterItemName(_name)
            Node[_name] = _data
        return True
    return Root, _lConstruct
        