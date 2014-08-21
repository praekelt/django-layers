#!/bin/sh

virtualenv ve
./ve/bin/python setup.py develop
./ve/bin/python manage.py runserver 0.0.0.0:8000 --settings=example.settings_basic &
./ve/bin/python manage.py runserver 0.0.0.0:8001 --settings=example.settings_web &
sleep 2
echo "Hit X to quit..."
while true; do
    read -p "Hit X[enter] to quit" yn
    case $yn in
        [Xx]* ) break;;
    esac
done
killall ./ve/bin/python
