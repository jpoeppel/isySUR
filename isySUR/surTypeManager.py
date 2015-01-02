# -*- coding: utf-8 -*-
"""
Created on Wed Dec 31 16:44:31 2014
Helper class that leads known sur types (indoor, outdoor, both) from a file and
can be queried for a certain rule.
@author: jpoeppel
"""

class surTypeManager():
  
  def __init__(self, configPath):
    """
      Constructor for the type manager. Parses the given config file.
      
      @param configPath: Path to the config file that is to be used.
      @type configPath: String
    """
    self.ruleTypes = {}
    self._parseConfig(configPath)
    
    
  def _parseConfig(self, configPath):
    """
      Private function to parse the given config file. Reads the config file and stores all lines
      in the dictionary with their respective type.
      
      @param configPath: Path to the config file that is to be used.
      @type configPath: String
    """
    configFile = open(configPath, 'r')
    curType = "IO"
    for line in configFile.readlines():
      line = line.rstrip('\n')
      if line == "[Indoor]":
        curType = "I"
      elif line == "[Outdoor]":
        curType = "O"
      elif line == "[Both]":
        curType = "IO"
      else:
        self.ruleTypes[line] = curType
      
    
  def getSURType(self, ruleString):
    """
      Function to query the surType for a given rule. Returns the classification ("I","O","IO") of the sur.
      If the given ruleString was not found in the config IO is returned.
      
      @param ruleString: String of the rule name, e.g. "animal_feeding=\"no\"".
      @type ruleString: String
      
      @return: Sur classification ("I","O","IO")
      @rtype: String
    """
    if self.ruleTypes.has_key(ruleString):
      return self.ruleTypes[ruleString]
    else:
      return 'IO'