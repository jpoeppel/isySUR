# -*- coding: utf-8 -*-
"""
Created on Thu Nov  6 11:47:29 2014

@author: jhemming & tschodde
"""

import unittest
from isySUR import osmAPI
from isySUR import osmData
import xml.dom.minidom as dom
import xml.etree.cElementTree as ET
import os

class TestOsmAPI(unittest.TestCase):
  def setUp(self):
    self.osmAPIobj=osmAPI.osmAPI()
    self.boundingBox = [52.032736,8.486593,52.042113,8.501194]
    self.osmDataFilename = "testData/dataOnlyForTests/test.xml"

    self.testXMLString = "<relation id='152483'>"\
                         "<nd ref='43682400'/>"\
                         "<nd ref='260441217'/>"\
                         "<member type='way' ref='17958713' role='inner'/>"\
                         "<member type='way' ref='17958715' role='outer'/>"\
                         "<tag k='leisure' v='pitch'/>"\
                         "<tag k='type' v='multipolygon'/>"\
                         "</relation>"
    self.testNode = ET.fromstring(self.testXMLString)
    
    self.testOsmObj = osmData.OSM()
    self.testOsmObj.addNode(osmData.Node("146891366", 52.0364239, 8.4867570,
                                         {"crossing":"traffic_signals","highway":"traffic_signals"}))
    self.testOsmObj.addNode(osmData.Node("46426098", 52.0375177, 8.4995645, {}))
    self.testOsmObj.addNode(osmData.Node("46426114", 52.0386730, 8.4981747, {}))
    self.testOsmObj.addWay(osmData.Way("46480681", ["593900008", "416938583"],
                                       {"bicycle":"yes","highway":"footway"}, self.testOsmObj))
    self.testOsmObj.addRelation(osmData.Relation("152923",
                                                 [("way","35221623","outer")],
                                                 {"natural":"scrub","type":"multipolygon"}, self.testOsmObj))
    self.testOsmObj.addRelation(osmData.Relation("905522",
                                                 [("way","26582813","outer"),(
                                                  "way","20213971","inner")],{"type":"multipolygon"}, self.testOsmObj))
  
  def test_performRequestWithWildcard(self):
    bBox = [50.92615995855398,5.396102964878082,50.92663164856874,5.397061854600906]
    testData = self.osmAPIobj.performRequest(bBox,[("way",['"building"']),("relation",['"building"'])])
    self.assertEqual(len(testData.nodes),12)
    self.assertEqual(len(testData.ways),1)
    self.assertEqual(len(testData.relations),0)
    
  def test_getDataFromPoly(self):
    polyString = "50.9263254 5.3972612 50.9264940 5.3967052 50.9260380 5.3963340 "\
                  "50.9258307 5.3968185 50.9261209 5.3971911"
    testData = self.osmAPIobj.getDataFromPoly(polyString)
    self.assertEqual(len(testData.nodes),75)
    self.assertEqual(len(testData.ways),6)
    self.assertEqual(len(testData.relations),0)
  
  def test_getOsmRequestData(self):
    testObj=self.osmAPIobj._getOsmRequestData(self.boundingBox[0],
                                              self.boundingBox[1],
                                              self.boundingBox[2],
                                              self.boundingBox[3],
                                              [])
    self.assertIsNotNone(testObj)
    self.assertEqual(testObj.has_key('data'),True)
    self.assertEqual(testObj['data'],'[out:xml][timeout:35];'\
                     '(node[""=""](52.032736,8.486593,52.042113,8.501194);'\
                     'way[""=""](52.032736,8.486593,52.042113,8.501194);'\
                     'relation[""=""](52.032736,8.486593,52.042113,8.501194););(._;>>;); out body qt;')
    
    testObj2 = self.osmAPIobj._getOsmRequestData(self.boundingBox[0],
                                                 self.boundingBox[1],
                                                 self.boundingBox[2],
                                                 self.boundingBox[3],
                                                 filterList=[("node",
                                                  ['"amenity"="university"']),("way",
                                                  ['"amenity"="university"']),("relation",
                                                  ['"amenity"="university"','"building"!="true"'])])
    self.assertIsNotNone(testObj2)
    self.assertEqual(testObj2.has_key('data'),True)
    self.assertEqual(testObj2['data'],'[out:xml][timeout:35];'\
                     '(node["amenity"="university"](52.032736,8.486593,52.042113,8.501194);'\
                     'way["amenity"="university"](52.032736,8.486593,52.042113,8.501194);'\
                     'relation["amenity"="university"]["building"!="true"](52.032736,8.486593,52.042113,8.501194);'\
                     ');(._;>>;); out body qt;')
                     
    testObj3 = self.osmAPIobj._getOsmRequestData(self.boundingBox[0],
                                                 self.boundingBox[1],
                                                 self.boundingBox[2],
                                                 self.boundingBox[3],
                                                 filterList=[("node",
                                                  ['"building"']),("way",
                                                  ['"building"']),("relation",
                                                  ['"building"'])])
    self.assertIsNotNone(testObj3)
    self.assertEqual(testObj3.has_key('data'),True)
    self.assertEqual(testObj3['data'],'[out:xml][timeout:35];'\
                     '(node["building"](52.032736,8.486593,52.042113,8.501194);'\
                     'way["building"](52.032736,8.486593,52.042113,8.501194);'\
                     'relation["building"](52.032736,8.486593,52.042113,8.501194);'\
                     ');(._;>>;); out body qt;')
   
  def test_parseData(self):
    
    testFile = open(self.osmDataFilename, "r").read()
    
    testDataObj = self.osmAPIobj._parseData(testFile)
    
    self.assertIsNotNone(testDataObj)
    self.assertIsNotNone(testDataObj.nodes)
    self.assertIsNotNone(testDataObj.ways)
    self.assertIsNotNone(testDataObj.relations)    

    self.assertEqual(self.testOsmObj, testDataObj)
   
  def test_getTags(self):
    tags = {"leisure":"pitch", "type":"multipolygon"}
    
    testTags = self.osmAPIobj._getTags(self.testNode)
    
    self.assertIsNotNone(testTags)
    self.assertEqual(tags, testTags)
  
  def test_getRefs(self):
    refs = ["43682400","260441217"]
    
    testRefs = self.osmAPIobj._getRefs(self.testNode)
    
    self.assertIsNotNone(testRefs)
    self.assertEqual(refs, testRefs)
  
  def test_getMembers(self):
    members = [("way", "17958713","inner"),("way","17958715", "outer")]
    
    testMembers = self.osmAPIobj._getMembers(self.testNode)
    
    self.assertIsNotNone(testMembers)
    self.assertEqual(members, testMembers)


if __name__ == '__main__':
  os.chdir("../..")
  unittest.main()