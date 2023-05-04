# slim debian version allows JAVA JDK 8
FROM python:3.10-slim

# Never prompt the user for choices on installation/configuration on packages
ENV DEBIAN_FRONTEND noninteractive
ENV TERM linux

# Airflow
ARG AIRFLOW_VERSION=2.6.0
ARG SPARK_VERSION=3.2.4
ARG HADOOP_VERSION=3.2
ARG AIRFLOW_HOME=/usr/local/app
ARG AIRFLOW_DEPS=""
ARG PYTHON_DEPS=""
ENV AIRFLOW_GPL_UNIDECODE yes

# Define en_US.
ENV LANGUAGE en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8
ENV LC_CTYPE en_US.UTF-8
ENV LC_MESSAGES en_US.UTF-8

COPY requirements.txt ./requirements.txt

RUN set -ex \
  && buildDeps=' \
  freetds-dev \
  libkrb5-dev \
  libsasl2-dev \
  libssl-dev \
  libffi-dev \
  libpq-dev \
  git \
  ' \
  && apt-get update -yqq \
  && apt-get upgrade -yqq \
  && apt-get install -yqq --no-install-recommends \
  $buildDeps \
  freetds-bin \
  build-essential \
  default-libmysqlclient-dev \
  apt-utils \
  curl \
  rsync \
  netcat \
  locales \
  iputils-ping \
  telnet \
  && sed -i 's/^# en_US.UTF-8 UTF-8$/en_US.UTF-8 UTF-8/g' /etc/locale.gen \
  && locale-gen \
  && update-locale LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 \
  && useradd -ms /bin/bash -d ${AIRFLOW_HOME} airflow \
  # && useradd -ms /bin/bash airflow \
  && pip install -U pip setuptools wheel \
  && export PYTHON_VERSION="$(python --version | cut -d " " -f 2 | cut -d "." -f 1-2)" \
  && export CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt" \
  && pip install "apache-airflow[async,crypto,celery,postgres,hive,google,jdbc,mysql,ssh${AIRFLOW_DEPS:+,}${AIRFLOW_DEPS}]==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}" \
  && if [ -n "${PYTHON_DEPS}" ]; then pip install ${PYTHON_DEPS}; fi \
  && pip install pyspark==${SPARK_VERSION} \
  && pip install -r requirements.txt \
  && apt-get purge --auto-remove -yqq $buildDeps \
  && apt-get clean \
  && rm -rf \
  /var/lib/apt/lists/* \
  /tmp/* \
  /var/tmp/* \
  /usr/share/man \
  /usr/share/doc \
  /usr/share/doc-base \
  && python --version \
  && pip freeze

###############################
## Begin JAVA and SPARK installation
###############################
# Java is required in order to spark-submit work
ENV SPARK_HOME /usr/local/spark

RUN mkdir -p /usr/share/man/man1 /usr/share/man/man2

RUN apt-get update -yqq \ 
  && apt-get install -yqq \
  openjdk-11-jdk \
  openjdk-11-jre \
  mlocate \
  curl \
  wget \
  procps \
  && cd "/tmp" \
  && wget https://dlcdn.apache.org/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz \
  && tar -xvzf spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz \
  && mkdir -p ${SPARK_HOME}/bin \
  && mkdir -p ${SPARK_HOME}/assembly/target/scala-2.12/jars \
  && cp -a spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}/bin/. ${SPARK_HOME}/bin/ \
  && cp -a spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}/jars/. ${SPARK_HOME}/assembly/target/scala-2.12/jars/ \
  && rm spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz \
  && apt-get clean \
  && rm -rf \
  /var/lib/apt/lists/* \
  /tmp/* \
  /var/tmp/* \
  /usr/share/man \
  /usr/share/doc \
  /usr/share/doc-base \
  && java --version

###############################
## Finish JAVA installation
###############################

COPY entrypoint.sh /entrypoint.sh

# Create SPARK_HOME env var
RUN export SPARK_HOME
ENV PATH $PATH:/usr/local/spark/bin

###############################
## Finish SPARK files and variables
###############################
COPY dags ${AIRFLOW_HOME}/airflow/dags

RUN chown -R airflow ${AIRFLOW_HOME}
RUN chmod +x entrypoint.sh

EXPOSE 8080 5555 8793

USER airflow
WORKDIR ${AIRFLOW_HOME}
ENTRYPOINT ["/entrypoint.sh"]
CMD ["webserver"] # set default arg for entrypoint