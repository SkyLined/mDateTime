import datetime, re;

rTime = re.compile(
  r"^\s*" +
  r"(\d{1,2})" +
  r":" + 
  r"(\d{1,2})" +
  r"(?:" +
    r":" + 
    r"(\d{1,2})" +
    r"(?:" +
      r"\." + 
      r"(\d{1,6})" +
    r")?" +
  r")?" +
  r"(?:" +
    r"\s*(am|pm)" +
  r")?" +
  r"\s*$",
  re.I
);

def fbIsValidInteger(uValue, uMinValueInclusive = None, uMaxValueExclusive = None):
  return (
    isinstance(uValue, (int, float))
    and (uValue % 1 == 0)
    and (uValue >= uMinValueInclusive if uMinValueInclusive is not None else True)
    and (uValue < uMaxValueExclusive if uMaxValueExclusive is not None else True)
  );

class cTime(object):
  # Static methods
  @staticmethod
  def fbIsValidHour(uValue):
    return fbIsValidInteger(uValue, 0, 24);
  @staticmethod
  def fbIsValidMinute(uValue):
    return fbIsValidInteger(uValue, 0, 60);
  @staticmethod
  def fbIsValidSecond(uValue):
    return fbIsValidInteger(uValue, 0, 60);
  @staticmethod
  def fbIsValidMicrosecond(uValue):
    return fbIsValidInteger(uValue, 0, 1000 * 1000);
  @staticmethod
  def fsGetTimeString(uHour, uMinute, uSecond, uMicrosecond):
    return ("%02d:%02d:%02d.%06d" % (uHour, uMinute, uSecond, uMicrosecond)).rstrip("0").rstrip(".");

  @staticmethod
  def fo0FromPyTime(oTime):
    return None if oTime is None else cTime.foFromPyTime(oTime);
  @staticmethod
  def foFromPyTime(oTime):
    return cTime(oTime.hour, oTime.minute, oTime.second, oTime.microsecond);
  
  @staticmethod
  def fo0FromJSON(s0Time):
    return None if s0Time is None else cTime.foFromJSON(s0Time);
  @staticmethod
  def foFromJSON(sTime):
    # JSON encoding uses the "string value" of cTime.
    return cTime.foFromString(sTime);
  
  @staticmethod
  def fo0FromMySQL(s0Time):
    return None if s0Time is None else cTime.foFromMySQL(s0Time);
  @staticmethod
  def foFromMySQL(sTime):
    # MySQL encoding uses the "string value" of cTime.
    return cTime.foFromMySQL(sTime);
  
  @staticmethod
  def fbIsValidTimeString(sTime):
    return isinstance(sTime, str) and rTime.match(sTime) is not None;
  @staticmethod
  def fo0FromString(s0Time):
    return None if s0Time is None else cTime.foFromString(s0Time);
  @staticmethod
  def foFromString(sTime):
    oTimeMatch = rTime.match(sTime) if isinstance(sTime, str) else None;
    if oTimeMatch is None: raise ValueError("Invalid time string " + repr(sTime) + ".");
    uHour = int(oTimeMatch.group(1) or 0);
    if (oTimeMatch.group(5) or "").upper() == "PM":
      uHour += 12;
    uMinute = int(oTimeMatch.group(2) or 0);
    uSecond = int(oTimeMatch.group(3) or 0);
    uMicrosecond = int(oTimeMatch.group(4).ljust(6, "0")) if oTimeMatch.group(4) else 0;
    return cTime(uHour, uMinute, uSecond, uMicrosecond);
  
  @staticmethod
  def foNow():
    return cTime.foFromPyTime(datetime.datetime.now());
  @staticmethod
  def foNowUTC():
    return cTime.foFromPyTime(datetime.datetime.utcnow());
  
  # Constructor
  def __init__(oSelf, uHour, uMinute, uSecond, uMicrosecond):
    oSelf.uHour = uHour;
    oSelf.uMinute = uMinute;
    oSelf.uSecond = uSecond;
    oSelf.uMicrosecond = uMicrosecond;
  # Properties
  @property
  def uHour(oSelf):
    return oSelf.__uHour;
  @uHour.setter
  def uHour(oSelf, uHour):
    if not cTime.fbIsValidHour(uHour): raise ValueError("Invalid hour " + repr(uHour) + ".");
    oSelf.__uHour = uHour;
  @property
  def uMinute(oSelf):
    return oSelf.__uMinute;
  @uMinute.setter
  def uMinute(oSelf, uMinute):
    if not cTime.fbIsValidMinute(uMinute): raise ValueError("Invalid minute " + repr(uMinute) + ".");
    oSelf.__uMinute = uMinute;
  @property
  def uSecond(oSelf):
    return oSelf.__uSecond;
  @uSecond.setter
  def uSecond(oSelf, uSecond):
    if not cTime.fbIsValidSecond(uSecond): raise ValueError("Invalid second " + repr(uSecond) + ".");
    oSelf.__uSecond = uSecond;
  @property
  def uMicrosecond(oSelf):
    return oSelf.__uMicrosecond;
  @uMicrosecond.setter
  def uMicrosecond(oSelf, uMicrosecond):
    if not cTime.fbIsValidMicrosecond(uMicrosecond): raise ValueError("Invalid microsecond " + repr(uMicrosecond) + ".");
    oSelf.__uMicrosecond = uMicrosecond;
  # Methods
  def foClone(oSelf):
    return cTime(oSelf.uHour, oSelf.uMinute, oSelf.uSecond, oSelf.uMicrosecond);
  
  def fSet(oSelf, uHour, uMinute, uSecond, uMicrosecond):
    if uHour is not None: oSelf.uHour = uHour;
    if uMinute is not None: oSelf.uMinute = uMinute;
    if uSecond is not None: oSelf.uSecond = uSecond;
    if uMicrosecond is not None: oSelf.uMicrosecond = uMicrosecond;
  
  def ftoGetEndTimeAndOverflowedDaysForDuration(oSelf, oDuration):
    # Note that this code ignores the time (if any) in oDuration
    # Add the year and month:
    iTotalMicroseconds = oSelf.uMicrosecond + oDuration.iMicroseconds;
    iTotalSeconds = oSelf.uSecond + oDuration.iSeconds;
    iTotalMinutes = oSelf.uMinute + oDuration.iMinutes;
    iTotalHours = oSelf.uHour + oDuration.iHours;
    def ftxGetPositiveValueInRangeAndOverflow(iValue, uMaxValue):
      uValue = iValue % uMaxValue;
      iOverflow = (iValue - uValue) / uMaxValue;
      return (uValue, iOverflow);
    uMicrosecond, iOverflowedSeconds = ftxGetPositiveValueInRangeAndOverflow(iTotalMicroseconds, 1000 * 1000);
    uSecond, iOverflowedMinutes = ftxGetPositiveValueInRangeAndOverflow(iTotalSeconds + iOverflowedSeconds, 60);
    uMinute, iOverflowedHours = ftxGetPositiveValueInRangeAndOverflow(iTotalMinutes + iOverflowedMinutes, 60);
    uHour, iOverflowedDays = ftxGetPositiveValueInRangeAndOverflow(iTotalHours + iOverflowedHours, 24);
    oEndTime = cTime(uHour, uMinute, uSecond, uMicrosecond);
    return (oEndTime, iOverflowedDays);
  
  def foGetDurationForEndTime(oSelf, oEndTime):
    iMicroseconds = oEndTime.uMicrosecond - oSelf.uMicrosecond;
    iSeconds = oEndTime.uSecond - oSelf.uSecond;
    iMinutes = oEndTime.uMinute - oSelf.uMinute;
    iHours = oEndTime.uHour - oSelf.uHour;
    oDuration = cTimeDuration(iHours, iMinutes, iSeconds, iMicroseconds);
    oDuration.fNormalize();
    return oDuration;
  
  def fbIsBefore(oSelf, oTime):
    if oSelf.uHour < oTime.uHour: return True;
    if oSelf.uHour > oTime.uHour: return False;
    if oSelf.uMinute < oTime.uMinute: return True;
    if oSelf.uMinute > oTime.uMinute: return False;
    if oSelf.uSecond < oTime.uSecond: return True;
    if oSelf.uSecond > oTime.uSecond: return False;
    if oSelf.uMicrosecond < oTime.uMicrosecond: return True;
    #if oSelf.uMicrosecond > oTime.uMicrosecond: return False;
    return False;
  def fbIsEqualTo(oSelf, oTime):
    return (
      oSelf.uHour == oTime.uHour and
      oSelf.uMinute == oTime.uMinute and
      oSelf.uSecond == oTime.uSecond and
      oSelf.uMicrosecond == oTime.uMicrosecond
    );
  def fbIsAfter(oSelf, oTime):
    if oSelf.uHour > oTime.uHour: return True;
    if oSelf.uHour < oTime.uHour: return False;
    if oSelf.uMinute > oTime.uMinute: return True;
    if oSelf.uMinute < oTime.uMinute: return False;
    if oSelf.uSecond > oTime.uSecond: return True;
    if oSelf.uSecond < oTime.uSecond: return False;
    if oSelf.uMicrosecond > oTime.uMicrosecond: return True;
    #if oSelf.uMicrosecond < oTime.uMicrosecond: return False;
    return False;
  
  def fbIsInThePast(oSelf):
    return cTime.fbIsBefore(oSelf, cTime.foNow());
  def fbIsInThePastUTC(oSelf):
    return cTime.fbIsBefore(oSelf, cTime.foNowUTC());
  def fbIsToday(oSelf):
    return cTime.fbIsEqualTo(oSelf, cTime.foNow());
  def fbIsTodayUTC(oSelf):
    return cTime.fbIsEqualTo(oSelf, cTime.foNowUTC());
  def fbIsInTheFuture(oSelf):
    return cTime.fbIsAfter(oSelf, cTime.foNow());
  def fbIsInTheFutureUTC(oSelf):
    return cTime.fbIsAfter(oSelf, cTime.foNowUTC());

  def fsToHumanReadableString(oSelf):
    # <hour>:<minute>[:<second>[.<microsecond>]]
    sValue = ("%d:%02d:%02d.%06d" % (
      oSelf.uHour,
      oSelf.uMinute,
      oSelf.uSecond,
      oSelf.uMicrosecond,
    )).rstrip("0").rstrip(".");
    if sValue.endswith(":00"):
      return sValue[:-3];
    return sValue;
  def foToPyTime(oSelf):
    return datetime.date(oSelf.uHour, oSelf.uMinute, oSelf.uSecond, oSelf.uMicrosecond);
  def fxToJSON(oSelf):
    # JSON encoding uses the "string value" of cTime.
    return str(oSelf);
  def fsToMySQL(oSelf):
    # MySQL encoding uses the "string value" of cTime.
    return str(oSelf);
  def fsToString(oSelf):
    return cTime.fsGetTimeString(oSelf.uHour, oSelf.uMinute, oSelf.uSecond, oSelf.uMicrosecond);
  def __str__(oSelf):
    return cTime.fsToString(oSelf);
  
  def __cmp__(oSelf, oOther):
    assert isinstance(oOther, cTime), \
        "Cannot compare %s to %s" % (oSelf, oOther);
    if oSelf.uHour != oSelf.uHour: return oSelf.uHour - oOther.uHour;
    if oSelf.uMinute != oSelf.uMinute: return oSelf.uMinute - oOther.uMinute;
    if oSelf.uSecond != oSelf.uSecond: return oSelf.uSecond - oOther.uSecond;
    if oSelf.uMicrosecond != oSelf.uMicrosecond: return oSelf.uMicrosecond - oOther.uMicrosecond;
    return 0;

from .cTimeDuration import cTimeDuration;