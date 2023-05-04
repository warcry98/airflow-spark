FROM python:3.10-slim

# Never prompt the user for choices on installation/configuration on packages
ENV DEBIAN_FRONTEND noninteractive
ENV TERM linux

# Spark and Hadoop
ARG SPARK_VERSION=3.2.4
ARG HADOOP_VERSION=3.2
ARG PYTHONHASHSEED=1

###############################
## Begin JAVA and SPARK installation
###############################
# Java is required in order to spark-submit work
ENV SPARK_HOME=/usr/local/spark

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
  && mkdir -p ${SPARK_HOME} \
  && tar -xvzf spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz -C ${SPARK_HOME} --strip-components=1 \
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

WORKDIR ${SPARK_HOME}

ENV SPARK_MASTER_PORT=7077
ENV SPARK_MASTER_WEBUI_PORT=8181
ENV SPARK_LOG_DIR=${SPARK_HOME}/logs
ENV SPARK_MASTER_LOG=${SPARK_HOME}/logs/spark-master.out
ENV SPARK_WORKER_LOG=${SPARK_HOME}/logs/spark-worker.out
ENV SPARK_WORKER_WEBUI_PORT=8181
ENV SPARK_MASTER_URL=spark://spark:7077
ENV SPARK_MODE=master

EXPOSE 8181 7077 7000

RUN mkdir -p ${SPARK_LOG_DIR} \
  && touch ${SPARK_MASTER_LOG} \
  && touch ${SPARK_WORKER_LOG} \
  && ln -sf /dev/stdout ${SPARK_MASTER_LOG} \
  && ln -sf /dev/stdout ${SPARK_WORKER_LOG}

COPY start-spark.sh /
RUN chmod +x /start-spark.sh

CMD [ "/bin/bash", "/start-spark.sh" ]