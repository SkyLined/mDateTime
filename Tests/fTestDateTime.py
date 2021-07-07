#Import the test subject
import mDateTime;

def fMustBeEqual(xValue1, xValue2, sErrorMessage):
  if not (
    (isinstance(xValue1, mDateTime.cDateTime) or isinstance(xValue1, mDateTime.cDateTimeDuration))
    and (isinstance(xValue2, mDateTime.cDateTime) or isinstance(xValue2, mDateTime.cDateTimeDuration))
    and str(xValue1) == str(xValue2)
  ):
    raise AssertionError(sErrorMessage);

def fDateTimePlusDurationMustEqual(sStartDateTime, sDuration, sExpectedHumanReadableDuration, sExpectedEndDateTime,
  sExpectedNormalizedDuration = None,
  sExpectedNormalizedHumanReadableDuration = None,
  sExpectedCalculatedDuration = None
):
  sExpectedNormalizedDuration = sExpectedNormalizedDuration if sExpectedNormalizedDuration is not None else sDuration;
  sExpectedNormalizedHumanReadableDuration = sExpectedNormalizedHumanReadableDuration if sExpectedNormalizedHumanReadableDuration is not None else sExpectedHumanReadableDuration;
  sExpectedCalculatedDuration = sExpectedCalculatedDuration if sExpectedCalculatedDuration is not None else sExpectedNormalizedDuration;
  oStartDateTime = mDateTime.cDateTime.foFromString(sStartDateTime);
  oDuration = mDateTime.cDateTimeDuration.foFromString(sDuration);
  
  sHumanReadableDuration = oDuration.fsToHumanReadableString();
  assert sHumanReadableDuration == sExpectedHumanReadableDuration, \
      "cDateTimeDuration(%s).fsToHumanReadableString() == %s (NOT %s)" % (sDuration, sHumanReadableDuration, sExpectedHumanReadableDuration)

  oEndDateTime = oStartDateTime.foGetEndDateTimeForDuration(oDuration);
  sEndDateTime = str(oEndDateTime);
  assert sEndDateTime == sExpectedEndDateTime, \
      "sEndDateTime == %s (NOT %s)" % (sEndDateTime, sExpectedEndDateTime);
  
  oNormalizedDuration = oDuration.foNormalizedForDate(oStartDateTime);
  sNormalizedDuration = str(oNormalizedDuration);
  assert sNormalizedDuration == sExpectedNormalizedDuration, \
      "sNormalizedDuration == %s (NOT %s)" % (sNormalizedDuration, sExpectedNormalizedDuration);
  sNormalizedHumanReadableDuration = oNormalizedDuration.fsToHumanReadableString();
  assert sNormalizedHumanReadableDuration == sExpectedNormalizedHumanReadableDuration, \
      "sNormalizedHumanReadableDuration == %s (NOT %s)" % (sNormalizedHumanReadableDuration, sExpectedNormalizedHumanReadableDuration);
  
  oCalculatedDuration = oStartDateTime.foGetDurationForEndDateTime(oEndDateTime);
  sCalculatedDuration = str(oCalculatedDuration);
  assert sCalculatedDuration == sExpectedCalculatedDuration or sExpectedNormalizedDuration, \
      "sCalculatedDuration == %s (NOT %s)" % (sCalculatedDuration, sExpectedNormalizedDuration);

def fNormalizedDurationMustEqual(sDuration, sNormalizedDuration):
  oNormalizedDuration = mDateTime.cDateTimeDuration.foFromString(sDuration).foNormalized();
  fMustBeEqual(
    oNormalizedDuration,
    mDateTime.cDateTimeDuration.foFromString(sNormalizedDuration),
    "%s normalized == %s (NOT %s)" % (sDuration, oNormalizedDuration, sNormalizedDuration)
  );

def fTestDateTime():
  print("  * Testing cDateTime/cDateTimeDuration...");
  fDateTimePlusDurationMustEqual("2000-01-01 20:01:01", "+1y/+1h",      "1 year and 1 hour",          "2001-01-01 21:01:01");
  fDateTimePlusDurationMustEqual("2000-01-01 20:01:01", "+12m/+60m",    "12 months and 60 minutes",   "2001-01-01 21:01:01",  "+1y/+1h",         "1 year and 1 hour");
  fDateTimePlusDurationMustEqual("2000-01-01 20:01:01", "+366d/+3600s", "366 days and 3600 seconds",  "2001-01-01 21:01:01",  "+1y/+1h",         "1 year and 1 hour");
  fDateTimePlusDurationMustEqual("2001-01-01 21:01:01", "+1y/+1h",      "1 year and 1 hour",          "2002-01-01 22:01:01");
  fDateTimePlusDurationMustEqual("2001-01-01 21:01:01", "+13m/+61m",    "13 months and 61 minutes",   "2002-02-01 22:02:01",  "+1y+1m/+1h+1m",   "1 year, 1 month, 1 hour, and 1 minute");
  fDateTimePlusDurationMustEqual("2001-01-01 21:01:01", "+397d/+3661s", "397 days and 3661 seconds",  "2002-02-02 22:02:02",  "+1y+1m+1d/+1h+1m+1s", "1 year, 1 month, 1 day, 1 hour, 1 minute, and 1 second");
  fDateTimePlusDurationMustEqual("2000-01-01 20:01:01", "+12m+32d/+23h+59m+59s", "12 months, 32 days, 23 hours, 59 minutes, and 59 seconds", \
                                                                                                      "2001-02-03 20:01:00",  "+1y+1m+1d/+23h+59m+59s", "1 year, 1 month, 1 day, 23 hours, 59 minutes, and 59 seconds");
  fDateTimePlusDurationMustEqual("2000-12-31 23:59:59.999999", "+1u",   "1 microsecond",              "2001-01-01 00:00:00");
  
  sDateTime = "2000-01-02 03:04:05.06";
  oDateTime = mDateTime.cDateTime.foFromString(sDateTime);
  assert str(oDateTime) == sDateTime, \
      "str(cDateTime.foFromString(%s)) == %s !?" % (repr(sDateTime), str(oDateTime));
  
  sISO8601UTCDateTime = "2000-01-02T03:04:05.06Z";
  oISO8601UTCDateTime = mDateTime.cDateTime.foFromString(sISO8601UTCDateTime);
  assert oISO8601UTCDateTime.fsToISO8601UTC() == sISO8601UTCDateTime, \
      "cDateTime.foFromString(%s).fsToISO8601UTC() == %s !?" % (repr(sISO8601UTCDateTime), oISO8601UTCDateTime.fsToISO8601UTC());
  assert str(oDateTime) == str(oISO8601UTCDateTime), \
      "cDateTime.foFromString(%s) == %s (NOT %s)" % (sDateTime, str(oDateTime), str(oISO8601UTCDateTime));
  
  fNormalizedDurationMustEqual("1y1m1d/1h1m1s1u", "+1y+1m+1d/+1h+1m+1s+1u");
  fNormalizedDurationMustEqual("1y+12m+366d/+21h+60m+3600s+3600000000u", "+2y+367d/0s");
  
  print("    + All tests successful.");
