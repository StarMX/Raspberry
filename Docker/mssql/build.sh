#生成镜像
docker build -t mssql .
#启动容器
docker run -d -v /(!绝对路径!)/mssqldata:/data mssql


