FROM corecdimage.inhuawei.com/lobechat/lobechatbackend:v16

# VARIABLE DEFINITION
MAINTAINER haotao h30063356 <haotao6@h-partners.com>
LABEL name="lobechatservice"
LABEL port=8000


USER root
# CUSTOM
RUN mkdir -p /usr/src/lobechatservice
COPY ./ /usr/src/lobechatservice/
WORKDIR /usr/src/lobechatservice
RUN chmod 777 /usr/local/bin/python

# 公开 8000 端口
EXPOSE 8000

# 默认命令启动 Flask 应用
CMD ["/usr/local/bin/python", "run.py"]