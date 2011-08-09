#! /usr/bin/env python
import sys, screed, re

for record in screed.open(sys.argv[1]):
   name = record.name
   sequence = record.sequence
   qual = record.accuracy

   C9plus = re.compile ('CCCCCCCCC+')
   for match in C9plus.finditer(sequence):
      start_match = match.start()
      end_qual = start_match + 8
      print end_qual
      print "%s: %s-%s" % ('Match HERE', start_match, match.end())
      print qual
      print qual[0:end_qual] + qual[match.end():]
   sequence = C9plus.sub('CCCCCCCC', sequence)

   G9plus = re.compile ('GGGGGGGGG+')
   sequence = G9plus.sub('GGGGGGGG', sequence)

   print '@%s\n%s\n+\n%s' % (name, sequence, qual)
