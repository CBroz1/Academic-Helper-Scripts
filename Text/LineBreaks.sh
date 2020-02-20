 

 awk '{ sub("\r$", ""); print }' $1.sh > $2.sh