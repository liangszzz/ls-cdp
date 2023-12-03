FROM amazon/aws-glue-libs:glue_libs_4.0.0_image_01
LABEL authors="liang"

USER root

ADD .aws /home/glue_user/.aws

ENV PYTHONPATH: /home/glue_user/aws-glue-libs/PyGlue.zip:/home/glue_user/spark/python/lib/py4j-0.10.9-src.zip:/home/glue_user/spark/python/
ENV HADOOP_CONF_DIR: /home/glue_user/spark/conf
ENV LD_LIBRARY_PATH: /home/glue_user/native_libs/amd64/hadoop-lzo-native:/home/glue_user/native_libs/amd64/hadoop-native/
ENV LOCALSTACK_HOSTNAME: localstack
ENV LOCALSTACK_PORT: 4566
ENV AWS_DEFAULT_REGION: ap-northeast-1
ENV AWS_ACCESS_KEY_ID: test
ENV AWS_SECRET_ACCESS_KEY: test
ENV DEFAULT_REGION: ap-northeast-1

EXPOSE 22
EXPOSE 8080
EXPOSE 18080
EXPOSE 4040
EXPOSE 8443
EXPOSE 8888
EXPOSE 8998

USER glue_user

COPY . /home/glue_user/workspace/jupyter_workspace

WORKDIR /home/glue_user/workspace/jupyter_workspace/fj-cdp
RUN python3 -m pip install --upgrade pip
RUN pip install poetry

RUN mkdir .checks
RUN poetry install -v