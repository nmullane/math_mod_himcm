#!/bin/bash

cd plots/saved_plots
for fn in `ls`; do
    xdg-open $fn
done
