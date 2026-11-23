# Boolean Parsing

## Entry Point

Boolean dispatch calls `BooleanParser`, which:

1. converts the input bytes to lowercase;
2. removes surrounding whitespace;
3. checks the true translation set;
4. checks the false translation set;
5. returns `None` when neither set contains the value.

## True Values

`BOOLEAN_TRANSLATION_MAP.TRUE` includes values such as `yes`, `y`, `true`,
`t`, `on`, `enabled`, `1`, and `ofc`, plus selected multilingual values.

## False Values

`BOOLEAN_TRANSLATION_MAP.FALSE` includes common values such as `no`, `n`,
`false`, `f`, `off`, `0`, `disabled`, and `negative`, plus selected phrases
and multilingual values.

## Unknown Values

Unknown boolean values return `None`; `_ipBooleanParser`/`BooleanParser` does
not raise for an unrecognized spelling. This makes the parser explicit rather
than defaulting unknown input to false.

## Reference and Source Comments

The false set contains a source comment that attributes an expanded collection
of phrases to a LinkedIn article titled "99 ways to say No". The README
preserves this attribution.

The implementation also contains original and modified phrases. Maintain
differences between exact source phrases, project additions, and typos exactly
unless behavior is intentionally changed and tested.

## Broad-Effect Risk

Boolean parsing is shared by all loader APIs through `TypeLibraryDispatch`.
Adding or removing an exact translation changes `loads`, `loadsarray`, and
`loadsiter` results. Tests should cover true, false, whitespace, case
normalization, unknown, and selected multilingual or phrase cases.
