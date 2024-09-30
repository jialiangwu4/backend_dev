# remove old deployment zip.
rm -f deployment.zip

# activate venv 
source .venv/bin/activate

# generate requirements 
# excluding pkg_resources package as it's causing error. 
# source: https://stackoverflow.com/a/40167445/8644910
pip freeze | grep -v "pkg_resources" > requirements.txt

# source the ~/.zprofile in case of any env changes
source ~/.zprofile 

# create/overwrite static files 
python3 manage.py collectstatic --noinput

# generate a zip file named deployment.zip, excluding .git and .venv
zip -r deployment.zip . -x "*.git*" "*.venv*"

eb deploy