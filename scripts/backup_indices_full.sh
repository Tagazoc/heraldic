#!/bin/sh

i=docs
elasticdump   --input=http://localhost:9200/$i   --output=$   | gzip > /var/backup/$i_words_full.json.gz
elasticdump   --input=http://localhost:9200/$i   --output=$   --searchBody '{"query": { "range" : { "gather_time" : { "lt" :  "now/d" } } }, "_source": { "excludes": [ "words" ] }}' | gzip > /var/backup/$i_full.json.gz
for i in docs_history errors suggestions feeds; do
    elasticdump   --input=http://localhost:9200/$i --output=$ --searchBody '{"query": { "range" : { "gather_time" : { "lt" :  "now/d" } } }}'| gzip > /var/backup/$i_full.json.gz
done

