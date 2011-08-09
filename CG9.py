#! /usr/bin/env python
import sys, screed, re

for record in screed.open(sys.argv[1]):
   name = record.name
   sequence = record.sequence
   qual = record.accuracy

   C9plus = re.compile ('CCCCCCCCC+')
   sequence = C8plus.sub('CCCCCCCC', sequence)

   G9plus = re.compile ('GGGGGGGGG+')
   sequence = G8plus.sub('GGGGGGGG', sequence)

   print '@%s\n%s\n+\n%s' % (name, sequence, qual)
