#!/bin/bash

for fn in `ls Rplots*.pdf`; do
    mv $fn plots/
    cd plots/
    xdg-open $fn
    cd ..
done
for fn in `ls plots/Rplots*.pdf`; do
    xdg-open $fn
done
