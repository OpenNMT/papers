#!/bin/bash

fast=/root/fast_align/build
trainPT=/root/mosesdecoder/scripts/training/train-model.perl

fastalign(){
    echo "RUN FASTALIGN"
    corpus_dir=$1
    work_dir=/root/workspace
    base=$2
    ss=$3
    tt=$4
    cd ${corpus_dir}
    dir=/root/workspace/$base.${ss}2${tt}
    filter_corpus_dir=/root/workspace/filtered
    mkdir -p $dir
    mkdir -p $filter_corpus_dir
    python /root/filter.py $base.$ss $base.$tt $filter_corpus_dir
    cd $filter_corpus_dir
    python /root/paste.py $base.$ss $base.$tt > $dir/data.${ss}-${tt}
    $fast/fast_align -i $dir/data.${ss}-${tt} -d -o -v    > $dir/data.${ss}-${tt}.forward 2> $dir/data.${ss}-${tt}.forward.log
    $fast/fast_align -i $dir/data.${ss}-${tt} -d -o -v -r > $dir/data.${ss}-${tt}.reverse 2> $dir/data.${ss}-${tt}.reverse.log
    echo "$fast/atools -i $dir/data.${ss}-${tt}.forward -j $dir/data.${ss}-${tt}.reverse -c grow-diag-final-and > $dir/${base}.${ss}2${tt}.gdfa"
    $fast/atools -i $dir/data.${ss}-${tt}.forward -j $dir/data.${ss}-${tt}.reverse -c grow-diag-final-and > $dir/${base}.${ss}2${tt}.gdfa    
}

learn_PB(){
    echo "BUILD PHRASETABLE"
    corpus_dir=/root/workspace/filtered
    work_dir=/root/workspace
    name=$2
    ss=$3
    tt=$4
    maxsent=$5
    dmodel=/root/workspace/$name.${ss}2${tt}
    mkdir -p $dmodel

    $trainPT \
    --first-step 4 \
    --last-step 6 \
   --corpus ${corpus_dir}/${name} \
    --f $ss \
    --e $tt \
    --alignment-file ${work_dir}/${name}.${ss}2${tt}/${name}.${ss}2${tt} \
    --alignment gdfa \
    --model-dir $dmodel \
    --lexical-file $dmodel/lex \
    --max-phrase-length $maxsent \
    --phrase-translation-table $dmodel/phrase-table \
    --factor-delimiter "NoFaCtOrS" \
    --parallel
}

>&2 fastalign /root/corpus $1 $2 $3
>&2 learn_PB /root/corpus $1 $2 $3 $4

cat /root/workspace/$1.${2}2${3}/phrase-table.gz
