git config --global user.email "<>"
git config --global user.name "Sakura OTA poster"
git fetch
git pull
COMMIT_MESSAGE=$(cat commit_mesg.txt)
rm commit_mesg.txt
git add .
git commit -m "$COMMIT_MESSAGE"
git push origin 11