FROM amazon/aws-glue-libs:glue_libs_4.0.0_image_01
LABEL authors="liang"

USER root

RUN yum update -y

RUN yum install -y openssh-server && yum install -y passwd && yum install -y openssh-clients
RUN yum install -y libxslt-devel libxml2-devel
RUN yum clean all
ADD doc/docker-for-dev/ssh_file/ssh_host_ecdsa_key /etc/ssh/ssh_host_ecdsa_key
ADD doc/docker-for-dev/ssh_file/ssh_host_ed25519_key /etc/ssh/ssh_host_ed25519_key
ADD doc/docker-for-dev/ssh_file/ssh_host_rsa_key /etc/ssh/ssh_host_rsa_key
ADD doc/docker-for-dev/ssh_file/ssh_host_ecdsa_key.pub /etc/ssh/ssh_host_ecdsa_key.pub
ADD doc/docker-for-dev/ssh_file/ssh_host_ed25519_key.pub /etc/ssh/ssh_host_ed25519_key.pub
ADD doc/docker-for-dev/ssh_file/ssh_host_rsa_key.pub /etc/ssh/ssh_host_rsa_key.pub

RUN chmod 644 /etc/ssh/*

ADD doc/docker-for-dev/ssh_file/sshd_config /etc/ssh/sshd_config

RUN chmod 644 /etc/ssh/sshd_config

ADD doc/docker-for-dev/shell/run_sshd.sh /usr/local/sbin/run_sshd.sh
RUN chmod +x /usr/local/sbin/run_sshd.sh

RUN echo 'root:123456' | chpasswd
RUN echo 'glue_user:123456' | chpasswd

ENV PYTHONPATH: /home/glue_user/aws-glue-libs/PyGlue.zip:/home/glue_user/spark/python/lib/py4j-0.10.9-src.zip:/home/glue_user/spark/python/
ENV HADOOP_CONF_DIR: /home/glue_user/spark/conf
ENV LD_LIBRARY_PATH: /home/glue_user/native_libs/amd64/hadoop-lzo-native:/home/glue_user/native_libs/amd64/hadoop-native/
ENV LOCALSTACK_HOSTNAME: localstack
ENV LOCALSTACK_PORT: 4566
ENV AWS_DEFAULT_REGION: ap-northeast-1
ENV AWS_ACCESS_KEY_ID: test
ENV AWS_SECRET_ACCESS_KEY: test
ENV DEFAULT_REGION: ap-northeast-1

COPY . /home/glue_user/workspace/ls-cdp
RUN chown -R glue_user /home/glue_user/workspace/ls-cdp
USER glue_user

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -U poetry

WORKDIR /home/glue_user/workspace/ls-cdp
#
RUN ~/.local/bin/poetry install -v
##
RUN aws configure set aws_access_key_id "test" --profile default && aws configure set aws_secret_access_key "test" --profile default && aws configure set region "ap-northeast-1" --profile default && aws configure set output "text" --profile default
RUN chmod +x shell/dev/*.sh
RUN mkdir .checks

CMD ["/usr/local/sbin/run_sshd.sh"]