#!/usr/bin/env bash
# script for doing numerous pip operations

case $1 in
  "freeze")
    printf "Freezing current dependencies into requirements.txt\n"
    pip freeze --local > requirements.txt
    ;;

  "load")
    printf "Installing dependencies from requirements.txt\n"
    pip install -r "./requirements.txt"
    ;;

 *)
   printf "bash scripts.sh [freeze, load]\n"
   ;;
esac