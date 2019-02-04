#!/bin/bash

freezeRepoDir='C:\muellz\freeze\'
bugprefix='freezerbug_'
fixedsuffix='_FIXED'
freezeRepo='git@gitserv1.telejet.de:robot-dev/freezedata.git'
callingDir='/home/daniel/bin'

version() {
    echo "V1.95  1.2.18 Nach Fix Rueckkehr zu alten Branch"
    echo "V1.94  12.12.17 Fehler bei der Versionsanzeige behoben"
    echo "V1.93  28.9.17 Versionsanzeige."
    echo "V1.92  27.9.17 Fehlernachricht bei getBranch erweitert."
    echo "V1.91  27.9.17 Falsches auscheckend bei -f -u behoben."
    echo "V1.9   19.9.17 Erstellen von working copy"
    echo "V1.8   18.9.17 Name darf nur Alphanummerisch sein!"
    echo "V1.71 Bugfix rename bei -f"
    echo "V1.7 Fixed Flag hinzugefuegt. Auto fetch bei -l"
    echo "V1.6 Auschecken der Bugs jetzt ueber Nummer!"
    echo "V1.5 bug suffix zu prefix; Nummerierung eingf."
    echo "V1.4 Freezer"
    echo "Merge of V1.3 & V1.2"
    echo "1.3 Freezer"
    echo "V1.21 Freezer jetzt mit freeze Repository"
    echo "V1.2 Freezer "
    echo "V1.1 Repo for freezefiles is added automaticaly"
}

usage() {
    echo "usage: git freezer <subcommand>"
    echo
    echo "Available subcommands are:"
    echo "-v             - Version Info."
    echo "-h             - Show this help."
    echo 
    echo "To show freezed branches sorted by date:"
    echo "-l             - show unfixed."
    echo "-la            - show all" 
    echo "-lf            - show fixed" 
    echo 
    echo "push           - Generate a new Branch with the freeze files"
    echo "                 The freezefiles have to be generated first!"
    echo "-d <bugnumber> - Deletes the branches for the specified bug."
    echo "-f <bugnumber> - mark as Fixed"
    echo "-u <bugnumber> - remove fixed Mark"
    echo "<bugnumber>    - restore all freezefiles for replay."
}

isClean(){
	value=$(git diff --exit-code)
	if [ "$?" != "0" ]; then
		echo "Workspace is not clean!"
		echo "Canceled"
		exit 1
	fi
}

freezerInit(){
    #verknuepfung zum Repo sicherstellen:
    if [ ! -d "$freezeRepoDir"'\.git' ]; then
        echo "Setting up System for freezer use:"
        echo
	    mkdir -p $freezeRepoDir	
        # Nicht einfach clonen, für den Fall, dass "Dir not empty"
        oldPwd=$PWD
        cd $freezeRepoDir
        git init
        git remote add origin $freezeRepo
        git fetch
        cd $oldPwd
        echo
        echo "Preperations for use of freezer DONE!"
        echo
    fi
}

push(){
    isClean
    #Hier Momentanen Branchnamen ermitteln.
    oldBranch=$(git rev-parse --abbrev-ref HEAD)
    read -p "Enter name of Bug:" bugname
    bugname=${bugname// /_}
    if [[ "$bugname" =~ [^a-zA-Z0-9_] ]]; then
      echo
      echo "Name ist UNGUELTIG!!!"
      echo "Es werden nur alphanummerische Zeichen und Leezzeichen bzw. Unterstriche akzeptiert!"
      echo
      echo "VORGANG ABGEBROCHEN!"
      echo
      exit 1
    fi 
    if [ -z "$bugname" ]; then
        echo
        echo "keine Name angegebenen!"
        echo
        exit 1
    fi
    read -p "Enter description:" description
    if [ -z "$description" ]; then
        echo
        echo "keine Beschreibung angegebenen!"
        echo
        exit 1
    fi

    cwd=$PWD

    cd $freezeRepoDir

    git reset --soft origin/master
    git fetch origin bugcount -q
    git checkout -f origin/bugcount -- bugcount.txt 
    bugno=$(head -n1 bugcount.txt)
    bugno=$(($bugno + 1))
    bugname="$bugprefix$bugno"'_'"$bugname"
    echo "Gespeichert als Bug Nr.: $bugno"
    
    git checkout -b $bugname
    git add -A
    git commit -m"$bugname":
    git push origin -u $bugname:$bugname > /dev/null
    echo "Replays gespeichert."

    git checkout -q bugcount    
    git pull -q
    echo $bugno > bugcount.txt
    git add -A
    git commit --allow-empty -q -m"Bug Nummer: $bugno" > /dev/null
    git push -q
    echo "Bugcount erhoeht."
    git checkout $bugname #Wechsel damit letzte freezedata in freezedir!

    cd $cwd
    git checkout -b $bugname
    git commit --allow-empty -q -m"$description"
    git push origin $bugname:$bugname -u 
    git checkout $oldBranch
    
}

getbranch(){
    local res=$(git branch -r --sort=-committerdate | grep "$bugprefix""$1"'_'| grep -v HEAD | sed 's@\<origin\>/@@g')

    if [ $(echo "$res" | wc -l) != 1 ]; then
        >&2 echo 
        >&2 echo "Zu der gegeben Nummer konnte kein Branch bestimmt werden"
        >&2 echo "Ggf. sind die refs veraltet, dann hilft git fetch -p"
        >&2 echo 
        exit 1
    fi
    echo $res
}

del(){
    isClean
    todel=$(getbranch "$1")
    
    read -p "$todel loeschen? (j/n)" anw
    if [ "j" != "$anw" ]; then
        echo
        echo "Abbruch."
        exit 1
    fi

    cwd=$PWD 
    git push origin :"$todel"
    git remote prune origin
    git branch -D "$todel"
    cd $freezeRepoDir
    nosuffix=${todel%%$fixedsuffix}
    git checkout master
    git push origin :"$nosuffix"
    git remote prune origin
    git branch -D "$nosuffix"
    cd $cwd
}

logall(){
    echo
    for branch in `git branch -r --sort=-committerdate | grep $bugprefix| grep -v HEAD`;do 
        printf "%-30s $(git show $branch --format="%cr" | head -n 1) \n" $branch 
    done | sed 's@\<origin\>/@@g' 
}

logunfixed(){
    echo
    for branch in `git branch -r --sort=-committerdate | grep $bugprefix| grep -v HEAD`;do 
        printf "%-30s $(git show $branch --format="%cr" | head -n 1) \n" $branch
    done | sed 's@\<origin\>/@@g' | grep -v $fixedsuffix
}

logfixed(){
    echo
    for branch in `git branch -r --sort=-committerdate | grep $bugprefix| grep -v HEAD`;do
        printf "%-30s $(git show $branch --format="%cr" | head -n 1) \n" $branch
    done | sed 's@\<origin\>/@@g' | grep $fixedsuffix
}

setfixed(){
    oldBranch=$(git rev-parse --abbrev-ref HEAD)
    branch=$(getbranch "$1")
    if [[ $branch == *$fixedsuffix ]]; then
        echo
        echo "Branch hat bereits Fixed-Suffix."
        echo "Abbruch!"
        exit 1
    fi
    newname="$branch""$fixedsuffix"
    git checkout $branch
    git branch -m "$branch" "$newname" 
    git push origin :"$branch"
    git push origin -u "$newname":"$newname"
    git checkout $oldBranch
}

unsetfixed(){
    branch=$(getbranch "$1")
    oldBranch=$(git rev-parse --abbrev-ref HEAD)
    if [[ $branch != *$fixedsuffix ]]; then
        echo
        echo "Branch hat keinen Fixed-Suffix zum entfernen."
        echo "Abbruch!"
        exit 1
    fi
    newname=${branch%$fixedsuffix}
    git checkout $branch
    git branch -m "$branch"  "$newname"
    git push origin :"$branch"
    git push origin -u  "$newname":"$newname"
    git checkout $oldBranch
}

main(){
    cd $callingDir
    freezerInit
    #Letzte Zeile Löschen (leider wird in git-freezer eine falsche
    #Versionsangabe gemacht und damit eine Änderung dort nicht zu
    #Problemen führt wird die Änderung hier rückgängig gemacht.)
    echo -ne "\033[1A\033[0K"
    echo $(version | head -n 1)
    echo

    if [ "$#" -lt 1 ]; then
        usage; exit 1
    fi

    git fetch -a 
    local subcommand="$1"; shift

    case $subcommand in
        "-h"|"--help")
            usage; exit 0
            ;;
        "-v"|"--version")
            version; exit 0
            ;;
        "push")
            push; exit 0
            ;;
        "-la")
            logall; exit 0
            ;;
        "-l")
            logunfixed; exit 0
            ;;
        "-lf")
            logfixed; exit 0
            ;;
        "-f")
            setfixed "$1"; exit 0
            ;;
        "-u")
            unsetfixed "$1"; exit 0
            ;;
        "-d")
            del "$1"; exit 0
            ;;  
    esac

    #Wenn kein Parameter kein Subcommand dann ist es ein Bugname -> auschecken:

    tocheckout=$(getbranch "$subcommand")
    isClean
    git checkout $tocheckout -f

    cd $freezeRepoDir
    git fetch -a -p
    nosuffix=${tocheckout%%$fixedsuffix}
    git checkout $nosuffix -f
    
    exit 0
}

main "$@"
