
if [ "$color_prompt" = yes ]; then
    PS1='\n\[\033[0;35m\]`acpi | grep -E -o "[0-9]*%"`\[\033[00m\]:${debian_chroot:($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\[\033[1;31m\]`__git_ps1`\[\033[0;37m\]   \n$'
else
    PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w\$ '
fi
