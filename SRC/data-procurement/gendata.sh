#!/bin/bash
cd data-generation;
python3 populate_data.py $1 $2 ;

cd ../;
python3 unify_data.py;