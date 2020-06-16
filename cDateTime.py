import calendar, datetime, re, time;

from .cDate import cDate;
from .cTime import cTime;

class cDateTime(cTime, cDate):
  # Static methods
  @staticmethod
  def fo0FromPyDateTime(oDateTime):
    return None if oDateTime is None else cDateTime.foFromPyDateTime(oDateTime);
  @staticmethod
  def foFromPyDateTime(oDateTime):
    return cDateTime(
      oDateTime.year, oDateTime.month, oDateTime.day,
      oDateTime.hour, oDateTime.minute, oDateTime.second, oDateTime.microsecond
    );
  
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
      oSelf.uHour, oSelf.uMinute, oSelf.uSecond, oTime.uMicrosecond
    );
  
  def fSet(oSelf, uYear = None, uMonth = None, uDay = None, uHour = None, uMinute = None, uSecond = None, uMicrosecond = None):
    cDate.fSet(oSelf, uYear, uMonth, uDay);
    cTime.fSet(oSelf, uHour, uMinute, uSecond, uMicrosecond);
  
  def foGetDate(oSelf):
    return cDate(oSelf.uYear, oSelf.uMonth, oSelf.uDay);
  
  def foGetTime(oSelf):
    return cTime(oSelf.uHour, oSelf.uMinute, oSelf.uSecond, oSelf.uMicrosecond);
  
  def foGetEndDateTimeForDuration(oSelf, oDuration):
    from cDateDuration import cDateDuration;
    from cTimeDuration import cTimeDuration;
    from cDateTimeDuration import cDateTimeDuration;
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
      oEndTime, iOverflowedDays = cTime.ftoGetEndTimeAndOverflowedDaysForDuration(oSelf, oTimeDuration);
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
    oDateDuration = cDate.foGetDurationForEndDate(oSelf, oEndDateTime);
    oTimeDuration = cTime.foGetDurationForEndTime(oSelf, oEndDateTime);
    return cDateTimeDuration.foFromDateAndTimeDuration(oDateDuration, oTimeDuration);
  
  def fbIsBefore(oSelf, oDateTime):
    return (
      cDate.fbIsBefore(oSelf, oDateTime)
      or (
        cDate.fbIsEqualTo(oSelf, oDateTime) and
        cTime.fbIsBefore(oSelf, oDateTime)
      )
    );
  def fbIsEqualTo(oSelf, oDate):
    return (
      cDate.fbIsEqualTo(oSelf, oDateTime) and
      cTime.fbIsEqualTo(oSelf, oDateTime)
    );
  def fbIsAfter(oSelf, oDate):
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
    return long(time.mktime(cDateTime.foToPyDateTime(oSelf).timetuple()));
  
  def fxToJSON(oSelf):
    # JSON encoding uses the "string value" of cDateTime.
    return cDateTime.fsToString(oSelf);
  def fsToMySQL(oSelf):
    # MySQL encoding uses the "string value" of cDateTime.
    return cDateTime.fsToString(oSelf);
  def fsToString(oSelf):
    return "%s %s" % (cDate.fsToString(oSelf), cTime.fsToString(oSelf));
  
  def __str__(oSelf):
    return cDateTime.fsToString(oSelf);
  
  def __cmp__(oSelf, oOther):
    assert isinstance(oOther, cDateTime), \
        "Cannot compare %s to %s" % (oSelf, oOther);
    return cDate.__cmp__(oSelf, oOther) or cTime.__cmp__(oSelf, oOther);

from .cDateTimeDuration import cDateTimeDuration;
from .cDateDuration import cDateDuration;
from .cTimeDuration import cTimeDuration;



