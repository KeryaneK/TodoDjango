Setup:

'./frontend'  
npm install  
npm run dev 

'./'  
pip install -r requirements.txt   
python manage.py makemigrations  
python manage.py migrate  
python manage.py runserver  

Unfortunately lack of time got me - that's why the frontend is unfinished. You can still check my approach as the login page is working properly.
I've tried to use as many DRF's build-in methods as possible to keep things clean (pagination, authentication, data validation etc.).
Being honest the API took me around 6 hours - that might be because I'm not working with Django on the daily basis. Anyway it was still fun! :)