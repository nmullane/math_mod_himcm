#!/bin/bash

for fn in `ls Rplots*.pdf`; do
    mv $fn plots/
    cd plots/
    xdg-open $fn
    cd ..
done
