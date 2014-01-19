# coding=utf-8
'''
Created on 16 jan 2014

@author: PC
'''
from html import HTMLwriter
from search import performSearch

def main():
    writer = HTMLwriter()
    writer.startBasicPage()
    performSearch('Baskervilles hund', writer)
#    performSearch('gris', writer)
    writer.closeBasicPage()

if __name__ == "__main__":
    main()
