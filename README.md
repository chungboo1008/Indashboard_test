# README

## First Need to Know
0. First Use
```
pip install -r requirements.txt
(django 3.9.4)
```
1. How to run
```
source venv/bin/activate 
(windows https://ithelp.ithome.com.tw/articles/10199980
.\venv\Scripts\activate.bat )

(postgreSQL ip
mblog>mainsite>view.py
line554
140.112.26.237)

cd mblog

python3 manage.py runserver 0.0.0.0:8002
(python manage.py runserver 0.0.0.0:8002)
```
2. Code structure
```
├── mblog (main project)
├── VENV 
│   ├── mainsite (models.py,admin.py,serializers.py,views.py)
│   ├── mblog (settings.py,urls.py)
│   ├── media 
│       ├── csv
│       ├── image
│       ├── xml
│   ├── static(for dashboard javascripts) 
│   ├── templates (index.html)
│       ├── temp(footer.html)
│   ├── templates (index.html)

```
3. Database structure

| auth_user| profile  |
| -------- | -------- |
| id(pk)   | id(pk)   |
| password |user_id(fk)|
|last_login|plan_id|
|is_superuser|dashboard|
|username||
|first_name||
|last_name||

4. APIs
https://hackmd.io/@K7Zj4KtHTsKtAwrOFk3ejA/BkVuUSLnS

5. Login Information
```
140.112.26.237:8002/admin
user_name:admin
password:ntu33663366
```

## Database How to Use

create a migration
```
python3 manage.py makemigrations
python manage.py makemigrations
```
Execute SQL 
```
python3 manage.py migrate
python manage.py migrate
```
## MATLAB SERVER

Start a MATLAB Production Server
```
mps-start -C matlab_server1
```
Status of MATLAB Production Server
```
mps-status -C matlab_server1
```