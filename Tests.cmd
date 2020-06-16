@ECHO OFF
IF "%~1" == "" (
  CALL :TEST_PYTHON IGNORE
  IF ERRORLEVEL 1 GOTO :ERROR
  CALL :TEST_PHP IGNORE
  IF ERRORLEVEL 1 GOTO :ERROR
  CALL :TEST_NODE IGNORE
  IF ERRORLEVEL 1 GOTO :ERROR
) ELSE IF "%~1" == "--python" (
  CALL :TEST_PYTHON
  IF ERRORLEVEL 1 GOTO :ERROR
) ELSE IF "%~1" == "--php" (
  CALL :TEST_PHP
  IF ERRORLEVEL 1 GOTO :ERROR
) ELSE IF "%~1" == "--node" (
  CALL :TEST_NODE
  IF ERRORLEVEL 1 GOTO :ERROR
) ELSE (
  ECHO Unknown argument %1
  ECHO Usage: Tests.cmd [--python^|--php^|--node]
  EXIT /B 0
)
EXIT /B 0

:TEST_PYTHON
  SETLOCAL
  IF NOT DEFINED PYTHON (
    REM Try to detect the location of python automatically
    FOR /F "usebackq delims=" %%I IN (`where "python" 2^>nul`) DO (
      SET PYTHON="%%~I"
      GOTO :FOUND_PYTHON
    )

    REM Check if python is found in its default installation path.
    IF EXIST "%SystemDrive%\Python27\python.exe" (
      SET PYTHON="%SystemDrive%\Python27\python.exe"
      GOTO :FOUND_PYTHON
    )
    ECHO - Cannot find python.exe.
    ENDLOCAL
    IF NOT "%~1" == "IGNORE" EXIT /B 1
    EXIT /B 0
  )
:FOUND_PYTHON
  ECHO * Testing Python...
  CALL %PYTHON% "%~dp0\Tests\Tests.py" %*
  ENDLOCAL & EXIT /B %ERRORLEVEL%

:TEST_PHP
  SETLOCAL
  IF NOT DEFINED PHP (
    REM Try to detect the location of PHP automatically
    FOR /F "usebackq delims=" %%I IN (`where "php" 2^>nul`) DO (
      SET PHP="%%~I"
      GOTO :FOUND_PHP
    )
    ECHO - Cannot find php.exe.
    ENDLOCAL
    IF NOT "%~1" == "IGNORE" EXIT /B 1
    EXIT /B 0
  )
:FOUND_PHP
  ECHO * Testing PHP...
  CALL %PHP% "%~dp0\Tests\Tests.php" %*
  ENDLOCAL & EXIT /B %ERRORLEVEL%


:ERROR
  ECHO - Error %ERRORLEVEL%!
  EXIT /B %ERRORLEVEL%
