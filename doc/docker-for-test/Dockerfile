FROM amazon/aws-glue-libs:glue_libs_4.0.0_image_01
LABEL authors="liang"

USER root

ENV PYTHONPATH: /home/glue_user/aws-glue-libs/PyGlue.zip:/home/glue_user/spark/python/lib/py4j-0.10.9-src.zip:/home/glue_user/spark/python/
ENV HADOOP_CONF_DIR: /home/glue_user/spark/conf
ENV LD_LIBRARY_PATH: /home/glue_user/native_libs/amd64/hadoop-lzo-native:/home/glue_user/native_libs/amd64/hadoop-native/
ENV LOCALSTACK_HOSTNAME: localstack
ENV LOCALSTACK_PORT: 4566
ENV AWS_DEFAULT_REGION: ap-northeast-1
ENV AWS_ACCESS_KEY_ID: test
ENV AWS_SECRET_ACCESS_KEY: test
ENV DEFAULT_REGION: ap-northeast-1

EXPOSE 8080
EXPOSE 18080
EXPOSE 4040
EXPOSE 8443
EXPOSE 8888
EXPOSE 8998

RUN python3 -m pip install --upgrade pip

COPY . /home/glue_user/workspace/ls-cdp
WORKDIR /home/glue_user/workspace/ls-cdp
RUN pip install -U poetry
RUN poetry install -v
RUN aws configure set aws_access_key_id "test" --profile default && aws configure set aws_secret_access_key "test" --profile default && aws configure set region "ap-northeast-1" --profile default && aws configure set output "text" --profile default
RUN chmod -R 755 shell/test/*.sh