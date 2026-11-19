import pathlib, re, typing; RegExp, _AcceptedOVLSuffixs, __all__ = re.compile(r"^\w+\]\s[\w]+((?:\.[\w]+)*(\$(?:\.[\w]+)*)?):\s"), ['.ovl'], ['loads', 'loadsarray']
def _iAssertPath(o:pathlib.Path, /) -> None: assert (o.is_file() and o.suffix in _AcceptedOVLSuffixs), "File failed to meet 'Qualified' Criteria"
def loads(o:str|pathlib.Path, /, frozen:bool=True) -> frozendict[typing.Any, typing.Any]|dict[typing.Any,typing.Any]:
    _iAssertPath(pathlib.Path(o));_ret, _ln = {}, 1, #type:ignore
    with open(o, 'r') as SrcFile:
        for line in SrcFile:
            if not line.startswith('...'): _type, _name, _class, _line = (((_name_class := (_meta_line := line.split(': ', 1))[0].split('] ', 1))[0], *(_name_class[1].split('$',1)), _meta_line[1].rstrip()) if RegExp.match(line) else (_:=''), _ln, _, line); _ret.setdefault(_class, dict()); _ret[_class][_name] = _iEval(_type, _line) #type:ignore
        else: _ret.update(_ret['']); del _ret[''] #type:ignore
        return frozendict(_ret) if frozen else _ret #type:ignore
def loadsarray(o:str|pathlib.Path, /, frozen:bool=True) -> tuple[typing.Any]|list[typing.Any]:
    _iAssertPath(pathlib.Path(o))
    values:list[typing.Any] = []
    with open(o, 'r') as SrcFile:
        for line in SrcFile:
            if line.startswith('...'):
                continue
            if RegExp.match(line):
                metadata, value = line.split(': ', 1)
                value_type, _ = metadata.split('] ', 1)
                values.append(_iEval(value_type, value.rstrip()))
            else:
                values.append(line.rstrip())
    return tuple(values) if frozen else values
def _iEval(_type: str, _line: str) -> typing.Any:
    match(_type):
        case "html":  import html5lib; return html5lib.parse(_line) #type:ignore
        case "json" | "pckl" | "yaml": __import__(_type := "pickle" if _type == "pickle" else _type); return (eval(_type)).loads(_line.encode()) #type:ignore
        case "md": import markdown; return markdown.markdown(_line)
        case "path": return pathlib.Path(_line)
        case "url" | "email" | "card" | "uuid" | "mac" | "ipv4" | "ipv6" | "iban" | "host" | "cusip": import validators; return _line if eval(f"validators.{"finance" if _type == "cusip" else ("mac_address" if _type == "mac"  else ( f"ip_adress.{_type}" if _type.startswith('ip') else ("hostname" if _type == "host" else _type)))}")(_line) else None #type:ignore
        case "blob": return _line.encode()
        case "csv" | "tsv": return [_val.strip() for _val in _line.split(',' if _type == "csv" else '\t')]
        case "int" | "float" | "complex" | "cplx": return eval('complex' if _type == "cplx" else _type)(_line)
        case "date" | "time" | "dt" | "datetime": from dateutil import parser; _type = ('' if _type in {"dt", "datetime"} else f'.{_type}()'); return eval(f'parser.parse(_line){_type}') #type:ignore
        case "bool": from boolean_parser import parse; return parse(_line) #type:ignore
        case _: return None if _type == 'nil' else _line