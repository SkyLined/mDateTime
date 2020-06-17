from fTestDependencies import fTestDependencies;
fTestDependencies();

from mDebugOutput import fEnableDebugOutputForClass, fEnableDebugOutputForModule, fTerminateWithException;
try:
  #Import the test subject
  from fTestDate import fTestDate;
  from fTestTime import fTestTime;
  from fTestDateTime import fTestDateTime;

  fTestDate();
  fTestTime();
  fTestDateTime();
  print "  + All tests successful.";
except Exception as oException:
  fTerminateWithException(oException, bShowStacksForAllThread = True);
