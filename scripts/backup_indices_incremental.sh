#!/bin/sh


i=docs
elasticdump   --input=http://localhost:9200/$i   --output=$   --searchBody '{"query": { "range" : { "gather_time" : { "gte" : "now-1d/d", "lt" :  "now/d" } } }, "_source": { "excludes": [ "words" ] }}'   | gzip > /var/backup/${i}_incr_$(date +%u).json.gz
elasticdump   --input=http://localhost:9200/$i   --output=$   --searchBody '{"query": { "range" : { "gather_time" : { "gte" : "now-1d/d", "lt" :  "now/d" } } }}'   | gzip > /var/backup/${i}_words_incr_$(date +%u).json.gz
for i in docs_history errors suggestions feeds; do
    elasticdump   --input=http://localhost:9200/$i   --output=$   --searchBody '{"query": { "range" : { "gather_time" : { "gte" : "now-1d/d", "lt" :  "now/d" } } }}'   | gzip > /var/backup/${i}_incr_$(date +%u).json.gz
done

