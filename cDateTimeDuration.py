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
  
  @staticmethod
  def foFromSeconds(nSeconds):
    (iDays, oTimeDuration) = cTimeDuration.ftxFromSeconds(nSeconds);
    return cDateTimeDuration(
      0, 0, iDays,
      oTimeDuration.iHours, oTimeDuration.iMinutes, oTimeDuration.iSeconds, oTimeDuration.iMicroseconds
    );
  
  # Constructor
  def __init__(oSelf, iYears = 0, iMonths = 0, iDays = 0, iHours = 0, iMinutes = 0, iSeconds = 0, iMicroseconds = 0):
    cDateDuration.__init__(oSelf, iYears, iMonths, iDays);
    cTimeDuration.__init__(oSelf, iHours, iMinutes, iSeconds, iMicroseconds);
  
  # Methods
  def foClone(oSelf):
    return cDateTimeDuration(
      oSelf.iYears, oSelf.iMonths, oSelf.iDays,
      oSelf.iHours, oSelf.iMinutes, oSelf.iSeconds, oSelf.iMicroseconds
    );
  def foGetDateDuration(oSelf):
    return cDateDuration.foClone(oSelf);
  def foGetTimeDuration(oSelf):
    return cTimeDuration.foClone(oSelf);
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
#    print("-" * 80);
#    print("0: %s" % str(oSelf));
    cTimeDuration.fNormalize(oSelf);
#    print("t: %s" % str(oSelf));
    # Overflow hours into days
    (oSelf.iHours, iOverflowedDays) = ftxGetValueInRangeAndOverflow(oSelf.iHours, 24);
    oSelf.iDays += iOverflowedDays;
#    print("o: %s" % str(oSelf));
    # Normalize date duration.
    cDateDuration.fNormalize(oSelf);
#    print("d: %s" % str(oSelf));
    # Normalize sign for time if different from date.
    iDateSignMultiplier = oSelf.__fiDateSignMultiplier();
    if iOverflowedDays * iDateSignMultiplier < 0: # Neither is 0 and only 1 is < 0
      # Re-normalize time duration.
      cTimeDuration.fNormalize(oSelf);
#      print("t: %s" % str(oSelf));
    iTimeSignMultiplier = oSelf.__fiTimeSignMultiplier();
    if iDateSignMultiplier * iTimeSignMultiplier < 0: # Neither is 0 and only 1 is < 0
      # Flow back from days into hours.
      oSelf.iHours += 24 * iDateSignMultiplier;
      oSelf.iDays += iTimeSignMultiplier;
      # Re-normalize time duration.
      cTimeDuration.fNormalize(oSelf);
#    print("n: %s" % str(oSelf));
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
  
  def fbIsSignNormalized(oSelf, i0SignMultiplier = None):
    iSignMultiplier = oSelf.__fiSignMultiplier() if i0SignMultiplier is None else i0SignMultiplier;
    return (
      0 <= oSelf.iMonths * iSignMultiplier and
      0 <= oSelf.iDays * iSignMultiplier and
      0 <= oSelf.iHours * iSignMultiplier and
      0 <= oSelf.iMinutes * iSignMultiplier and
      0 <= oSelf.iSeconds * iSignMultiplier and
      0 <= oSelf.iMicroseconds * iSignMultiplier
    );
  def fbIsNormalized(oSelf, i0SignMultiplier = None):
    iSignMultiplier = oSelf.__fiSignMultiplier() if i0SignMultiplier is None else i0SignMultiplier;
    return iSignMultiplier == 0 or (
      0 <= oSelf.iYears * iSignMultiplier and
      0 <= oSelf.iMonths * iSignMultiplier < 12 and
      0 <= oSelf.iDays * iSignMultiplier and
      0 <= oSelf.iMinutes * iSignMultiplier < 60 and
      0 <= oSelf.iSeconds * iSignMultiplier < 60 and
      0 <= oSelf.iMicroseconds * iSignMultiplier < 1000
    );
  
  def fNegative(oSelf):
    oSelf.iYears *= -1;
    oSelf.iMonths *= -1;
    oSelf.iDays *= -1;
    oSelf.iMinutes *= -1;
    oSelf.iSeconds *= -1;
    oSelf.iMicroseconds *= -1;
  
  def fsToHumanReadableString(oSelf, u0MaxNumberOfUnitsInOutput = None):
    assert cDateTimeDuration.fbIsSignNormalized(oSelf), \
        "Duration (%s) must be sign-normalized before converting to human readable string!" % oSelf;
    asComponents = cDateDuration.fasToHumanReadableStrings(oSelf) + cTimeDuration.fasToHumanReadableStrings(oSelf);
    if u0MaxNumberOfUnitsInOutput is not None:
      asComponents = asComponents[:u0MaxNumberOfUnitsInOutput];
    if len(asComponents) == 0:
      return "0 seconds";
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
  def fasGetDetails(oSelf):
    return [oSelf.fsToString(), "%snormalized" % ("" if oSelf.fbIsNormalized() else "sign " if oSelf.fbIsSignNormalized() else "not ")];
  def __repr__(oSelf):
    sModuleName = ".".join(oSelf.__class__.__module__.split(".")[:-1]);
    return "<%s.%s#%X|%s>" % (sModuleName, oSelf.__class__.__name__, id(oSelf), "|".join(oSelf.fasGetDetails()));
  
  def __cmp__(oSelf, oOther):
    assert isinstance(oOther, cDateTimeDuration), \
        "Cannot compare %s to %s" % (oSelf, oOther);
    return cDateDuration.__cmp__(oSelf, oOther) or cTimeDuration.__cmp__(oSelf, oOther);

from .cDateTime import cDateTime;
