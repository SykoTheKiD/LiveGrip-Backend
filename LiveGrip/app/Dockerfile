FROM python:3.5-onbuild
CMD /usr/local/bin/gunicorn LiveGrip.wsgi:application -w 2 -b :8000

ENV SECRET_KEY=oze6a9^1zt@3dc++%uux0@b3&y)lhssy5xo+ufbs+)43$hw4#o
ENV DEBUG=true
ENV DB_NAME=mysql
ENV DB_USER=mysql
ENV DB_PASS=mysql
ENV DB_SERVICE=mysql
ENV DB_PORT=3306
ENV CI=false
