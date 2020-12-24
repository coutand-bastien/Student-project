#!/bin/bash

if [ $# = 0  ]; then
    java -jar ./build/artifacts/Projet_ASD3_CompressionImageBitmap_jar/Projet_ASD3_CompressionImageBitmap.jar
fi

if [ $# = 3  ]; then
    java -jar ./build/artifacts/Projet_ASD3_CompressionImageBitmap_jar/Projet_ASD3_CompressionImageBitmap.jar "$1" "$2" "$3"
fi