#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# encoding: utf-8

"""
plg2dot.py

(C) 2011-2012 by Damir Cavar (http://cavar.me/damir/)

All rights reserved.

Converts XFST Prolog files to DOT.

For XFST see: http://www.fmsbook.com/
For Graphviz and DOT see: http://www.graphviz.org/

Required:
You will need to generate a prolog file of your FST using XFST.
See the XFST manual for instructions how to do that.

Usage:
Assume your generated prolog file is stored as mymorph.plg.
Use the following command line to convert it to DOT:

./plg2dot.py mymorph.plg > mymorph.dot

The DOT output in this command is redirected to the file mymorph.dot.

On Windows machines, or in case the plg2dot.py file is not set
to be executable, you might need to prepend the python3 command.
"""


import sys, codecs, re
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

networkname = re.compile(r"network\((?P<netlabel>.+)\)\.")
arcdef = re.compile(r"arc\((?P<netlabel>.+),\s+(?P<from>.+),\s+(?P<to>.+),\s+\"(?P<label>[\w+-]+)\"(:\"(?P<label2>\w+)\")?\)\.")
finaldef = re.compile(r"final\((?P<netlabel>.+),\s+(?P<state>.+)\)\.")


class Graph:
   label = ""
   finalstates = []
   transitions = []

   def getDOT(self):
      finals = set(self.finalstates)
      states = set()
      for i in self.transitions:
         states.add(i[0])
         states.add(i[1])
      tmp = ""
      for i in self.transitions:
         tmp = tmp + " ".join( ("\t", str(i[0]), "->", str(i[1]), "[label=\"" + i[2] + "\"];\n") )
      return " ".join( ("digraph", self.label, "{\n") ) + "\trankdir=LR;\n\tsize=\"8,5\";\n" + \
         "\tnode [shape = doublecircle]\n" + "\t\t" + " ".join(finals) + " ;\n\n" + \
         "\tnode [shape = circle]\n" + "\t\t" + " ".join(states.difference(set(self.finalstates))) + ";\n\n" + \
         "\tnull [shape = plaintext label=\"\"];\n\tnull -> 0;\n\n" + tmp + "}\n"


def main(files):
   for i in files:
      try:
         ifp = open(i, mode="r", encoding="utf-8")
         myGraph = Graph()
         for line in ifp:
            mo = arcdef.match(line)
            if mo:
               if mo.group("label2"):
                  label = mo.group("label") + ":" + mo.group("label2")
               else:
                  label = mo.group("label")
               myGraph.transitions.append( (mo.group("from"), mo.group("to"), label) )
               continue
            mo = finaldef.match(line)
            if mo:
               myGraph.finalstates.append(mo.group("state"))
               continue
            mo = networkname.match(line)
            if mo:
               myGraph.label = mo.group("netlabel")
         ifp.close()
         print(myGraph.getDOT())
      except IOError as e:
         sys.exit("File " + i + " IO error:" + str(e))


if __name__ == '__main__':
   main(sys.argv[1:])
