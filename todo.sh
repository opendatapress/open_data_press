# Shows all TODO  comments in the codebase
grep --recursive --line-number --exclude-dir="lib" --exclude-dir=".git" --exclude="todo.sh" --exclude="*.pyc" TODO . | sed -e 's/:[ ]\+/\t/g'