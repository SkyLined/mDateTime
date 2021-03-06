import re;

from .cDateDuration import cDateDuration;
from .cTimeDuration import cTimeDuration;

class cDateTimeDuration(cDateDuration, cTimeDuration):
  # Static methods
  
  @staticmethod
  def fo0FromJSON(sDuration):
    return None if sDuration is None else cDateTimeDuration.foFromJSON(sDuration);
  @staticmethod
  def foFromJSON(sDuration):
    # JSON encoding uses the "string value" of cDateTimeDuration.
    return cDateTimeDuration.foFromString(sDuration);
  
  @staticmethod
  def fo0FromMySQL(sDuration):
    return None if sDuration is None else cDateTimeDuration.foFromMySQL(sDuration);
  @staticmethod
  def foFromMySQL(sDuration):
    # MySQL encoding uses the "string value" of cDateTimeDuration.
    return cDateTimeDuration.foFromString(sMySQL);
  
  @staticmethod
  def fbIsValidDurationString(sDuration):
    tDuration_sDate_and_sTime = sDuration.split("/");
    if len(tDuration_sDate_and_sTime) != 2:
      return False;
    (sDateDuration, sTimeDuration) = tDuration_sDate_and_sTime;
    return (
      cDateDuration.fbIsValidDurationString(sDateDuration)
      and cTimeDuration.fbIsValidDurationString(sTimeDuration)
    );
  @staticmethod
  def fo0FromString(s0Duration):
    return None if s0Duration is None else cDateTimeDuration.foFromString(s0Duration);
  @staticmethod
  def foFromString(sDuration):
    tDuration_sDate_and_sTime = sDuration.split("/");
    if len(tDuration_sDate_and_sTime) == 2:
      (sDateDuration, sTimeDuration) = tDuration_sDate_and_sTime;
      oDateDuration = cDateDuration.foFromString(sDateDuration);
      oTimeDuration = cTimeDuration.foFromString(sTimeDuration);
    else:
      # It is either a date duration or a time duration; try to parse it as
      # either:
      try:
        oDateDuration = cDateDuration.foFromString(sDuration);
        oTimeDuration = cTimeDuration(0,0,0,0);
      except:
        try:
          oTimeDuration = cTimeDuration.foFromString(sDuration);
          oDateDuration = cDateDuration(0,0,0);
        except:
          raise ValueError("Invalid duration string " + repr(sDuration));
    return cDateTimeDuration(
      oDateDuration.iYears, oDateDuration.iMonths, oDateDuration.iDays,
      oTimeDuration.iHours, oTimeDuration.iMinutes, oTimeDuration.iSeconds, oTimeDuration.iMicroseconds
    );
  
  @staticmethod
  def foFromDateAndTimeDuration(oDateDuration, oTimeDuration):
      return cDateTimeDuration(
        oDateDuration.iYears, oDateDuration.iMonths, oDateDuration.iDays,
        oTimeDuration.iHours, oTimeDuration.iMinutes, oTimeDuration.iSeconds, oTimeDuration.iMicroseconds
      );
  
  # Constructor
  def __init__(oSelf, iYears, iMonths, iDays, iHours, iMinutes, iSeconds, iMicroseconds):
    cDateDuration.__init__(oSelf, iYears, iMonths, iDays);
    cTimeDuration.__init__(oSelf, iHours, iMinutes, iSeconds, iMicroseconds);
  
  # Methods
  def foClone(oSelf):
    return cDateTimeDuration(
      oSelf.iYears, oSelf.iMonths, oSelf.iDays,
      oSelf.iHours, oSelf.iMinutes, oSelf.iSeconds, oSelf.iMicroseconds
    );
  def foGetReversed(oSelf):
    return cDateTimeDuration(
      -oSelf.iYears, -oSelf.iMonths, -oSelf.iDays,
      -oSelf.iHours, -oSelf.iMinutes, -oSelf.iSeconds, -oSelf.iMicroseconds
    );
  def fSet(oSelf,
    iYears = None, iMonths = None, iDays = None,
    iHours = None, iMinutes = None, iSeconds = None, iMicroseconds = None
  ):
    cDateDuration.fSet(oSelf, iYears, iMonths, iDays);
    cTimeDuration.fSet(oSelf, iHours, iMinutes, iSeconds, iMicroseconds);
  def foAdd(oSelf, oOtherDuration):
    cDateTimeDuration.fSet(oSelf,
      oSelf.iYears + oOtherDuration.iYears, oSelf.iMonths + oOtherDuration.iMonths, oSelf.iDays + oOtherDuration.iDays,
      oSelf.iHours + oOtherDuration.iHours, oSelf.iMinutes + oOtherDuration.iMinutes, oSelf.iSeconds + oOtherDuration.iSeconds,
      oSelf.iMicroseconds + oOtherDuration.iMicroseconds,
    );
    return oSelf;
  def foSubtract(oSelf, oOtherDuration):
    cDateTimeDuration.fSet(oSelf,
      oSelf.iYears - oOtherDuration.iYears, oSelf.iMonths - oOtherDuration.iMonths, oSelf.iDays - oOtherDuration.iDays,
      oSelf.iHours - oOtherDuration.iHours, oSelf.iMinutes - oOtherDuration.iMinutes, oSelf.iSeconds - oOtherDuration.iSeconds,
      oSelf.iMicroseconds - oOtherDuration.iMicroseconds,
    );
    return oSelf;
  def foPlus(oSelf, oOtherDuration):
    return oSelf.foClone().foAdd(oOtherDuration);
  def foMinus(oSelf, oOtherDuration):
    return oSelf.foClone().foSubtract(oOtherDuration);
  
  def __fiDateSignMultiplier(oSelf):
    iSignNumber = oSelf.iYears or oSelf.iMonths or oSelf.iDays;
    return -1 if iSignNumber < 0 else 0 if iSignNumber == 0 else 1;
  def __fiTimeSignMultiplier(oSelf):
    iSignNumber = oSelf.iHours or oSelf.iMinutes or oSelf.iSeconds or oSelf.iMicroseconds;
    return -1 if iSignNumber < 0 else 0 if iSignNumber == 0 else 1;
  def __fiSignMultiplier(oSelf):
    return oSelf.__fiDateSignMultiplier() or oSelf.__fiTimeSignMultiplier();
  def fNormalize(oSelf):
    # Normalize ranges ("13m40d/25h" -> "1y,1m,41d/1h")
    # We cannot do this for days, as the number of days in a month varies by month.
    def ftxGetValueInRangeAndOverflow(iValue, uMaxValue):
      iValueInRange = iValue % uMaxValue;
      iOverflow = (iValue - iValueInRange) / uMaxValue;
      return (iValueInRange, iOverflow);
    # Normalize time duration.
#    print "-" * 80;
#    print "0: %s" % str(oSelf);
    cTimeDuration.fNormalize(oSelf);
#    print "t: %s" % str(oSelf);
    # Overflow hours into days
    (oSelf.iHours, iOverflowedDays) = ftxGetValueInRangeAndOverflow(oSelf.iHours, 24);
    oSelf.iDays += iOverflowedDays;
#    print "o: %s" % str(oSelf);
    # Normalize date duration.
    cDateDuration.fNormalize(oSelf);
#    print "d: %s" % str(oSelf);
    # Normalize sign for time if different from date.
    iDateSignMultiplier = oSelf.__fiDateSignMultiplier();
    iTimeSignMultiplier = oSelf.__fiTimeSignMultiplier();
    if iDateSignMultiplier * iTimeSignMultiplier < 0: # Neither is 0 and only 1 is < 0
      # Flow back from days into hours.
      oSelf.iHours += 24 * iDateSignMultiplier;
      oSelf.iDays += iTimeSignMultiplier;
      # Re-normalize time duration.
      cTimeDuration.fNormalize(oSelf);
#      print "+-: %s" % str(oSelf);
  def foNormalized(oSelf):
    oNormalized = cDateTimeDuration.foClone(oSelf);
    oNormalized.fNormalize();
    return oNormalized;
  def foNormalizedForDate(oSelf, oDate):
    # First created a normalized copy, to overflow time into days:
    oNormalized = cDateTimeDuration.foNormalized(oSelf);
    # Then get the normalized date duration for that.
    oNormalizedDateDuration = cDateDuration.foNormalizedForDate(oNormalized, oDate);
    # Then create a normalized date time duration based on the date from the later and the time from the former
    return cDateTimeDuration(
      oNormalizedDateDuration.iYears, oNormalizedDateDuration.iMonths, oNormalizedDateDuration.iDays,
      oNormalized.iHours, oNormalized.iMinutes, oNormalized.iSeconds,
      oNormalized.iMicroseconds,
    );
  def fnToSecondsForDateTime(oSelf, oDateTime):
    oEndDateTime = oDateTime.foGetEndDateTimeForDuration(oSelf);
    return oEndDateTime.fnToTimestamp() - oDateTime.fnToTimestamp();
  
  def fbIsZero(oSelf, iSignMultiplier = None):
    iSignMultiplier = oSelf.__fiSignMultiplier() if iSignMultiplier is None else iSignMultiplier;
    assert cDateTimeDuration.fbIsSignNormalized(oSelf, iSignMultiplier), \
        "This method only works on sign-normalized instances";
    return iSignMultiplier == 0;
  def fbIsPositive(oSelf, iSignMultiplier = None):
    iSignMultiplier = oSelf.__fiSignMultiplier() if iSignMultiplier is None else iSignMultiplier;
    assert cDateTimeDuration.fbIsSignNormalized(oSelf, iSignMultiplier), \
        "This method only works on sign-normalized instances";
    return iSignMultiplier == 1;
  def fbIsNegative(oSelf, iSignMultiplier = None):
    iSignMultiplier = oSelf.__fiSignMultiplier() if iSignMultiplier is None else iSignMultiplier;
    assert cDateTimeDuration.fbIsSignNormalized(oSelf, iSignMultiplier), \
        "This method only works on sign-normalized instances";
    return iSignMultiplier == -1;
  
  def fbIsSignNormalized(oSelf, iSignMultiplier = None):
    iSignMultiplier = oSelf.__fiSignMultiplier() if iSignMultiplier is None else iSignMultiplier;
    return (
      oSelf.iMonths * iSignMultiplier >= 0 and
      oSelf.iDays * iSignMultiplier >= 0 and
      oSelf.iHours * iSignMultiplier >= 0 and
      oSelf.iMinutes * iSignMultiplier >= 0 and
      oSelf.iSeconds * iSignMultiplier >= 0 and
      oSelf.iMicroseconds * iSignMultiplier >= 0
    );
  def fbIsNormalized(oSelf, iSignMultiplier = None):
    iSignMultiplier = oSelf.__fiSignMultiplier() if iSignMultiplier is None else iSignMultiplier;
    return iSignMultiplier == 0 or (
      0 < oSelf.iMonths * iSignMultiplier < 12 and
      0 < oSelf.iDays * iSignMultiplier < 28 and # We can only know for sure if the number of days is small enough
      0 < oSelf.iMinutes * iSignMultiplier < 60 and
      0 < oSelf.iSeconds * iSignMultiplier < 60 and
      0 < oSelf.iMicroseconds * iSignMultiplier < 1000
    );
  
  def fsToHumanReadableString(oSelf):
    iSignMultiplier = oSelf.__fiSignMultiplier();
    if iSignMultiplier == 0: return "0 seconds";
    assert cDateTimeDuration.fbIsSignNormalized(oSelf, iSignMultiplier), \
        "Duration must be sign-normalized before converting to human readable string!";
    # Show positive and negative durations the same.
    uYears = abs(oSelf.iYears); uMonths = abs(oSelf.iMonths); uDays = abs(oSelf.iDays);
    uHours = abs(oSelf.iHours); uMinutes = abs(oSelf.iMinutes); uSeconds = abs(oSelf.iSeconds);
    uMilliAndMicroseconds = abs(oSelf.iMicroseconds);
    uMicroseconds = uMilliAndMicroseconds % 1000;
    uMilliseconds = (uMilliAndMicroseconds - uMicroseconds) / 1000;
    asComponents = [sComponent for sComponent in [
      ("%d year%s"        % (uYears,        "" if uYears == 1        else "s")) if uYears        else None,
      ("%d month%s"       % (uMonths,       "" if uMonths == 1       else "s")) if uMonths       else None,
      ("%d day%s"         % (uDays,         "" if uDays == 1         else "s")) if uDays         else None,
      ("%d hour%s"        % (uHours,        "" if uHours == 1        else "s")) if uHours        else None,
      ("%d minute%s"      % (uMinutes,      "" if uMinutes == 1      else "s")) if uMinutes      else None,
      ("%d second%s"      % (uSeconds,      "" if uSeconds == 1      else "s")) if uSeconds      else None,
      ("%d millisecond%s" % (uMilliseconds, "" if uMilliseconds == 1 else "s")) if uMilliseconds else None,
      ("%d microsecond%s" % (uMicroseconds, "" if uMicroseconds == 1 else "s")) if uMicroseconds else None,
    ] if sComponent]
    return (
      (", ".join(asComponents[:-1]) + ", and " + asComponents[-1]) if len(asComponents) >= 3 else
      " and ".join(asComponents)
    );
  
  def fxToJSON(oSelf):
    # JSON encoding uses the "string value" of cDateDuration.
    return cDateTimeDuration.fsToString(oSelf);
  def fsToMySQL(oSelf):
    # MySQL encoding uses the "string value" of cDateDuration.
    return cDateTimeDuration.fsToString(oSelf);
  def fsToString(oSelf):
    return "/".join([s for s in [
      cDateDuration.fsToString(oSelf) if oSelf.__fiDateSignMultiplier() != 0 else None,
      cTimeDuration.fsToString(oSelf) if oSelf.__fiTimeSignMultiplier() != 0 else None,
    ] if s]);
  def __str__(oSelf):
    return cDateTimeDuration.fsToString(oSelf);
  
  def __cmp__(oSelf, oOther):
    assert isinstance(oOther, cDateTimeDuration), \
        "Cannot compare %s to %s" % (oSelf, oOther);
    return cDateDuration.__cmp__(oSelf, oOther) or cTimeDuration.__cmp__(oSelf, oOther);

from .cDateTime import cDateTime;
