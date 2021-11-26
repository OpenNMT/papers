from __future__ import print_function

import argparse
import os
import sys

parser = argparse.ArgumentParser()
parser.add_argument('-vmap', required=True,
                    help="a vocab mapping file")
parser.add_argument('-tv',
                    help="target vocabulary file")
parser.add_argument('-src', required=True,
                    help="source file")
parser.add_argument('-tgt', required=True,
                    help="target file")

args = parser.parse_args()

mapping = dict()
lmax = -1
e_count = 0
with open(args.vmap) as f:
    for l in f:
        e_count += 1
        (src,tgt) = l.split('\t')
        lsrc = src.split(' ')
        if src == "":
            lsrc = []
        l = len(lsrc)
        if l not in mapping:
            mapping[l] = dict()
            if l > lmax:
                lmax = l
        mapping[l][src] = set()
        for e in tgt.split(' '):
            mapping[l][src].add(e)

sys.stderr.write("read mapping - %d entries (max length %d)\n" % (e_count, lmax))

tvocab = set()
if args.tv:
    with open(args.tv) as f:
        for v in f:
            tvocab.add(v.strip())
        sys.stderr.write("target vocabulary %d\n" % len(tvocab))

fsrc = open(args.src)
ftgt = open(args.tgt)

count = 0
c_total = 0
c_miss = 0
c_miss_tvocab = 0
misses = dict()
svocab = 0
while True:
    src = fsrc.readline().strip()
    tgt = ftgt.readline().strip()
    if not src:
        break
    count += 1
    lsrc = src.split(' ')
    vocab = set(mapping[0][""])
    for i in range(len(lsrc)):
        for j in range(i+1, len(lsrc)+1):
            seq = ' '.join(lsrc[i:j])
            if j-i >= lmax:
                break
            if seq in mapping[j-i]:
                vocab = vocab.union(mapping[j-i][seq])
    ltgt = tgt.split(' ')
    c_total += len(ltgt)
    for v in ltgt:
        if v not in vocab:
            if v not in misses:
                misses[v] = 1
            else:
                misses[v] += 1
            c_miss += 1
        if v not in tvocab:
            c_miss_tvocab += 1
    svocab += len(vocab)

sys.stderr.write("voc_mapping misses %d/%d (%.2f%%) on %d lines\n" % (c_miss, c_total, int(c_miss*10000./c_total)/100, count))
if args.tv:
    sys.stderr.write("oracle misses %d/%d (%.2f%%)\n" % (c_miss_tvocab, c_total, int(c_miss_tvocab*10000./c_total)/100))
sys.stderr.write("#vocab/sentences %.2f\n" % (int(svocab*10.0/count)/10))
for v in misses:
    print(v, misses[v])
