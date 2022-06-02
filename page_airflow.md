---
layout: page
title: Using Airflow for job control in zts.
---

### Setting up Airflow to run in a Docker container:
* Initial setup will follow the Apache Airlow quick-start procedure and run with CeleryExecuter.  Apache Airflow documentation recommends running on kubernetes (with official helm chart) for production.
Install [Docker Community Edition](https://docs.docker.com/engine/install/) - ~already installed~

1. Install [Docker Community Edition](https://docs.docker.com/engine/install/)  *(already installed)*
   1. Configure to use 4GB / container

    * check memory:

        `docker run --rm "debian:bullseye-slim" bash -c 'numfmt --to iec $(echo $(($(getconf _PHYS_PAGES) * $(getconf PAGE_SIZE))))'`

    * change config
      - mac: [here](https://docs.docker.com/desktop/mac/)
      - windows: [here](https://docs.docker.com/desktop/windows/)

2. Install Docker Compose (v1.29.1) - [here](https://docs.docker.com/compose/install/) ~already installed~
3. Deploy Airflow on Docker Compose
    1. fetch [docker-compose.yaml](https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml)

        `curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.3.0/docker-compose.yaml'`

    * notes:
      * **airflow-scheduler**: monitors all tasks and DAGs, then triggers the task instances once their dependencies are complete.
      * **airflow-webserver**: available at [localhost:8080](available at http://localhost:8080)
      * **airflow-worker**: executes the tasks given by the scheduler
      * **airflow-init**: initialization service
      * **flower**: [flower app](https://flower.readthedocs.io/en/latest/), Celery monitoring tool. [localhost:5555](http://localhost:5555)
      * **postgres**: database
      * **redis**: broker that forwards messages from scheduler to worker
