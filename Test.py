from cDate import cDate;
from cDateDuration import cDateDuration;
def fMustBeEqual(xValue1, xValue2, sErrorMessage):
  if not (
    (isinstance(xValue1, cDate) or isinstance(xValue1, cDateDuration))
    and (isinstance(xValue2, cDate) or isinstance(xValue2, cDateDuration))
    and str(xValue1) == str(xValue2)
  ):
    raise Error(sErrorMessage);

def fDatePlustDurationMustEqual(sStartDate, sDuration, sEndDate):
  oStartDate = cDate.foFromString(sStartDate);
  oDuration = cDateDuration.foFromString(sDuration);
  oEndDate = cDate.foFromString(sEndDate);
  oCalculatedEndDate = oStartDate.foGetEndDateForDuration(oDuration);
  oCalculatedDuration = oStartDate.foGetDurationForEndDate(oEndDate);
  oNormalizedDuration = oDuration.foNormalizedForDate(oStartDate);
  fMustBeEqual(
    oEndDate,
    oCalculatedEndDate,
    "%s %s == %s (NOT %s)" % (sStartDate, sDuration, oCalculatedEndDate, sEndDate)
  );
  fMustBeEqual(
    oCalculatedDuration,
    oNormalizedDuration,
    "%s -> %s == %s (NOT %s)" % (sStartDate, sEndDate, oCalculatedDuration, oNormalizedDuration)
  );

def fNormalizedDurationForDateMustEqual(sDuration, sDate, sNormalizedDuration):
  oNormalizedDuration = cDateDuration.foFromString(sDuration).foNormalizedForDate(cDate.foFromString(sDate));
  fMustBeEqual(
    oNormalizedDuration,
    cDateDuration.foFromString(sNormalizedDuration),
    "%s normalized for %s == %s (NOT %s)" % (sDuration, sDate, oNormalizedDuration, sNormalizedDuration)
  );

fDatePlustDurationMustEqual("2000-01-01", "+1y", "2001-01-01");
fDatePlustDurationMustEqual("2000-01-01", "+12m", "2001-01-01");
fDatePlustDurationMustEqual("2000-01-01", "+366d", "2001-01-01"); # 2000 is a leap year.
fDatePlustDurationMustEqual("2001-01-01", "+1y", "2002-01-01");
fDatePlustDurationMustEqual("2001-01-01", "+12m", "2002-01-01");
fDatePlustDurationMustEqual("2001-01-01", "+365d", "2002-01-01"); # 2001 is not a leap year.

fDatePlustDurationMustEqual("2000-02-01", "+28d", "2000-02-29"); # 2000 is a leap year.
fDatePlustDurationMustEqual("2000-02-01", "+29d", "2000-03-01"); # 2000 is a leap year.
fDatePlustDurationMustEqual("2001-02-01", "+28d", "2001-03-01"); # 2001 is not a leap year.
fDatePlustDurationMustEqual("2000-01-01", "+1y+1m+28d", "2001-03-01"); # 2001 is not a leap year; days are applied last.

fDatePlustDurationMustEqual("2000-01-01", "+1m", "2000-02-01");
fDatePlustDurationMustEqual("2000-01-01", "+31d", "2000-02-01");

fDatePlustDurationMustEqual("2000-01-01", "+1d", "2000-01-02");

fDatePlustDurationMustEqual("2000-01-01", "+1y1m1d", "2001-02-02");

fNormalizedDurationForDateMustEqual("1y1m1d", "2000-01-01", "1y1m1d");
fNormalizedDurationForDateMustEqual("+1y-1m+31d", "2000-01-01", "1y");
fNormalizedDurationForDateMustEqual("+2 years, -12 months, -366 day", "2000-01-01", "0d");

oTestDate = cDate(2000, 2, 28);
oFromStringTestDate = cDate.foFromString("2000-02-28");
oFromJSONTestDate = cDate.foFromJSON("2000-02-28");
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

oDate1 = cDate(2000, 1, 1);
oDate2 = cDate(2000, 1, 2);
oDate3 = cDate(2000, 2, 1);
oDate4 = cDate(2001, 1, 1);
if not oDate1.fbIsEqualTo(oDate1): raise AssertionError("%s should be equal to itself." % oDate1);
if not oDate1.fbIsBefore(oDate2): raise AssertionError("%s should be before %s." % (oDate1, oDate2));
if not oDate1.fbIsBefore(oDate3): raise AssertionError("%s should be before %s." % (oDate1, oDate3));
if not oDate1.fbIsBefore(oDate4): raise AssertionError("%s should be before %s." % (oDate1, oDate4));

if not oDate2.fbIsAfter(oDate1): raise AssertionError("%s should be after %s." % (oDate2, oDate1));
if not oDate2.fbIsEqualTo(oDate2): raise AssertionError("%s should be equal to itself." % oDate2);
if not oDate2.fbIsBefore(oDate3): raise AssertionError("%s should be before %s." % (oDate2, oDate3));
if not oDate2.fbIsBefore(oDate4): raise AssertionError("%s should be before %s." % (oDate2, oDate4));

if not oDate3.fbIsAfter(oDate1): raise AssertionError("%s should be after %s." % (oDate3, oDate1));
if not oDate3.fbIsAfter(oDate2): raise AssertionError("%s should be after %s." % (oDate3, oDate2));
if not oDate3.fbIsEqualTo(oDate3): raise AssertionError("%s should be equal to itself." % oDate3);
if not oDate3.fbIsBefore(oDate4): raise AssertionError("%s should be before %s." % (oDate3, oDate4));

if not oDate4.fbIsAfter(oDate1): raise AssertionError("%s should be after %s." % (oDate4, oDate1));
if not oDate4.fbIsAfter(oDate2): raise AssertionError("%s should be after %s." % (oDate4, oDate2));
if not oDate4.fbIsAfter(oDate3): raise AssertionError("%s should be after %s." % (oDate4, oDate3));
if not oDate4.fbIsEqualTo(oDate4): raise AssertionError("%s should be equal to itself." % oDate4);


print "All tests successful.";