# coding=utf-8
'''
Created on 16 jan 2014

@author: PC
'''
"""
Debug the script. 

Run this module to debug the script locally. 

"""
from html import HTMLwriter
from search import performSearch

def main():
    writer = HTMLwriter()
    writer.startBasicPage()
    performSearch('Herman Melville', writer)
#    performSearch('gris', writer)
    writer.closeBasicPage()

if __name__ == "__main__":
    main()
