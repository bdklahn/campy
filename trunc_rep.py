#! /usr/bin/env python
import sys, screed, re

# "rep" = "repeat"

rep_num = int(sys.argv[1])
rep_str = sys.argv[2]

trunc_rep = rep_str * rep_num

rep_pat_txt = trunc_rep + rep_str + '+'
rep_pat = re.compile (rep_pat_txt)

for record in screed.open(sys.argv[3]):
   name = record.name
   sequence = record.sequence
   qual = record.accuracy

   for match in rep_pat.finditer(sequence):
      qual_chop_end = match.start() + rep_num * len(rep_str)
      qual = qual[0:qual_chop_end] + qual[match.end():]

   sequence = rep_pat.sub(trunc_rep, sequence)

   print '@%s\n%s\n+\n%s' % (name, sequence, qual)
