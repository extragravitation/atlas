#!/bin/sh
# Reader A: download archive + paper source, verify hash, extract.
set -e
D=/home/claude/audit_xcop/readers/a
mkdir -p $D/dl $D/ex $D/paper/src
curl -sL -o $D/dl/data_E22.tar.gz "https://drive.switch.ch/index.php/s/nKxwcKwftb3Esjc/download"
echo "ff9ad2129c7bd50f95783c32369643eb87cc9e5ac7a6bfc3eda090e31838953d  $D/dl/data_E22.tar.gz" | sha256sum -c - || { echo "HASH MISMATCH - STOP"; exit 1; }
tar -xzf $D/dl/data_E22.tar.gz -C $D/ex
curl -sL -o $D/paper/eprint.tar.gz https://arxiv.org/e-print/2205.01110v1
tar -xzf $D/paper/eprint.tar.gz -C $D/paper/src
