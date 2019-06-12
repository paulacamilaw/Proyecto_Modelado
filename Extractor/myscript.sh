#!/usr/bin/env bash

rm *.3D

v=${1?Error: Ingrese otra variable}
b=${2?Error: Ingrese otro bloque}

python extractor.py extraer $v-$b

cp *.3D ../../../../../Visit/Proj/

cd
./visit
