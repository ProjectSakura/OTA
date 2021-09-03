git config --global user.email "noreply.projectsakurabot@gmail.com"
git config --global user.name "Project Sakura Bot"
git fetch
git pull
COMMIT_MESSAGE=$(cat commit_mesg.txt)
rm commit_mesg.txt
git add .
git commit -m "$COMMIT_MESSAGE"
git push origin 11