from pathlib import Path
from re import compile, Pattern, split
from typing import Literal, Generator, Any, Iterable, Callable, Iterator #type:ignore
import os
# Global Constants ===========|
ACCEPTED_OVL_SUFFIXES = (".ovl", ".conf")
META_REGEXP = compile(rb"^\w+\][ \t]{1,3}[\w]+ {0,3}(\$ ?[\w]+(?: ?\.[\w]+)*)? {0,3}:[\s]{0,3}")
class BOOLEAN_TRANSLATION_MAP:
    FALSE = {
            b'no', b'false', b'f', b'n',
            b'nah', b'nuh-uh', b'heck nah',
            b'spicy beans', b'moi? je refuse.',
            b'nope', b'no way', b'negative', b'0', b'off', b'non', b'disabled',
            'нет'.encode(), 'н'.encode(), b'nay',
            b'non', 'ложь'.encode(), 'л'.encode(),
            b'faux', b'falsch', b'nein', b'aus', b'a',
            b'hors', b'h', 'выключен'.encode(),
            'в'.encode(), 
            #Starting from here, these are quotes from '99 ways to say No' (https://www.linkedin.com/pulse/20130501190655-52397036-100-ways-to-say-no)
            b'not now.', b'look! squirrel!',
            b'my word of the day is rest, so i can\'t fit another thing in.'
            b'nope.', b'no thanks, i won\' be able to make it.',
            b'not this time.', b'heck no.', 'no way, josé'.encode(), #Modified
            b'no way, jose', #Original
            b'regrettably, i\'m not able to.', b'it\'s that time of the year when I must say no.', b'it\'s a wednesday. i have a "no on wednesday" policy.',
            b'ask me in a year.', b'i know someone that might be a fit for that. i\'ll email you their information.',
            b'you\'re so kind to think of me, but i can\'t.', b'maybe another time.',
            b'sounds great, but i can\'t commit.', b'rats! would\'ve loved to.', b'i\'m slammed.',
            b'perhaps next seaon when things clear up.', b'i\'m at the end of my rope right now so have to take a raincheck.',
            b'if only it worked.', b'i\'ll need to bow out.', b'i\'m going to have to exert my no muscle on this one.',
            b'i\'m taking some time.', b'thanks for thinking of me, but i can\'t.', b'i\'m in a season of no.',
            b'i\'m not the girl for you on this one.', # Original.
            b'i\'m not the man for you on this one.', # Counterpart.
            b'i ain\'t got your back on this one.', # Inclusive?
            b'i\'m resting right now.', b'i\'m not sure i\'m the best for it.', b'no thank you, but it sounds lovely.',
            b'it sounds like you\'re looking for something i\'m not able to give right now.', b'i believe i wouldn\'t fit the bill, sorry.',
            b'it\'s not a good idea for me.', b'not now.', b'i\'m trying to cut back.',
            b'i won\'t be able to help.', b'if only i had a clone!',
            b'i\'m not able to set aside the time needed.', b'i won\'t be able to dedicate the time i need to it.',
            b'i\'m head-down right now on a project, so won\'t be able to.', b'i wish there were two of me!',
            b'i\'m honored, but can\'t.'
            b'nononononono', b'i\'m booked into something else.', b'i\'m not able to make that time.',
            b'thanks, but no thanks.', b'i\'m not able to make it this week', #option one.
            b'i\'m not able to make it this month', b'i\'m not able to make it this year', #option 2, 3
            b'bye now.', b'i\'ve got too much on my plate right now.', b'i\'m not taking on anything else right now.',
            b'bandwith is low, so i won\'t be able to make it work.', b'i wish i could make it work.',
            b'not possible.' b'i wish i were able to.', b'if only i could!', b'i\'d love to -- but can\'t.',
            b'darn! not able to fit it in.', b'nah.', b'no thanks, i have another commitment.', 
            b'unfortunately, it\'s not a good time.', b'sadly i have something else.', b'unfortunately not.',
            b'i have something else. sorry.', b'apologies, but i can\'t make it.',
            b'thank you so much for asking, can you keep me on your list for next year?',
            b'i\'m flattered you considered me, but unfortunately i\'ll have to pass this time.',
            b'oh i wish i could help but you know, i bet claire could help you with that.', # Empathies extended to whosoever this poor soul named Claire was.
            b'no, sorry, that\'s not really me thing.', b'can i get back to you on that?', b'ew.',
            b'no, i\'d rather you didn\'t, but thanks anyway', b'i can\'t make it work.', b'it just won\'t fit right now.',
            b'i\'m really buckling down on my priorities right now, so i can\'t.',
            b'no say i.', b'what\'s the compensation?', b'how much are you willing to pay?', #option one
            b'how much are you able to pay?', # Better option.
            b'ick.', b'are you able to better that offer?', b'sorry, no can do.', b'i only say yes to very select opportunities, and unfortunately this doesn\'t meet my criteria.',
            b'the demands would be too much for me.', b'it\'s not feasible for me to take this on.',
            b'i wish i had all the time in the world.', b'my body double can.', b'in another runtime', # originally said 'life'.
            b'i cry, but decline.', b'my advisors won\'t agree to it.', b'my body says yes, but my heart say no.',
            b'i\'m not the person you\'re looking for.', b'these aren\'t the droids you\'re looking for.', # That last one was from StarWars.
            b'i don\'t have an iota of bandwidth left in my brain.', b'if only.', b'n to the o.', b'no.'
            }
    TRUE = {
        b'yes', b'cool beans', b'y', b'enabled', b'yea', b'yay', b'moi? j\'eccepte.', b'oui', b'ouais', b'1', b'i',
        b'on', 'allumé'.encode(), b'true', b't', b'ofc', b'mhm', b'ok', b'ja', "да".encode(), "Правда".encode(), "П".encode(), "д".encode()
    }

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
    assert _ihAssert(o)
    with open(o, 'rb') as Source: 
        for line in Source: yield line

def _ihBlobber(stream:Generator[bytes], /) -> Generator[bytes]:
    """Cleans up the blobbing from the `_ihGenerateSrc`."""
    BUF = bytearray()
    for chunk in stream:
        if META_REGEXP.match(chunk) and META_REGEXP.match(BUF): yield bytes(BUF); del BUF[:] #Necessary not to feed junk
        elif chunk.startswith(b'...'): continue
        BUF.extend(chunk)
    else:
        if META_REGEXP.match(BUF): yield bytes(BUF); del BUF[:] #Necessary to ensure no junk

def _ihMeta(stream:Generator[bytes], /) -> Generator[tuple[bytes, bytes, bytes, bytes]]:
    for blob in stream:
        _meta, _blob = split(rb" ?:[\s]{0,3}", blob.rstrip(b'\r\n'), maxsplit=1)
        _type, _meta = split(rb"\][ \t]{1,3}", _meta, maxsplit=1)
        _name, *_class = split(rb" {0,3}\$ ?", _meta, maxsplit=1)
        yield _type, _name, _class[0] if _class else b'', _blob

    

def _ipDeliminatedValueParserFactory(o: bytes) -> Callable[[bytes], Iterable[str|int]]:
    lDeliminator: Pattern[str] = compile('')
    match(o):
        case b'lsv': lDeliminator = compile(os.linesep)
        case b'wsv': lDeliminator = compile(r'\s')
        case b'csv': lDeliminator = compile(r',\s*')
        case b'tsv': lDeliminator = compile(r'\t')
        case _: raise ValueError(f"Unsupported delimiter type: {o.decode()}")
    def _iParser(x:bytes) -> Iterable[str|int]: 
        return [int(_) if _.isnumeric() else _ for _ in lDeliminator.split(x.decode())]
    return _iParser

def BooleanParser(o:bytes, /) -> bool|None:
    o = o.lower().strip()
    if o in BOOLEAN_TRANSLATION_MAP.TRUE: return True
    elif o in BOOLEAN_TRANSLATION_MAP.FALSE: return False
    else: return None # Necessary for explicitness.
        
# Internal Functions =========|
def InternalPlumbing(o: str|Path) -> Generator[tuple[bytes, bytes, bytes, bytes]]:
    SourceGenerator = _ihGenerateSrc(Path(o))
    BlobGenerator   = _ihBlobber(SourceGenerator)
    return _ihMeta(BlobGenerator)

def TypeLibraryDispatch(o:bytes, /) -> tuple[Callable[..., Any], bool]:
    """Maps the object type to a standard library, and the method used."""
    match(o.lower()):
        case b'html'|b'html5'|b'htm': return __import__('html5lib').parse, True
        case b'path': return  __import__('pathlib').Path, True #Pathlib is already imported.
        case b'url'| b'email'| b'card'| b'uuid' | b'iban': return  (lambda x: x if getattr(__import__('validators'), o.decode())(x) else None), True # type:ignore
        case b'ipv4'| b'ipv6': return  (lambda x: x if getattr(__import__('validators.ip_address'), o.decode())(x) else None), True #type:ignore
        case b'mac': return  (lambda x: x if __import__('validators').mac_address(x) else None), True # type:ignore
        case b'cusip' | b'isin' | b'sedol': return  getattr(__import__('validators.finance'), o.decode()), True
        case b'blob': return  bytes, False
        case b'json': return  __import__('json').loads, False
        case b'yaml': return  __import__('yaml').safe_load, False
        # case b'pckl'|b'pkl': return  __import__('pickle').loads, False
        case b'csv'|b'tsv'|b'wsv'|b'lsv': return  _ipDeliminatedValueParserFactory(o), False
        case b'md': return  __import__('markdown').markdown, True
        case b'int'|b'float': return  int if o == b'int' else float, True
        case b'cplx'|b'complex'|b'imag': return complex, True
        case b'bool': return  BooleanParser, False
        case b'date': return (lambda x: __import__('dateutil').parser.parse(x).date()), False #type:ignore
        case b'time': return (lambda x: __import__('dateutil').parser.parse(x).time()), False #type:ignore
        case b'datetime'|b'dt': return __import__('dateutil').parser.parse, False
        case b'toml': return __import__('tomllib').loads, True
        case _: return (lambda x: x.decode()), False #type:ignore

def Eval(library: Callable[[bytes|str], Any], toString: bool, data:bytes) -> Any:
    return library(data.decode() if toString else data)

def ClassFactory(Root: DictLike= {}):
    if not isinstance(Root, (dict)): raise TypeError(F"IncorrectDatatype: {type(Root)}") #type:ignore
    ClassCounterDatabase:dict[tuple[str], int] = {} #Intentionally Flat because this is a table.
    if isinstance(Root, frozendict): Root = dict(Root)
    Node = Root
    ClassPath: tuple[str] = '',
    def _lCounter(_cls: tuple[str]) -> int:
        ClassCounterDatabase.setdefault(_cls, -1)
        ClassCounterDatabase[_cls] += 1
        return (ClassCounterDatabase[_cls])
    def _lResolveClassPath(path:str) -> bool:
        """Exists incase I add more abhorent, whitespace relevant rules to the syntax, idk, like context or something."""
        nonlocal ClassPath
        _path:tuple[str] = *split(r' ?\.', path), #type:ignore
        if _path == ClassPath: return False
        elif _path[0]: ClassPath = _path
        else: ClassPath = '',
        return True
    def _lWalkObject() -> DictLike:
        """Recurses through the local `_Object` to get to a specific node. Returns the last legal node."""
        nonlocal Node, ClassPath, Root; Node=Root
        for subnode in ClassPath: 
            if subnode in Node: Node = Node[subnode]
            elif subnode: Node.setdefault(subnode, dict()); Node = Node[subnode] #type:ignore
        else: return Node
    def _lRegisterSubClass(_cls: str) -> None: 
        if not _lResolveClassPath(_cls): return
        _lWalkObject() #type:ignore
        
    def _lRegisterItemName(_name: bytes) -> str|int:
        nonlocal ClassPath; return _lCounter(ClassPath) if _name == b'nil' else _name.decode()
    def _lConstruct(o: Generator[tuple[bytes, bytes, bytes, bytes]]) -> Literal[True]:
        nonlocal Node
        for _type, _name, _class, _data in o:
            _lRegisterSubClass(_class.decode())
            Node[_lRegisterItemName(_name)] = Eval(*TypeLibraryDispatch(_type), _data) #type:ignore
        return True
    return Root, _lConstruct
