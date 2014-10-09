from rpython.translator import cdir
from rpython.rtyper.lltypesystem import rffi
from rpython.translator.tool.cbuild import ExternalCompilationInfo


compilation_info = ExternalCompilationInfo(
    includes=["readline/readline.h"],
    libraries=["readline"]
)


def llexternal(*args, **kwargs):
    return rffi.llexternal(*args, compilation_info=compilation_info, **kwargs)


_readline = llexternal("readline", [rffi.CCHARP], rffi.CCHARP)


def readline(prompt):
    return unicode(rffi.charp2str(_readline(rffi.str2charp(prompt))))
