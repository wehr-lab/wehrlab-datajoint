#!/bin/bash

# -------------------
# adapted from https://github.com/datajoint/mysql-docker/blob/master/dist/debian/Dockerfile
# This is probably super insecure and the sql database shouldn't
# be exposed without first making sure it's safe!
# --------------------


# change this to where ya puttin stuff
# this should match the directories in sql_df.cnf
BASE_DIR=/mnt/fastdisk/datajoint

SQL_BASE=${BASE_DIR}/base
SQL_DATA=${BASE_DIR}/data
SQL_MESSAGES=${BASE_DIR}/messages
SQL_TMP=${BASE_DIR}/tmp
SQL_KEYS=${BASE_DIR}/keys

mkdir SQL_BASE
mkdir SQL_DATA
mkdir SQL_MESSAGES
mkdir SQL_TMP
mkdir SQL_KEYS
sudo chown mysql:mysql SQL_KEYS

CNF_DESTINATION=/etc/mysql/conf.d

## ----------------
# make keys and then make them owned by the mysql user

# Create CA certificate
openssl genrsa 2048 > ${SQL_KEYS}/ca-key.pem;
openssl req -subj '/CN=CA/O=MySQL/C=US' -new -x509 -nodes -days 3600 \
        -key ${SQL_KEYS}/ca-key.pem -out ${SQL_KEYS}/ca.pem;
# Create server certificate, remove passphrase, and sign it
# server-cert.pem = public key, server-key.pem = private key
openssl req -subj '/CN=SV/O=MySQL/C=US' -newkey rsa:2048 -days 3600 \
        -nodes -keyout ${SQL_KEYS}/server-key.pem -out ${SQL_KEYS}/server-req.pem;
openssl rsa -in ${SQL_KEYS}/server-key.pem -out ${SQL_KEYS}/server-key.pem;
openssl x509 -req -in ${SQL_KEYS}/server-req.pem -days 3600 \
        -CA ${SQL_KEYS}/ca.pem -CAkey ${SQL_KEYS}/ca-key.pem -set_serial 01 -out ${SQL_KEYS}/server-cert.pem;
# Create client certificate, remove passphrase, and sign it
# client-cert.pem = public key, client-key.pem = private key
openssl req -subj '/CN=CL/O=MySQL/C=US' -newkey rsa:2048 -days 3600 \
        -nodes -keyout ${SQL_KEYS}/client-key.pem -out ${SQL_KEYS}/client-req.pem;\
openssl rsa -in ${SQL_KEYS}/client-key.pem -out ${SQL_KEYS}/client-key.pem;\
openssl x509 -req -in ${SQL_KEYS}/client-req.pem -days 3600 \
        -CA ${SQL_KEYS}/ca.pem -CAkey ${SQL_KEYS}/ca-key.pem -set_serial 01 -out ${SQL_KEYS}/client-cert.pem

# make all the files owned by mysql
sudo chown -R mysql:mysql ${SQL_KEYS}

# ---------------------
# copy our config file

sudo cp ./sql_db.cnf ${CNF_DESTINATION}/dj.cnf
sudo chown mysql:mysql ${CNF_DESTINATION}/dj.cnf
sudo chmod g+w ${CNF_DESTINATION}/dj.cnf
