This repository contains tools for building and evaluating vocabulary maps used to predict and reduce the size of the target vocabulary during translation.

# File format

A vocabulary map file is a list of mapping "source ngram > target meanings". Each line represents such mapping with the format:

```
source ngram\tmeaning1 meaning2 meaning3...
```

A source ngram can be empty (0-gram).

# Vocabulary calculation

Given a sentence `S = m_1 ... m_k`, the target vocabulary `Tvoc` is calculated as followed:

```
Tvoc.insert(meanings[''])

for i = 1, k do
  for p = 1, k-i+1 do
  	seq = concat(m_p, ' ', ..., m_{p+i-1})
  	Tvoc.insert(meanings[seq])
  end
 end
```

where `meanings` is a map string>list of string.

# Building a vmap

To build a vmap, you need to have a list of 0-generated meanings (see below) and a phrase table for your language pair (can be gzipped). The vmap is build using the script `build-vmap.py`:

```
usage: build-vmap.py [-h] -pt PHRASE_TABLE [-zg ZERO_GENERATE_LIST]
                     [-ms MAX_SIZE] [-mf MIN_FREQ] [-km KEEP_MEANING]
                     [-tv TGT_VOCAB] [-l LIMIT]

optional arguments:
  -h, --help            show this help message and exit
  -pt PHRASE_TABLE, --phrase_table PHRASE_TABLE
                        phrase table
  -zg ZERO_GENERATE_LIST, --zero_generate_list ZERO_GENERATE_LIST
                        list of terms generated from 0
  -ms MAX_SIZE, --max_size MAX_SIZE
                        maximal size of source sequences
  -mf MIN_FREQ, --min_freq MIN_FREQ
                        minimal frequency of pair
  -km KEEP_MEANING, --keep_meaning KEEP_MEANING
                        number of meaning to keep per entry
  -tv TGT_VOCAB, --tgt_vocab TGT_VOCAB
                        save target vocabulary for max coverage calculation
  -l LIMIT, --limit LIMIT
                        limit the number of entries (for dev)
```

Typically `-ms 3 -mf 2 -km 20` should give a good coverage.

The vmap is generated on stdout, and on stderr, the 50 most common meanings are display - this list is generally a good candidate for build the 0-generated list file.

The 0-generated file is a simple text file with one meaning per line.

# Evaluating the vmap

You can evaluate the coverage of a vmap on a given test set (source and target tokenized) with the `eval-vmap.py` script and using the `TGT_VOCAB` that you can generate as an additional file using `build-vmap.py` script.

```
usage: eval-vmap.py [-h] -vmap VMAP [-tv TV] -src SRC -tgt TGT

optional arguments:
  -h, --help  show this help message and exit
  -vmap VMAP  a vocab mapping file
  -tv TV      target vocabulary file
  -src SRC    source file
  -tgt TGT    target file
```

The script is outputing the coverage ratio of the target sentences predicted from source sentences using the vmap, and the number of vocabs per sentence.

# Building phrase-table

You can build a phrase table using the docker described in the repository:

```
docker build -f Dockerfile . -t build-pt
docker run -v MYCORPUSPATH:/root/corpus build-pt CORPUSNAME SS TT N > phrase-table.gz
```

where `CORPUSPATH/CORPUSNAME.{SS,TT}` are tokenized source/target files, and `N` the max n-gram length.
