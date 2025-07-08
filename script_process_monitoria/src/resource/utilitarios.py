#!/usr/bin/python
# -*- coding: utf-8 -*-
import codecs

import re
import os

class Utils:

    def __init__(self):
        self.ptha_src = os.getcwd()

    def read_file(self, file):
        
        pathx = '/home/administrador/projetos/dados-agent-ia/script_process_monitoria/src/sql/'
        if re.findall(r'administrador', pathx):
            
 
            file = f'{pathx}{file}'
            
        else:
            file = f'/home/andre/projetogithub/dados-agent-ia/script_process_monitoria/src/sql/{file}'

        f=codecs.open(file, "r", 'utf-8')
        conteudo=f.readlines()
        strsql = ""

        for ln in conteudo:
            strsql += ln

        return strsql
                
    def read_file_win(self, file):
        
        
        file = f'C:\\Users\\abarbosa\\Documents\\projetos\\processos_sql_server\\src\\v1\\sql\\{file}'

        f=codecs.open(file, "r", 'utf-8')
        conteudo=f.readlines()
        strsql = ""
    
        for ln in conteudo:
            strsql += ln

        return strsql
