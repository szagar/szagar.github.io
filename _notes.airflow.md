#Using Airflow for job control in zts.

## Setting up Airflow to run in a Docker container:
* Initial setup will follow the Apache Airlow quick-start procedure and run with CeleryExecuter.  Apache Airflow documentation recommends running on kubernetes (with official helm chart) for production.
1. [Install Docker Community Edition](https://docs.docker.com/engine/install/) - ~already installed~
  1. Configure to use 4GB / container
    * check memory: `docker run --rm "debian:bullseye-slim" bash -c 'numfmt --to iec $(echo $(($(getconf _PHYS_PAGES) * $(getconf PAGE_SIZE))))'`
    * mac: [here](https://docs.docker.com/desktop/mac/)
    * windows: [here](https://docs.docker.com/desktop/windows/)
2. Install Docker Compose (v1.29.1) - [here](https://docs.docker.com/compose/install/) ~already installed~
