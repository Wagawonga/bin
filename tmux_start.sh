#!/bin/bash

if [[ ! $TERM =~ screen ]] && [ -z $TMUX ]
then
    tmux new-session -d
    tmux split-window -h
    tmux select-pane -R
    tmux attach-session -d
fi
