#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 22 18:36:46 2014
Main entrance point for the informatiCup program.
Name should change once a final name for the program has been found.
@author: adreyer & jpoeppel
"""

import isySUR.program
import os
import argparse
import sys

def parseArguments():
  parser = argparse.ArgumentParser(description='isySUR script to calculate \
    the subjective area of influence of space usage rules (SURs).')
  subparsers = parser.add_subparsers(title='Version',
                                     description='Please choose whether to \
                                       start with or without GUI.')
  parser_gui = subparsers.add_parser('gui', help='Start with GUI.')
  parser_gui.set_defaults(func=gui)
  parser_cli = subparsers.add_parser('cli', help='Start with command-line interface.')
  parser_cli.set_defaults(func=cli)
  parser_cli.add_argument('input', type=str,
                        help='Input file containing the SURs which area of influence is to be computed.')
  parser_cli.add_argument('output', type=str,
                        help='Path for the resulting KML(s). If the path points to a file, only one KML \
                          file will be created, containing all calculated areas. If path points to a directory \
                          a KML file for each SUR will be created as well as one containing all areas.')
  parser_cli.add_argument('-c','--config', type=str, default='',
                        help='Path to config file for SUR classification (indoor, outdoor, both).')
  return parser.parse_args()
  
def gui(args):
  try:
    sys.argv = ['']
    print 1
    import isySUR.gui.MapGUI as gui
    print 2
    if "linux" in sys.platform:
      gui.MapApp().run()
      print 3
    elif "win" in sys.platform:
      try:
        gui.MapApp().run()
      except:
        if args.kivy == '':
          raise Exception('Unknown location of kivy.bat!')        
        os.system(args.kivy + " ./isySUR/gui/MapGUI.py")
  except:
    print "GUI could not be loaded. Is kivy installed correctly?"
  
def cli(args):
  isySUR.program.Pipeline().computeKMLsAndStore(args.input, args.output, args.config)

if __name__ == '__main__':
  args = parseArguments()
  args.func(args)