#! /usr/bin/env python
import sys, screed, re

# "rep" = "repeat"

rep_num = int(sys.argv[1])
rep_str = str(sys.argv[2]).upper

trunc_rep = rep_str * rep_num
len_rep_str = len(rep_str)

rep_pat_txt = trunc_rep + rep_str + '+'
rep_pat = re.compile (rep_pat_txt)

for record in screed.open(sys.argv[3]):
   name = record.name
   sequence = record.sequence
   qual = record.accuracy

   shorter_by = 0
   for match in rep_pat.finditer(sequence):
      new_match_start = match.start() - shorter_by
      new_match_end = match.end() - shorter_by
      qual_chop_end = new_match_start + rep_num * len_rep_str
      qual = qual[0:qual_chop_end] + qual[new_match_end:]
      shorter_by = shorter_by + ( new_match_end - qual_chop_end )
   sequence = rep_pat.sub(trunc_rep, sequence)

   print '@%s\n%s\n+\n%s' % (name, sequence, qual)
