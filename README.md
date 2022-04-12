# crop_yield
Crop yield prediction Instalation Guide:

# Pull the source code by this command: 
git clone https://github.com/ashik035/crop_yield.git

# Now run these commands at the project dir

pip install --upgrade pip

pip install virtualenv

python -m virtualenv venv 

source venv/Scripts/activate

pip install django

python manage.py migrate

python manage.py runserver
