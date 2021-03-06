# -*- coding: utf-8 -*-
"""
Created on Thu Nov  6 12:23:35 2014

@author: jpoeppel & adreyer
"""


import unittest
from isySUR import osmData
from isySUR import isyUtils

class TestNodeObject(unittest.TestCase):
  
  def setUp(self):
    isyUtils._relativeNullPoint=(0.0,0.0)
    self.id = "0001"
    self.lat = 0.1
    self.lon = 2.1
    self.tags = {"highway":"traffic_signals"}
    
  def test_getDistance(self):
    testNode = osmData.Node(self.id, self.lat, self.lon, self.tags)
    trueObj=osmData.distanceResult(141568.41351944,(testNode.id,testNode.__class__))
    result=testNode.getDistance((1.0,3.0))
    self.assertEqual(result.nearestObj,trueObj.nearestObj)
    self.assertEqual(result.distance,trueObj.distance)
    
  def test_getDistanceFail(self):
    testNode = osmData.Node(self.id, self.lat, self.lon, self.tags)
    with self.assertRaises(TypeError):
      testNode.getDistance("asd")
    
  def test_coords(self):
    testNode = osmData.Node(self.id, self.lat, self.lon, self.tags)
    trueValue=(0.1,2.1)
    self.assertEqual(testNode.coords,trueValue)
  
  def test_createNode(self):
    testNode = osmData.Node(self.id, self.lat, self.lon, self.tags)
    self.assertIsNotNone(testNode)
    self.assertEqual(testNode.id, self.id)
    self.assertEqual(testNode.lat, self.lat)
    self.assertEqual(testNode.lon, self.lon)
    self.assertEqual(testNode.tags, self.tags)
    
  def test_createNodeFailWrongFields(self):
    testNode = osmData.Node(self.id, self.lon, self.lat, self.tags)
    self.assertEqual(testNode.id, self.id)
    self.assertNotEqual(testNode.lat, self.lat)
    self.assertNotEqual(testNode.lon, self.lon)
    self.assertEqual(testNode.tags, self.tags)
    
  def test_createNodeWithIntId(self):
    testNode = osmData.Node(int(self.id), self.lat,self.lon,self.tags)
    self.assertNotEqual(testNode.id, self.id)
    self.assertEqual(testNode.id, int(self.id))
    
  def test_createNodeFailWrongLatType(self):
    with self.assertRaises(ValueError):
      testNode = osmData.Node(self.id, "0.1a", self.lon, self.tags)    
      
  def test_createNodeFailNotADictionary(self):
    with self.assertRaises(TypeError):
      testNode = osmData.Node(self.id, self.lat, self.lon, "a:b")
           
    
  def test_isNodeEqual(self):
    testNode = osmData.Node(self.id, self.lat, self.lon, self.tags)
    #Deliberatly not using the self variables to make sure it is filled with
    #other objects
    otherNode = osmData.Node("0001" , 0.1, 2.1, {"highway":"traffic_signals"})
    self.assertEqual(testNode, otherNode)
    
  def test_isNodeNotEqual(self):
    testNode = osmData.Node(self.id, self.lat, self.lon, self.tags)
    #Deliberatly not using the self variables to make sure it is filled with
    #other objects
    otherNode = osmData.Node("0002", 0.1, 2.1, {"highway":"traffic_signals"})
    self.assertNotEqual(testNode, otherNode)

  def test_getCoordinateString(self):
    testNode = osmData.Node(self.id, self.lat, self.lon, self.tags)
    testString = "%.8f,%.8f" %(self.lon, self.lat)
    self.assertEqual(testNode.getCoordinateString(), testString)

if __name__ == '__main__':
  unittest.main()
