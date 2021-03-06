# -*- coding: utf-8 -*-
"""
Created on Sat Jan 10 11:41:33 2015

@author: jpoeppel
"""

import sys
import os
import isySUR.kmlData as kml

if __name__ == "__main__":
  if len(sys.argv) < 3:
    print "Usage: %s <ReferenceDirectory> <TestDirectory>" % sys.argv[0]
    sys.exit(1)
    
  refDir = sys.argv[1]
  testDir = sys.argv[2]
  incorrectFiles = []
  for f in os.listdir(refDir):
    
    print "Checking file:", f
    refKML = kml.KMLObject.parseKML(refDir + os.sep + f)
    
    testKML = kml.KMLObject.parseKML(testDir + os.sep + f)
    different = False
    
    if len(refKML.placemarks) != len(testKML.placemarks):
      different = True
    else:
      for i in range(len(refKML.placemarks)):
        if not different:
          if len(refKML.placemarks[i].polygon) != len(testKML.placemarks[i].polygon):
            different = True
          else:
            for j in range(len(refKML.placemarks[i].polygon)):
              if refKML.placemarks[i].polygon[j] != testKML.placemarks[i].polygon[j]:
                different = True
                break
    
    if different:      
      incorrectFiles.append(f)
      
  print "Unequal files: ", incorrectFiles