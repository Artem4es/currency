#!/bin/sh

until alembic upgrade heads

do
    echo "Waiting for volume to be ready..."
    if [ "$counter" -gt 5 ];
    then
        echo "Exiting loop!"
        exit 1
    else
        counter=$((counter+1))
        sleep 5
    fi
done

python3 main.py