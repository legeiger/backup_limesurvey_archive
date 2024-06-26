## Backup Docker Container for Limesurvey
Simple docker container which offers an easy way to export lsa and lss archives from Limesurvey to a folder of your choice.
I use it in compaion with cron and a backup script to export all surveys inside the limesurvey instance.

Currently only Limesurvey >= 6.X are supported. 

## Usage

You only need to specify hostname, username and password. All surveys will be exported in the mounted folder /data. 

    docker run --rm -it -v /folder/to/backup:/data \
    -e timestamp="" \    
    -e LS_URL="" \
    -e username="" \
    -e password="" ghcr.io/legeiger/backup_limesurvey_archive:v2

timestmap should be string containing current date and time like `2022-03-01_12:03:34`.
LS URL should be the whole FQDN of the server with leading https:// like `https://account.limesurvey.org/de/`.


### push new image
https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry

    docker build -t backup_limesurvey_archive:v3 .

    docker login ghcr.io --username legeiger --password-stdin

    docker tag backup_limesurvey_archive:v3  ghcr.io/legeiger/backup_limesurvey_archive:v3

    docker push ghcr.io/legeiger/backup_limesurvey_archive:v3


