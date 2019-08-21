@ECHO OFF
SETLOCAL
REM Try to detect the location of python automatically
SET PYTHON=
FOR /F "usebackq delims=" %%I IN (`where "python" 2^>nul`) DO (
  SET PYTHON="%%~I"
  GOTO :FOUND_PYTHON
)

REM Check if python is found in its default installation path.
IF NOT EXIST "%SystemDrive%\Python27\python.exe" (
  SET PYTHON="%SystemDrive%\Python27\python.exe"
)
:FOUND_PYTHON

SET PHP=
REM Try to detect the location of PHP automatically
FOR /F "usebackq delims=" %%I IN (`where "php" 2^>nul`) DO (
  SET PHP="%%~I"
  GOTO :FOUND_PHP
)
:FOUND_PHP

IF DEFINED PYTHON (
  ECHO * Testing Python...
  CALL %PYTHON% "%~dp0\Tests\Tests.py" %*
  IF ERRORLEVEL 1 (ENDLOCAL & EXIT /B 1)
) ELSE (
  ECHO - Cannot find python.exe.
)
IF DEFINED PHP (
  ECHO * Testing PHP...
  CALL %PHP% "%~dp0\Tests\Tests.php" %*
  IF ERRORLEVEL 1 (ENDLOCAL & EXIT /B 1)
) ELSE (
  ECHO - Cannot find php.exe.
)
EXIT /B %ERRORLEVEL%
