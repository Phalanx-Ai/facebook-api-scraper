#!/bin/bash

MYDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
cd ${MYDIR}

mkdir -p data/today
mkdir -p data/archive

export PYTHONIOENCODING=utf8
. ./settings.env

python3 ./scrape_posts.py > data/today/fb-posts.json
python3 ./transform_json_post_to_sirius.py data/today/fb-posts.json > data/today/fb-posts.jf
python3 ./import_posts.py data/today/fb-posts.jf
python3 ./set_root_posts.py data/today/fb-posts.jf

python3 ./scrape_comments.py data/today/fb-posts.json > data/today/fb-comments.jf
python3 ./import_posts.py data/today/fb-comments.jf
python3 ./pair_posts_with_comments.py

cp data/today/fb-posts.jf data/archive/fb-posts-`/bin/date +%Y-%m-%d`.jf
cp data/today/fb-comments.jf data/archive/fb-comments-`/bin/date +%Y-%m-%d`.jf
