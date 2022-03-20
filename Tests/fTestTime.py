#Import the test subject
import mDateTime;

def fMustBeEqual(xValue1, xValue2, sErrorMessage):
  if not (
    (isinstance(xValue1, mDateTime.cTime) or isinstance(xValue1, mDateTime.cTimeDuration))
    and (isinstance(xValue2, mDateTime.cTime) or isinstance(xValue2, mDateTime.cTimeDuration))
    and str(xValue1) == str(xValue2)
    and xValue1 == xValue2
  ):
    raise AssertionError(sErrorMessage);

def fTimePlusDurationMustEqual(sStartTime, sDuration, sExpectedHumanReadableDuration, sExpectedEndTime,
  iExpectedOverflowedDays = 0,
  sExpectedNormalizedDuration = None,
  sExpectedNormalizedHumanReadableDuration = None,
  sExpectedCalculatedDuration = None
):
  sExpectedNormalizedDuration = sExpectedNormalizedDuration if sExpectedNormalizedDuration is not None else sDuration;
  sExpectedNormalizedHumanReadableDuration = sExpectedNormalizedHumanReadableDuration if sExpectedNormalizedHumanReadableDuration is not None else sExpectedHumanReadableDuration;
  sExpectedCalculatedDuration = sExpectedCalculatedDuration if sExpectedCalculatedDuration is not None else sExpectedNormalizedDuration;
  oStartTime = mDateTime.cTime.foFromString(sStartTime);
  oDuration = mDateTime.cTimeDuration.foFromString(sDuration);
  
  sHumanReadableDuration = oDuration.fsToHumanReadableString();
  assert sHumanReadableDuration == sExpectedHumanReadableDuration, \
      "cTimeDuration(%s).fsToHumanReadableString() == %s (NOT %s)" % (sDuration, sHumanReadableDuration, sExpectedHumanReadableDuration)

  oEndTime, iOverflowedDays = oStartTime.ftxGetEndTimeAndOverflowedDaysForDuration(oDuration);
  assert iOverflowedDays == iExpectedOverflowedDays, \
      "iOverflowedDays == %d (NOT %d)" % (iOverflowedDays, iExpectedOverflowedDays);
  sEndTime = str(oEndTime);
  assert sEndTime == sExpectedEndTime, \
      "sEndTime == %s (NOT %s)" % (sEndTime, sExpectedEndTime);
  
  oNormalizedDuration = oDuration.foNormalized();
  sNormalizedDuration = str(oNormalizedDuration);
  assert sNormalizedDuration == sExpectedNormalizedDuration, \
      "sNormalizedDuration == %s (NOT %s)" % (sNormalizedDuration, sExpectedNormalizedDuration);
  sNormalizedHumanReadableDuration = oNormalizedDuration.fsToHumanReadableString();
  assert sNormalizedHumanReadableDuration == sExpectedNormalizedHumanReadableDuration, \
      "sNormalizedHumanReadableDuration == %s (NOT %s)" % (sNormalizedHumanReadableDuration, sExpectedNormalizedHumanReadableDuration);
  
  oCalculatedDuration = oStartTime.foGetDurationForEndTime(oEndTime);
  sCalculatedDuration = str(oCalculatedDuration);
  assert sCalculatedDuration == sExpectedCalculatedDuration or sExpectedNormalizedDuration, \
      "sCalculatedDuration == %s (NOT %s)" % (sCalculatedDuration, sExpectedNormalizedDuration);

def fNormalizedDurationMustEqual(sDuration, sNormalizedDuration, nTotalInSeconds):
  oNormalizedDuration = mDateTime.cTimeDuration.foFromString(sDuration).foNormalized();
  fMustBeEqual(
    oNormalizedDuration,
    mDateTime.cTimeDuration.foFromString(sNormalizedDuration),
    "%s normalized == %s (NOT %s)" % (sDuration, oNormalizedDuration, sNormalizedDuration)
  );
  assert oNormalizedDuration.fnGetTotalSeconds() == nTotalInSeconds, \
      "%s in seconds == %s instead of %s" % (oNormalizedDuration, oNormalizedDuration.fnGetTotalSeconds(), nTotalInSeconds);

def fTestTime():
  print("  * Testing cTime/cTimeDuration...");
  fTimePlusDurationMustEqual("20:01:01", "+1h",     "1 hour",         "21:01:01");
  fTimePlusDurationMustEqual("20:01:01", "+60m",    "60 minutes",     "21:01:01",         0, "+1h",         "1 hour");
  fTimePlusDurationMustEqual("20:01:01", "+3600s",  "3600 seconds",   "21:01:01",         0, "+1h",         "1 hour");
  fTimePlusDurationMustEqual("21:01:01", "+1h",     "1 hour",         "22:01:01");
  fTimePlusDurationMustEqual("21:01:01", "+61m",    "61 minutes",     "22:02:01",         0, "+1h+1m",      "1 hour and 1 minute");
  fTimePlusDurationMustEqual("21:01:01", "+3661s",  "3661 seconds",   "22:02:02",         0, "+1h+1m+1s",   "1 hour, 1 minute, and 1 second");
  fTimePlusDurationMustEqual("20:01:01", "+59m+59s", "59 minutes and 59 seconds", \
                                                                      "21:01:00");
  fTimePlusDurationMustEqual("20:01:01", "+1u",     "1 microsecond",  "20:01:01.000001");
  fTimePlusDurationMustEqual("20:01:01", "+1000u",  "1 millisecond",  "20:01:01.001");
  fTimePlusDurationMustEqual("20:01:01.01", "+101u", "101 microseconds", \
                                                                      "20:01:01.010101");
  fTimePlusDurationMustEqual("20:01:01.001001", "+1001u", "1 millisecond and 1 microsecond", \
                                                                      "20:01:01.002002");
  fTimePlusDurationMustEqual("20:01:01.000001", "+999999u", "999 milliseconds and 999 microseconds", \
                                                                      "20:01:02");
  fTimePlusDurationMustEqual("20:01:01.000001", "+24h+60m+60s+1000000u", "24 hours, 60 minutes, 60 seconds, and 1000 milliseconds", \
                                                                      "21:02:02.000001",  1, "+25h+1m+1s",  "25 hours, 1 minute, and 1 second", "+1h+1m+1s");
  fNormalizedDurationMustEqual("1s1u", "+1s+1u", 1.000001);
  fNormalizedDurationMustEqual("1m1s1u", "+1m+1s+1u", 61.000001);
  fNormalizedDurationMustEqual("1h1m1s1u", "+1h+1m+1s+1u", 3661.000001);
  fNormalizedDurationMustEqual("+1h+60m+3600s+3600000000u", "+4h", 14400);
  
  print("    + All tests successful.");
