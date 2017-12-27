# -*- coding: utf-8 -*-

class DocsisDevice:
    """Represents the avalaible  Docsis Devices ids
    """
    __idCmts="Cmts"
    __idCm="Cm"
    __idCmInCmts="CmInCmts"
    
    def cmts(): return DocsisDevice.__idCmts
    
    def cm(): return DocsisDevice.__idCm
    
    def cmInCmts(): return DocsisDevice.__idCmInCmts
    