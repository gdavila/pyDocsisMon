# -*- coding: utf-8 -*-

class DocsisDevice:
    """Represents the avalaible  Docsis Devices ids
    """
    __idCmts="Cmts"
    __idCm="Cm"
    __idCm31="Cm31"
    __idCmInCmts="CmInCmts"
    
    def cmts(): return DocsisDevice.__idCmts
    
    def cm(): return DocsisDevice.__idCm
    
    def cm31(): return DocsisDevice.__idCm31
    
    def cmInCmts(): return DocsisDevice.__idCmInCmts
    