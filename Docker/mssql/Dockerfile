# mssql-server-linux
# Maintainers: Microsoft Corporation (LuisBosquez and twright-msft on GitHub)
# GitRepo: https://github.com/Microsoft/mssql-docker

# Base OS layer: Latest Ubuntu LTS.
FROM microsoft/mssql-server-linux

# 设置证书
ENV ACCEPT_EULA Y

# 设置sa帐户的密码
ENV SA_PASSWORD SqlServer.

# Default SQL Server TCP/Port.
EXPOSE 1433

# Copy all SQL Server runtime files from build drop into image.
#COPY ./data /data

# 挂载一个数据卷，用于放置脚本和备份数据
VOLUME /data

# Run SQL Server process.
CMD /opt/mssql/bin/sqlservr.sh