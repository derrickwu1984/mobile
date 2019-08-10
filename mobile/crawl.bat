@echo off & color 02
echo 请输入7位手机号号段
set /p phoneNo=
Z:
cd E:\projects\mobile\mobile
cmd /k "workon ess && python main.py %phoneNo%"



