import datetime, re, time;

gbDebugOutput = False;

from .cDate import cDate;
from .cTime import cTime;

rISO8601UTCDateTime = re.compile(r"^\s*(\d{4})\-?(\d\d)-?(\d\d)T(\d\d):?(\d\d):?(\d\d)(\.\d+)?(?:Z|\+00:00)\s*$", re.I);

class cDateTime(cTime, cDate):
  # Static methods
  @staticmethod
  def foFromTimestamp(nTimestamp):
    uTimestamp = int(nTimestamp);
    oStructTime = time.localtime(uTimestamp);
    uMicroseconds = int((nTimestamp - uTimestamp) * 1000 * 1000);
    return cDateTime(
      oStructTime.tm_year, oStructTime.tm_mon, oStructTime.tm_mday,
      oStructTime.tm_hour, oStructTime.tm_min, oStructTime.tm_sec, uMicroseconds
    );
  
  @staticmethod
  def fo0FromPyDateTime(oDateTime):
    return None if oDateTime is None else cDateTime.foFromPyDateTime(oDateTime);
  @staticmethod
  def foFromPyDateTime(oDateTime):
    return cDateTime.foFromTimestamp(oDateTime.timestamp());
  
  @staticmethod
  def fo0FromJSON(s0DateTime):
    return None if s0DateTime is None else cDateTime.foFromJSON(s0DateTime);
  @staticmethod
  def foFromJSON(sDateTime):
    # JSON encoding uses the "string value" of cDateTime.
    return cDateTime.foFromString(sDateTime);
  
  @staticmethod
  def fo0FromMySQLDateTime(s0DateTime):
    return None if s0DateTime is None else cDateTime.foFromMySQLDateTime(s0DateTime);
  @staticmethod
  def foFromMySQLDateTime(sDateTime):
    # SQL encoding uses the "string value" of cDateTime.
    return cDateTime.foFromString(sDateTime);
  
  @staticmethod
  def fbIsValidDateTimeString(sDateTime):
    oISO8601UTCMatch = rISO8601UTCDateTime.match(sDateTime);
    if oISO8601UTCMatch:
      sYear, sMonth, sDay, sHour, sMinute, sSeconds, sFractionalSeconds = oISO8601UTCMatch.groups();
      tsDate_sTime = ("%s-%s-%s" % (sYear, sMonth, sDay), "%s:%s:%s%s" % (sHour, sMinute, sSeconds, sFractionalSeconds or ""));
    else:
      tsDate_sTime = sDateTime.split(" ");
    return (
      len(tsDate_sTime) == 2
      and cDate.fbIsValidDateString(tsDate_sTime[0])
      and cTime.fbIsValidTimeString(tsDate_sTime[1])
    );
  @staticmethod
  def fo0FromString(s0DateTime):
    return None if s0DateTime is None else cDateTime.foFromString(s0DateTime);
  
  @staticmethod
  def foFromString(sDateTime):
    oISO8601UTCMatch = rISO8601UTCDateTime.match(sDateTime);
    if oISO8601UTCMatch:
      sYear, sMonth, sDay, sHour, sMinute, sSeconds, sFractionalSeconds = oISO8601UTCMatch.groups();
      tsDate_sTime = ("%s-%s-%s" % (sYear, sMonth, sDay), "%s:%s:%s%s" % (sHour, sMinute, sSeconds, sFractionalSeconds or ""));
    else:
      tsDate_sTime = sDateTime.split(" ");
      if len(tsDate_sTime) != 2: raise ValueError("Invalid date+time string " + repr(sDateTime) + ".");
    oDate = cDate.foFromString(tsDate_sTime[0]);
    oTime = cTime.foFromString(tsDate_sTime[1]);
    return cDateTime.foFromDateAndTime(oDate, oTime);
  
  @staticmethod
  def foFromDateAndTime(oDate, oTime):
    return cDateTime(
      oDate.uYear, oDate.uMonth, oDate.uDay,
      oTime.uHour, oTime.uMinute, oTime.uSecond, oTime.uMicrosecond
    );
  
  @staticmethod
  def foNow():
    return cDateTime.foFromPyDateTime(datetime.datetime.now());
  @staticmethod
  def foNowUTC():
    return cDateTime.foFromPyDateTime(datetime.datetime.utcnow());
  # Constructor
  def __init__(oSelf, uYear, uMonth, uDay, uHour, uMinute, uSecond, uMicrosecond = 0):
    cDate.__init__(oSelf, uYear, uMonth, uDay);
    cTime.__init__(oSelf, uHour, uMinute, uSecond, uMicrosecond);
  # Methods
  def foClone(oSelf):
    return cDateTime(
      oSelf.uYear, oSelf.uMonth, oSelf.uDay,
      oSelf.uHour, oSelf.uMinute, oSelf.uSecond, oSelf.uMicrosecond
    );
  
  def fSet(oSelf, uYear = None, uMonth = None, uDay = None, uHour = None, uMinute = None, uSecond = None, uMicrosecond = None):
    cDate.fSet(oSelf, uYear, uMonth, uDay);
    cTime.fSet(oSelf, uHour, uMinute, uSecond, uMicrosecond);
  
  def foGetDate(oSelf):
    return cDate(oSelf.uYear, oSelf.uMonth, oSelf.uDay);
  
  def foGetTime(oSelf):
    return cTime(oSelf.uHour, oSelf.uMinute, oSelf.uSecond, oSelf.uMicrosecond);
  
  def foGetEndDateTimeForDuration(oSelf, oDuration):
    from .cDateDuration import cDateDuration;
    from .cTimeDuration import cTimeDuration;
    from .cDateTimeDuration import cDateTimeDuration;
    if isinstance(oDuration, cDateTimeDuration):
      oDateDuration = oTimeDuration = oDuration;
    elif isinstance(oDuration, cDateDuration):
      oDateDuration = oDuration;
      oTimeDuration = None;
    elif isinstance(oDuration, cTimeDuration):
      oDateDuration = None;
      oTimeDuration = oDuration;
    else:
      raise AssertionError("%s is not a duration" % repr(oDuration));
    # Aply time duration and apply overflowed days to date duration. The later 
    # is done on a copy so as not to modify the argument passed to this function.
    if oTimeDuration:
      # Found out how many days we will go forward/backwards base on time duration:
      oEndTime, iOverflowedDays = cTime.ftxGetEndTimeAndOverflowedDaysForDuration(oSelf, oTimeDuration);
      if iOverflowedDays:
        if oDateDuration:
          oDateDuration = oDateDuration.foClone();
          oDateDuration.iDays += iOverflowedDays;
        else:
          oDateDuration = cDateDuration(0, 0, iOverflowedDays);
    else:
      oEndTime = oSelf;
    # Apply date duration
    oEndDate = oSelf if not oDateDuration else cDate.foGetEndDateForDuration(oSelf, oDateDuration);
    return cDateTime.foFromDateAndTime(oEndDate, oEndTime);
  
  def foGetDurationForEndDateTime(oSelf, oEndDateTime):
    # If the end date is before the start date, reverse them, get the duration,
    # make it negative and return that. This allows us to assume oSelf >= oEndDateTime.
    if oEndDateTime.fbIsBefore(oSelf):
      oDuration = oEndDateTime.foGetDurationForEndDateTime(oSelf);
      oDuration.fNegative();
      if gbDebugOutput: print("=> return: %s" % oDuration);
      return oDuration;
    if gbDebugOutput: print("=== cDateTime.foGetDurationForEndDateTime(%s, %s) ===" % (str(oSelf), str(oEndDateTime)));
    oTimeDuration = cTime.foGetDurationForEndTime(oSelf, oEndDateTime);
    if gbDebugOutput: print("  1: time duration %s" % oTimeDuration);
    if cTime.fbIsAfter(oSelf, oEndDateTime):
      # The end date-time is at an earlier time in the day than the start.
      # Let's add 24 hours to the time duration and move the date a day forward:
      oTimeDuration.iHours += 24;
      oTimeDuration.fNormalize(); # This should now be positive.
      if gbDebugOutput: print("  2: time duration %s" % oTimeDuration);
      oEndDate = cDate.foGetEndDateForDuration(oEndDateTime, cDateDuration(iDays = -1));
    else:
      oEndDate = oEndDateTime.foGetDate();
    if gbDebugOutput: print("  3: end date %s" % oEndDate);
    oDateDuration = cDate.foGetDurationForEndDate(oSelf, oEndDate);
    if gbDebugOutput: print("  4: date duration %s" % oDateDuration);
    return cDateTimeDuration.foFromDateAndTimeDuration(oDateDuration, oTimeDuration);
  
  def fbIsBefore(oSelf, oDateTime):
    return (
      cDate.fbIsBefore(oSelf, oDateTime)
      or (
        cDate.fbIsEqualTo(oSelf, oDateTime) and
        cTime.fbIsBefore(oSelf, oDateTime)
      )
    );
  def fbIsEqualTo(oSelf, oDateTime):
    return (
      cDate.fbIsEqualTo(oSelf, oDateTime) and
      cTime.fbIsEqualTo(oSelf, oDateTime)
    );
  def fbIsAfter(oSelf, oDateTime):
    return (
      cDate.fbIsAfter(oSelf, oDateTime)
      or (
        cDate.fbIsEqualTo(oSelf, oDateTime) and
        cTime.fbIsAfter(oSelf, oDateTime)
      )
    );
  
  def fsToHumanReadableString(oSelf):
    # Month <day>th, <year>
    return "%s at %s" % (cDate.fsToHumanReadableString(oSelf), cTime.fsToHumanReadableString(oSelf));
  def foToPyDateTime(oSelf):
    return datetime.datetime(
      oSelf.uYear, oSelf.uMonth, oSelf.uDay,
      oSelf.uHour, oSelf.uMinute, oSelf.uSecond, oSelf.uMicrosecond
    );
  def fnToTimestamp(oSelf):
    return time.mktime(cDateTime.foToPyDateTime(oSelf).timetuple()) + (oSelf.uMicrosecond / 1000.0 / 1000);
  def fuToTimestamp(oSelf):
    return int(time.mktime(cDateTime.foToPyDateTime(oSelf).timetuple()));
  
  def fxToJSON(oSelf):
    # JSON encoding uses the "string value" of cDateTime.
    return cDateTime.fsToString(oSelf);
  def fsToMySQL(oSelf):
    # MySQL encoding uses the "string value" of cDateTime.
    return cDateTime.fsToString(oSelf);
  def fsToISO8601UTC(oSelf):
    return "%sT%sZ" % (cDate.fsToString(oSelf), cTime.fsToString(oSelf));
  def fsToString(oSelf):
    return "%s %s" % (cDate.fsToString(oSelf), cTime.fsToString(oSelf));
  
  def __str__(oSelf):
    return cDateTime.fsToString(oSelf);
  def fasGetDetails(oSelf):
    return [oSelf.fsToString()];
  def __repr__(oSelf):
    sModuleName = ".".join(oSelf.__class__.__module__.split(".")[:-1]);
    return "<%s.%s#%X|%s>" % (sModuleName, oSelf.__class__.__name__, id(oSelf), "|".join(oSelf.fasGetDetails()));
  
  def __lt__(oSelf, oOther):
    assert isinstance(oOther, oSelf.__class__), \
        "Cannot compare %s to %s" % (oSelf, oOther);
    return (
      cDate.__lt__(oSelf, oOther)
      or cTime.__lt__(oSelf, oOther)
    );
  def __le__(oSelf, oOther):
    return oSelf < oOther or oSelf == oOther;
  def __eq__(oSelf, oOther):
    assert isinstance(oOther, oSelf.__class__), \
        "Cannot compare %s to %s" % (oSelf, oOther);
    return (
      cDate.__eq__(oSelf, oOther)
      or cTime.__eq__(oSelf, oOther)
    );
  def __gt__(oSelf, oOther):
    assert isinstance(oOther, oSelf.__class__), \
        "Cannot compare %s to %s" % (oSelf, oOther);
    return (
      cDate.__gt__(oSelf, oOther)
      or cTime.__gt__(oSelf, oOther)
    );
  def __ge__(oSelf, oOther):
    return oSelf > oOther or oSelf == oOther;

from .cDateTimeDuration import cDateTimeDuration;
from .cDateDuration import cDateDuration;
from .cTimeDuration import cTimeDuration;
