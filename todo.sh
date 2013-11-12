# Shows all TODO  comments in the codebase
grep --recursive --line-number --exclude-dir="./lib" --exclude="todo.sh" TODO . | sed -e 's/:[ ]\+/\t/g'