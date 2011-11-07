#! /usr/bin/env python
import screed, sys, string

def is_pair(name1, annotations1, name2, annotations2):
    if '1:N:0:' in annotations1 and '2:N:0:' in annotations2:
        s1 = name1.split(' ')[0]
        s2 = name2.split(' ')[0]
        if s1 == s2:
            assert(s1)
            return True
    return False

infile = sys.argv[1]
outfile = infile.replace('R1_', '')
outfile = outfile.replace('fq', 'fa')
outfile = outfile.replace('.gz', '')
reads = screed.open(infile)

num_args = len(sys.argv)

if num_args == 1:
  print('You\'ll need some read sequences files for this.')
  exit()
elif num_args == 2:
  try:
    reads = screed.open(sys.argv[1])
  except:
    print('argument doesn\'t appear to be an existing fasta/q filepath')
    exit()
else: 
  try:
    reads_f1 = screed.open(sys.argv[1])
    reads_f2 = screed.open(sys.argv[2])
  except:
    print('An argument doesn\'t appear to be an existing fasta/q filepath')
    exit()
  def alternate():
    for n in reads_f1:
      yield(n)
      yield(reads_f2.next())
  reads = alternate()

single_fp = open(outfile + '.se', 'w')
paired_fp = open(outfile + '.pe', 'w')

last_record = None
last_name = None
last_annotations = None
for record in reads:
    name = record['name'].split()[0]
    annotations = record['annotations']
    sequence = record['sequence']

    if last_record:
        if is_pair(last_name, last_annotations, name, annotations):
           print >>paired_fp, '>%s\n%s' % (last_name, last_record['sequence'])
           print >>paired_fp, '>%s\n%s' % (name, record['sequence'])
           name, annotations, record = None, None, None
        else:
           print >>single_fp, '>%s\n%s' % (last_name, last_record['sequence'])

    last_name = name
    last_annotations = annotations
    last_record = record

if last_record:
    if is_pair(last_name, last_annotations, name, annotations):
        print >>paired_fp, '>%s\n%s' % (last_name, last_record['sequence'])
        print >>paired_fp, '>%s\n%s' % (name, record['sequence'])
        name, annotations, record = None, None, None
    else:
        print >>single_fp, '>%s\n%s' % (last_name, last_record['sequence'])
        name, annotations, record = None, None, None

if record:
   print >>single_fp, '>%s\n%s' % (name, record['sequence'])

single_fp.close()
paired_fp.close()

### check, at the end, to see if it worked!
paired_fp = open(outfile + '.pe')
if not paired_fp.read(1):
    raise Exception("no paired reads!? check file formats...")
