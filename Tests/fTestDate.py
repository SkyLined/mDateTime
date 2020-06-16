#Import the test subject
import mDateTime;

def fMustBeEqual(xValue1, xValue2, sErrorMessage):
  if not (
    (isinstance(xValue1, mDateTime.cDate) or isinstance(xValue1, mDateTime.cDateDuration))
    and (isinstance(xValue2, mDateTime.cDate) or isinstance(xValue2, mDateTime.cDateDuration))
    and str(xValue1) == str(xValue2)
  ):
    raise Exception(sErrorMessage);

def fDatePlusDurationMustEqual(sStartDate, sDuration, sExpectedHumanReadableDuration, sEndDate, sNormalizedDuration = None):
  oStartDate = mDateTime.cDate.foFromString(sStartDate);
  oDuration = mDateTime.cDateDuration.foFromString(sDuration);
  sHumanReadableDuration = oDuration.fsToHumanReadableString();
  oEndDate = mDateTime.cDate.foFromString(sEndDate);
  oCalculatedEndDate = oStartDate.foGetEndDateForDuration(oDuration);
  oCalculatedDuration = oStartDate.foGetDurationForEndDate(oEndDate);
  oNormalizedDuration = oDuration.foNormalizedForDate(oStartDate);
  if (sHumanReadableDuration != sExpectedHumanReadableDuration):
    raise Exception(
      "cDateDuration(%s).fsToHumanReadableString() == %s (NOT %s)" % (sDuration, sHumanReadableDuration, sExpectedHumanReadableDuration)
    );
  fMustBeEqual(
    oEndDate,
    oCalculatedEndDate,
    "%s + %s == %s (NOT %s)" % (sStartDate, sDuration, oCalculatedEndDate, sEndDate)
  );
  fMustBeEqual(
    oCalculatedDuration,
    oNormalizedDuration,
    "%s -> %s == %s (NOT %s)" % (sStartDate, sEndDate, oCalculatedDuration, oNormalizedDuration)
  );
  if (sNormalizedDuration and sNormalizedDuration != str(oNormalizedDuration)):
    raise Exception("%s -> %s == %s (NOT %s)" % (sStartDate, sEndDate, oNormalizedDuration, sNormalizedDuration));

def fNormalizedDurationForDateMustEqual(sDuration, sDate, sNormalizedDuration):
  oNormalizedDuration = mDateTime.cDateDuration.foFromString(sDuration).foNormalizedForDate(mDateTime.cDate.foFromString(sDate));
  fMustBeEqual(
    oNormalizedDuration,
    mDateTime.cDateDuration.foFromString(sNormalizedDuration),
    "%s normalized for %s == %s (NOT %s)" % (sDuration, sDate, oNormalizedDuration, sNormalizedDuration)
  );

def fTestDate():
  print "  * Testing cDate/cDateDuration...";
  fDatePlusDurationMustEqual("2000-01-01", "+1y",   "1 year",     "2001-01-01");
  fDatePlusDurationMustEqual("2000-01-01", "+12m",  "12 months",  "2001-01-01");
  fDatePlusDurationMustEqual("2000-01-01", "+366d", "366 days",   "2001-01-01"); # 2000 is a leap year.
  fDatePlusDurationMustEqual("2001-01-01", "+1y",   "1 year",     "2002-01-01");
  fDatePlusDurationMustEqual("2001-01-01", "+12m",  "12 months",  "2002-01-01");
  fDatePlusDurationMustEqual("2001-01-01", "+365d", "365 days",   "2002-01-01"); # 2001 is not a leap year.

  fDatePlusDurationMustEqual("2000-02-01", "+28d", "28 days", "2000-02-29"); # 2000 is a leap year.
  fDatePlusDurationMustEqual("2000-02-01", "+29d", "29 days", "2000-03-01"); # 2000 is a leap year.
  fDatePlusDurationMustEqual("2001-02-01", "+28d", "28 days", "2001-03-01"); # 2001 is not a leap year.
  fDatePlusDurationMustEqual("2000-01-01", "+1y+1m+28d", "1 year, 1 month, and 28 days", "2001-03-01"); # 2001 is not a leap year; days are applied last.

  fDatePlusDurationMustEqual("2000-01-01", "+1m", "1 month", "2000-02-01");
  fDatePlusDurationMustEqual("2000-01-01", "+31d", "31 days", "2000-02-01");

  fDatePlusDurationMustEqual("2000-01-01", "+1d", "1 day", "2000-01-02");

  fDatePlusDurationMustEqual("2000-01-01", "+1y1m1d", "1 year, 1 month, and 1 day", "2001-02-02");

  fNormalizedDurationForDateMustEqual("1y1m1d", "2000-01-01", "1y1m1d");
  fNormalizedDurationForDateMustEqual("+1y-1m+31d", "2000-01-01", "1y");
  fNormalizedDurationForDateMustEqual("+2 years, -12 months, -366 day", "2000-01-01", "0d");

  # Check day/month is adjusted if needed when months are added to potentially overflow the day.
  fDatePlusDurationMustEqual("2000-01-30", "1m", "1 month", "2000-02-29", "+30d");
  fDatePlusDurationMustEqual("2001-01-30", "1m", "1 month", "2001-02-28", "+29d");
  fDatePlusDurationMustEqual("2001-01-29", "1m", "1 month", "2001-02-28", "+30d");
  fDatePlusDurationMustEqual("2001-01-28", "1m", "1 month", "2001-02-28", "+1m");

  oTestDate = mDateTime.cDate(2000, 2, 28);
  oFromStringTestDate = mDateTime.cDate.foFromString("2000-02-28");
  oFromJSONTestDate = mDateTime.cDate.foFromJSON("2000-02-28");
  oClonedTestDate = oTestDate.foClone();
  fMustBeEqual(oTestDate, oFromStringTestDate, "cDate.foFromString(\"2000-02-28\") should not result in %s" % oFromStringTestDate);
  fMustBeEqual(oTestDate, oFromJSONTestDate, "cDate.foFromJSON(\"2000-02-28\") should not result in %s" % oFromJSONTestDate);
  fMustBeEqual(oTestDate, oClonedTestDate, "%s should not be cloned as %s" % (oTestDate, oClonedTestDate));

  oTestDate.uDay = 29;
  try:
    oTestDate.uYear = 2001;
  except Exception:
    pass;
  else:
    raise AssertionError("%s should not be possible." % oTestDate);

  oTestDate.uDay = 28;
  oTestDate.uYear = 2001;
  try:
    oTestDate.uDay = 29;
  except Exception:
    pass;
  else:
    raise AssertionError("%s should not be possible." % oTestDate);

  oTestDate.uMonth = 1;
  oTestDate.uDay = 29;
  try:
    oTestDate.uMonth = 2;
  except Exception:
    pass;
  else:
    raise AssertionError("%s should not be possible." % oTestDate);

  def fCompareDates(oDate1, sResults, oDate2):
    if sResults == "IsBefore":
      if not oDate1.fbIsBefore(oDate2): raise AssertionError("%s should be before %s." % (oDate1, oDate2));
    else:
      if oDate1.fbIsBefore(oDate2): raise AssertionError("%s should not be before %s." % (oDate1, oDate2));
    if sResults == "IsEqualTo":
      if not oDate1.fbIsEqualTo(oDate2): raise AssertionError("%s should be equal to %s." % (oDate1, oDate2));
    else:
      if oDate1.fbIsEqualTo(oDate2): raise AssertionError("%s should not be equal to %s." % (oDate1, oDate2));
    if sResults == "IsAfter":
      if not oDate1.fbIsAfter(oDate2): raise AssertionError("%s should be after %s." % (oDate1, oDate2));
    else:
      if oDate1.fbIsAfter(oDate2): raise AssertionError("%s should not be after %s." % (oDate1, oDate2));

  oDate1 = mDateTime.cDate(2000, 1, 1);
  oDate2 = mDateTime.cDate(2000, 1, 2);
  oDate3 = mDateTime.cDate(2000, 2, 1);
  oDate4 = mDateTime.cDate(2001, 1, 1);
  fCompareDates(oDate1, "IsEqualTo", oDate1);  
  fCompareDates(oDate1, "IsBefore", oDate2);  
  fCompareDates(oDate1, "IsBefore", oDate3);  
  fCompareDates(oDate1, "IsBefore", oDate4);  

  fCompareDates(oDate2, "IsAfter", oDate1);  
  fCompareDates(oDate2, "IsEqualTo", oDate2);  
  fCompareDates(oDate2, "IsBefore", oDate3);  
  fCompareDates(oDate2, "IsBefore", oDate4);  

  fCompareDates(oDate3, "IsAfter", oDate1);  
  fCompareDates(oDate3, "IsAfter", oDate2);  
  fCompareDates(oDate3, "IsEqualTo", oDate3);  
  fCompareDates(oDate3, "IsBefore", oDate4);  

  fCompareDates(oDate4, "IsAfter", oDate1);  
  fCompareDates(oDate4, "IsAfter", oDate2);  
  fCompareDates(oDate4, "IsAfter", oDate3);  
  fCompareDates(oDate4, "IsEqualTo", oDate4);  

  print "    + All tests successful.";
