@echo off & color 02
echo ������Ҫ��ѯ��7λ��ͨ�ֻ��ŶΣ�
set /p phoneNo=
Z:
cd Z:\projects\envs\mobile\mobile 
cmd /k "workon crawl && python main.py %phoneNo%"



