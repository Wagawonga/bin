#!/bin/bash

if [[ ! $TERM =~ screen ]] && [ -z $TMUX ]
then
    SESSION=main
    if ! tmux has-session -t $SESSION; then
        tmux new -d -s $SESSION
        tmux split-window -h
        tmux select-pane -R
    fi
    tmux attach -dt $SESSION
fi
