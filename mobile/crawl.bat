@echo off & color 02
echo 请输入要查询的7位联通手机号段：
set /p phoneNo=
Z:
cd Z:\projects\envs\mobile\mobile 
cmd /k "workon crawl && python main.py %phoneNo%"



