
# FOODGRAM-REACT-PROJECT

### Foodgram it's a unique social network, capable to connect people around the world. If you like delicious meals, you can try this app. Features of this app: you can create recipies, add to favorited, subscribe on any author, add all your favorited recepies to shopping cart what allows you to download pdf.file of all ingredients which you added. 


## Getting Startet

### To start this project you need to do this few steps

```bash
    git clone git@github.com:XviD1231/foodgram-project-react.git
```
### Move to your directory with project
```
    cd <your/path_to_project>/foodgram-project-react/infra
```
### Connect to your server:
```
    ssh - i <path_to_SSH/SSH_name><username@server_ip>
```
### Install docker compose on your remote server(better do it in your root directory):
~~~
    - sudo apt update
    - sudo apt install curl
    - curl -fSL https://get.docker.com -o get-docker.sh
    - sudo sh ./get-docker.sh
    - sudo apt-get install docker-compose-plugin 
~~~
### Create file_for_project:
~~~
    sudo mkdir /foodgram-project-react/
~~~
### Copy infra directory from foodgram-project-react on your remote server:
~~~
    scp -i path_to_SSH/SSH_name foodgram-project-recact/infra/ \
    username@server_ip:/home/username/foodgram-project-react/infra
~~~
### Work with containers:
~~~
    - cd foodgram-project-react
    - sudo docker system prune -af
    - sudo docker compose pull
    - sudo docker compose down -v
    - sudo docker compose up --build -d
~~~
### Next step is create tables on database, load this tables with data of ingredients using management command
~~~
    - cd foodgram-project-react
    - sudo docker compose -f docker-compose.yml exec backend python manage.py makemigrations
    - sudo docker compose -f docker-compose.yml exec backend python manage.py migrate
    - sudo docker compose -f docker-compose.yml exec backend python manage.py collectstatic
    - sudo docker compose -f docker-compose.yml exec backend cp -r /app/collected_static/ ./app/backend_static/
    - sudo docker compose -f docker-compose.yml exec backend python manage.py createsuperuser
~~~

​

## Screenshot

![App Screenshot](https://pictures.s3.yandex.net/resources/S16_01_1692340098.png)


## Stack of backend:
___
![Python](https://img.shields.io/badge/Python%20-3.9-blueviolet) ![Django](https://img.shields.io/badge/Django%20-3.2-blueviolet) ![DRF](https://img.shields.io/badge/DjangoRestFramework-3.12.4-blueviolet) ![simple](https://img.shields.io/badge/DjangoRestFramework--simplejwt-5.2.2-blueviolet)![Docker](https://img.shields.io/badge/Docker-Desktop-red)

## Example of env file:
~~~
POSTGRES_DB=<your_db_name>
POSTGRES_USER=<your_name>
POSTGRES_PASSWORD=<your_password>
DB_HOST=db
DB_PORT=5432
# Данные серверов и ключа.
ALLOWED_HOSTS=<dns-example>,localhost,127.0.1
SECRET_KEY=<django-secret-key from settings>
~~~
## Feedback

If you have any feedback, please reach out to me at vxvidv@gmail.com



## 🔗 Link
[![portfolio](https://img.shields.io/badge/my_portfolio-000?style=for-the-badge&logo=ko-fi&logoColor=white)](https://github.com/XviD1231?tab=repositories)


## Links to site for reviewer
 - [https://130.193.42.123/](https://130.193.42.123/)
 - [https://foodgram-xvid.servebeer.com](https://foodgram-xvid.servebeer.com)
 - Superuser ```login: Test```, ```email: sd@sd.sd```, ```password: 1```
