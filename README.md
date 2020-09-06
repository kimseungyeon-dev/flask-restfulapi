# flask-restfulapi

docker 
 - container : Ubuntu 14.04.6
 - python 3.4.3 
 - flask
 - sqlalchemy
 - sqlite

install command
 - docker run -it --name flask -p 5000:5000  ubuntu:14.04
 - apt update && apt install python3-pip -y
 - pip3 install virtualenv && virtualenv 소스디렉토리
 - source bin/activate && pip3 install flask-restful & pip3 install Flask-SQLAlchemy
 - apt-get install sqlite3
