@echo off
chcp 65001 >nul 2>&1

:: 设置Python脚本的完整路径
set "PYTHON_SCRIPT=D:\vscode_project\my-knowledge-base\upload_with_llm.py"

:: 检查脚本文件是否存在
if not exist "%PYTHON_SCRIPT%" (
    echo 错误：未找到Python脚本文件！
    echo 路径：%PYTHON_SCRIPT%
    pause
    exit /b 1
)

:: 运行Python脚本
echo 正在运行Python脚本：%PYTHON_SCRIPT%
echo ----------------------------------------
python "%PYTHON_SCRIPT%"

:: 脚本运行结束后的处理
echo ----------------------------------------
echo 脚本运行完成！
pause