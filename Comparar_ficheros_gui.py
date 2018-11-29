# -*- coding: utf-8 -*-
"""
Created on Thu May 24 10:32:36 2018

@author: paulo.conceicao
"""

from PyQt5.QtWidgets import (QMainWindow, QTextEdit, 
    QAction, QFileDialog, QApplication)
from PyQt5.QtGui import QIcon
import sys
import os
import pandas as pd
import hashlib
import csv
import difflib
import time

class Import(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
        
    def initUI(self):      

        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)
        self.statusBar()

        openFile = QAction(QIcon('open.png'), 'Cargar fichero antiguo', self)
        openFile.setShortcut('Ctrl+A')
        openFile.setStatusTip('Selecciona ruta del fichero antiguo')
        openFile.triggered.connect(self.showDialog)
        
        openFile1 = QAction(QIcon('open.png'), 'Cargar fichero nuevo', self)
        openFile1.setShortcut('Ctrl+N')
        openFile1.setStatusTip('Selecciona ruta del fichero nuevo')
                
        exitAction = QAction("Salir",self) 
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Salir de la app')       
        exitAction.triggered.connect(self.close)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Menu')
        fileMenu.addAction(openFile) 
        fileMenu.addAction(openFile1) 
        fileMenu.addAction(exitAction)       

        x, y, w, h = 400, 400, 500, 350
        self.setGeometry(x, y, w, h)
        self.setWindowTitle('Comparar ficheros *.txt *.csv')
        
        self.show()

    def getold1(self):
        
#        old1, filter = QFileDialog.getOpenFileName(self, 'Seleccionar fichero antiguo', 'C:\\Data\\ficheros_resumen - copia\\', filter='*.txt *.csv')
        old1, filter = QFileDialog.getOpenFileName(self, 'Seleccionar fichero antiguo', 'W:\\', filter='*.txt *.csv')
        if old1:
            self.textEdit.setText('\nCargar ficheros... ')
#            self.textEdit.setText('\nFichero antiguo: ' + str(old1)) 
            self.old1 = old1 

    def getnew1(self):
        
#        new1, filter = QFileDialog.getOpenFileName(self, 'Seleccionar fichero nuevo', 'C:\\Data\\ficheros_resumen - copia\\', filter='*.txt *.csv')
        new1, filter = QFileDialog.getOpenFileName(self, 'Seleccionar fichero nuevo', 'W:\\', filter='*.txt *.csv')
        if new1:
#            self.textEdit.append('\nFichero nuevo: ' + str(new1)) 
            self.new1 = new1 
            
    def showDialog(self):

        self.getold1()
 
        self.getnew1()
        
        os.chdir(os.path.dirname(os.path.realpath(str(self.old1)))) 
        
        inicio = time.clock()
        
        def checksum(f):
            md5 = hashlib.md5()
            md5.update(open(f,"rb").read())
            return md5.hexdigest()
        
        def is_contents_same(f1, f2):
            return checksum(f1) == checksum(f2)

        no_igual = True
        try:        
            if not is_contents_same(self.old1, self.new1):
                self.textEdit.append('\n    Los ficheros no son iguales --> Identificar diferencias') 
                no_igual = True
            else:    
                self.textEdit.append('\n    Los ficheros son iguales!') 
                no_igual = False
        
        except Exception as e:
            self.statusBar().showMessage('Error en checksum: ' + str(e))

        if no_igual:
            try:
                oldx = csv.reader(open(self.old1, 'r', encoding="utf8"))
                old = []
                for row in oldx:
                    oldx =[row[0]]
                    old.append(oldx)
                old = pd.DataFrame(old)
                old.columns = ['col']
            except Exception as e:
                self.statusBar().showMessage('Error carga fichero antiguo: ' + str(e))
             
            self.textEdit.append('\nFichero antiguo: ' + str(self.old1))         
            self.textEdit.append(str(old.describe()))   
                 
            try:
                newx = csv.reader(open(self.new1, 'r', encoding="utf8"))
                new = []
                for row in newx:
                    newx =[row[0]]
                    new.append(newx)
                new = pd.DataFrame(new)
                new.columns = ['col']
            except Exception as e:
                self.statusBar().showMessage('Error carga fichero nuevo: ' + str(e))
                    
            self.textEdit.append('\nFichero nuevo: ' + str(self.new1))
            self.textEdit.append(str(new.describe()))         
    
            try:             
                old_new = pd.merge(old, new, how='outer', indicator=True).query('_merge != "both"')
                
                #pivot de la column col
                for x in old_new.col.unique():
                    old_new[x]=(old_new.col==x).astype(int)
                
                #reordenar las variables
                cols = old_new.columns.tolist()
                cols = cols[2:] + cols[:-(len(old_new.columns)-2)]
                old_new = old_new[cols]    
                
                list_=[]
                for i, item in enumerate(old_new['col']):
                    for j, item in enumerate(old_new['col']): 
                        old_new.iloc[i,j] = round(difflib.SequenceMatcher(lambda x: x == " ", old_new.columns[j], old_new.iloc[i,len(old_new.columns)-2] ).ratio(), 3)
                        
                        for opcode in difflib.SequenceMatcher(lambda x: x == " ", old_new.columns[j], old_new.iloc[i,len(old_new.columns)-2] ).get_opcodes():
                            if old_new.iloc[i,j] > 0.8 and old_new.iloc[i,j] < 1:
                                comparacion = [opcode,i,j]
                                list_.append(comparacion)
                
                comparacion = pd.DataFrame(list_)
                comparacion1 = comparacion.groupby([1,2])[0].apply(lambda x: ''.join(map(str,x))).reset_index(name=3)
                comparacion1[2] = comparacion1[2].map(str) + comparacion1[3]
                comparacion2 = comparacion1.groupby([1])[2].apply(lambda x: ''.join(map(str,x))).reset_index(name=3)
                old_new1 = old_new.reset_index()
                final = pd.merge(old_new1, comparacion2, how='left', left_index=True, right_on=1)
                final = final.rename(columns={1: 'indice', 3: 'posiciones'})
                final[list(range(1,len(final.at[0,'col'])+1))] = final['col'].apply(lambda x: pd.Series(list(x)))
            except Exception as e:
                self.statusBar().showMessage('Error a calcular: ' + str(e))
    
            try:               
                writer = pd.ExcelWriter('comparacion.xlsx', engine='xlsxwriter')                
                final.to_excel(writer, sheet_name='comparacion', startrow=0) 
            except Exception as e:
                self.statusBar().showMessage('Error a escribir fichero comparacion.xlsx: ' + str(e))
    
            self.textEdit.append('\nFichero "comparacion.xlsx" creado en la carpeta: ' + os.path.dirname(os.path.realpath(self.old1))) 

        fin=time.clock()
        tiempo = str(round((fin-inicio), 2))    
        self.statusBar().showMessage('Ejecución terminada em ' + tiempo + ' segundos')

def main():
    
    app = QApplication(sys.argv)
    ex = Import()
    ex.show()
    sys.exit(app.exec_())

#import profile
#profile.run('main()')    

if __name__ == '__main__':
    main()
