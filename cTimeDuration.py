import math, re;

gbDebugOutput = False;

rTimeDuration = re.compile(
  r"^\s*" +
  r"(?:([+-]?\d+)\s*h(?:ours?)?\s*,?\s*)?" +
  r"(?:([+-]?\d+)\s*m(?:inutes?)?\s*,?\s*)?" +
  r"(?:([+-]?\d+)\s*s(?:econds?)?\s*,?\s*)?" +
  r"(?:([+-]?\d+)\s*u(?:seconds?)?)?" +
  r"\s*$"
);
def fbIsValidInteger(uValue):
  return isinstance(uValue, (int, float)) and uValue % 1 == 0;

class cTimeDuration(object):
  # static methods
  @staticmethod
  def fo0FromJSON(sDuration):
    return None if sDuration is None else cTimeDuration.foFromJSON(sDuration);
  @staticmethod
  def foFromJSON(sDuration):
    # JSON encoding uses the "string value" of cTimeDuration.
    return cTimeDuration.foFromString(sDuration);
  
  @staticmethod
  def fo0FromMySQL(sDuration):
    return None if sDuration is None else cTimeDuration.foFromMySQL(sDuration);
  @staticmethod
  def foFromMySQL(sDuration):
    # MySQL encoding uses the "string value" of cTimeDuration.
    return cTimeDuration.foFromString(sMySQL);
  
  @staticmethod
  def ftxFromSeconds(nSeconds):
    iSign = -1 if nSeconds < 0 else 1;
    nTotalSeconds = abs(nSeconds);
    uTotalSeconds = int(nTotalSeconds);
    uMicroseconds = int(1000 * 1000 * (nTotalSeconds - uTotalSeconds));
    # These asserts are here to check the code is doing what it is supposed to do because I ran into an issue
    # in other code that I think may have been caused by a bug here.
    assert uMicroseconds >= 0, \
        "uMicroseconds = %s" % uMicroseconds;
    uSeconds = uTotalSeconds % 60;
    assert uSeconds >= 0, \
        "uSeconds = %s" % uSeconds;
    
    uTotalMinutes = (uTotalSeconds - uSeconds) / 60;
    uMinutes = uTotalMinutes % 60;
    assert uMinutes >= 0, \
        "uMinutes = %s" % uMinutes;
    
    uTotalHours = (uTotalMinutes - uMinutes) / 60;
    uHours = uTotalHours % 24;
    assert uHours >= 0, \
        "uHours = %s" % uHours;
    
    uDays = (uTotalHours - uHours) / 24;
    assert uDays >= 0, \
        "uDays = %s" % uDays;
    
    oTimeDuration = cTimeDuration(
      iSign * uHours,
      iSign * uMinutes,
      iSign * uSeconds,
      iSign * uMicroseconds,
    );
    return (iSign * uDays, oTimeDuration);
  
  @staticmethod
  def fbIsValidDurationString(sDuration):
    oDurationMatch = rTimeDuration.match(sDuration) if isinstance(sDuration, str) else None;
    return oDurationMatch is not None and any([sComponent is not None for sComponent in oDurationMatch.groups()]);
  @staticmethod
  def fo0FromString(sDuration):
    return None if sDuration is None else cTimeDuration.foFromString(sDuration);
  @staticmethod
  def foFromString(sDuration):
    oDurationMatch = rTimeDuration.match(sDuration) if isinstance(sDuration, str) else None;
    if oDurationMatch is None or all([sComponent is None for sComponent in oDurationMatch.groups()]):
      raise ValueError("Invalid duration string " + repr(sDuration));
    sHours, sMinutes, sSeconds, sMicroseconds = oDurationMatch.groups();
    iHours = int(sHours) if sHours else 0;
    iMinutes = int(sMinutes) if sMinutes else 0;
    iSeconds = int(sSeconds) if sSeconds else 0;
    iMicroseconds = int(sMicroseconds) if sMicroseconds else 0;
    return cTimeDuration(iHours, iMinutes, iSeconds, iMicroseconds);
  # Constructor
  def __init__(oSelf, iHours = 0, iMinutes = 0, iSeconds = 0, iMicroseconds = 0):
    if not fbIsValidInteger(iHours): raise ValueError("Invalid number of hours " + repr(iHours) + ".");
    if not fbIsValidInteger(iMinutes): raise ValueError("Invalid number of minutes " + repr(iMinutes) + ".");
    if not fbIsValidInteger(iSeconds): raise ValueError("Invalid number of seconds " + repr(iSeconds) + ".");
    if not fbIsValidInteger(iMicroseconds): raise ValueError("Invalid number of microseconds " + repr(iMicroseconds) + ".");
    oSelf.__iHours = iHours;
    oSelf.__iMinutes = iMinutes;
    oSelf.__iSeconds = iSeconds;
    oSelf.__iMicroseconds = iMicroseconds;
  # Properties
  @property
  def iHours(oSelf):
    return oSelf.__iHours;
  @iHours.setter
  def iHours(oSelf, iHours):
    if not fbIsValidInteger(iHours): raise ValueError("Invalid number of hours " + repr(iHours) + ".");
    oSelf.__iHours = iHours;
  @property
  def iMinutes(oSelf):
    return oSelf.__iMinutes;
  @iMinutes.setter
  def iMinutes(oSelf, iMinutes):
    if not fbIsValidInteger(iMinutes): raise ValueError("Invalid number of minutes " + repr(iMinutes) + ".");
    oSelf.__iMinutes = iMinutes;
  @property
  def iSeconds(oSelf):
    return oSelf.__iSeconds;
  @iSeconds.setter
  def iSeconds(oSelf, iSeconds):
    if not fbIsValidInteger(iSeconds): raise ValueError("Invalid number of seconds " + repr(iSeconds) + ".");
    oSelf.__iSeconds = iSeconds;
  @property
  def iMicroseconds(oSelf):
    return oSelf.__iMicroseconds;
  @iMicroseconds.setter
  def iMicroseconds(oSelf, iMicroseconds):
    if not fbIsValidInteger(iMicroseconds): raise ValueError("Invalid number of microseconds " + repr(iMicroseconds) + ".");
    oSelf.__iMicroseconds = iMicroseconds;
  # methods
  def foClone(oSelf):
    return cTimeDuration(oSelf.iHours, oSelf.iMinutes, oSelf.iSeconds, oSelf.iMicroseconds);
  def foGetReversed(oSelf):
    return cTimeDuration(-oSelf.iHours, -oSelf.iMinutes, -oSelf.iSeconds, -oSelf.iMicroseconds);
  def fSet(oSelf, iHours = None, iMinutes = None, iSeconds = None, iMicroseconds = None):
    if iHours is not None:
      oSelf.iHours = iHours;
    if iMinutes is not None:
      oSelf.iMinutes = iMinutes;
    if iSeconds is not None:
      oSelf.iSeconds = iSeconds;
    if iMicroseconds is not None:
      oSelf.iMicroseconds = iMicroseconds;
  def foAdd(oSelf, oOtherDuration):
    cTimeDuration.fSet(oSelf,
      oSelf.iHours + oOtherDuration.iHours, oSelf.iMinutes + oOtherDuration.iMinutes, oSelf.iSeconds + oOtherDuration.iSeconds,
      oSelf.iMicroseconds + oOtherDuration.iMicroseconds,
    );
    return oSelf;
  def foSubtract(oSelf, oOtherDuration):
    oSelf.fSet(
      oSelf.iHours - oOtherDuration.iHours, oSelf.iMinutes - oOtherDuration.iMinutes, oSelf.iSeconds - oOtherDuration.iSeconds,
      oSelf.iMicroseconds - oOtherDuration.iMicroseconds,
    );
    return oSelf;
  def foPlus(oSelf, oOtherDuration):
    return oSelf.foClone().foAdd(oOtherDuration);
  def foMinus(oSelf, oOtherDuration):
    return oSelf.foClone().foSubtract(oOtherDuration);
  
  def __fiSignMultiplier(oSelf):
    iSignNumber = oSelf.iHours or oSelf.iMinutes or oSelf.iSeconds or oSelf.iMicroseconds;
    return -1 if iSignNumber < 0 else 0 if iSignNumber == 0 else 1;
  def fNormalize(oSelf):
    if gbDebugOutput: print("=== cTimeDuration.fNormalize(%s) ===" % str(oSelf));
    # Normalize ranges and make everything except hours positive ("-61s" -> "-1h+58m+59s")
    def ftiGetPositiveValueInRangeAndOverflow(iValue, uMaxValue, iOverflowBaseValue):
      iOverflow = math.floor(iValue / uMaxValue);
      uValueInRange = iValue % uMaxValue;
      return (uValueInRange, iOverflow + iOverflowBaseValue);
    oSelf.iMicroseconds, oSelf.iSeconds = ftiGetPositiveValueInRangeAndOverflow(oSelf.iMicroseconds, 1000 * 1000, oSelf.iSeconds);
    if gbDebugOutput: print("  1: s<-u %s" % oSelf);
    oSelf.iSeconds, oSelf.iMinutes = ftiGetPositiveValueInRangeAndOverflow(oSelf.iSeconds, 60, oSelf.iMinutes);
    if gbDebugOutput: print("  2: m<-s %s" % oSelf);
    oSelf.iMinutes, oSelf.iHours = ftiGetPositiveValueInRangeAndOverflow(oSelf.iMinutes, 60, oSelf.iHours);
    if gbDebugOutput: print("  3: h<-m %s" % oSelf);
    if oSelf.iHours < 0:
      # negative hours: make everything negative or zero.
      if oSelf.iMinutes or oSelf.iSeconds or oSelf.iMicroseconds:
        # borrow an hour to make the rest negative.
        oSelf.iHours +=1; # will remain negative or become zero
        oSelf.iMinutes -= 60; # will become negative
        if gbDebugOutput: print("  4: h->m %s" % oSelf);
      if oSelf.iSeconds or oSelf.iMicroseconds:
        oSelf.iMinutes +=1; # will remain negative or become zero
        oSelf.iSeconds -= 60; # will become negative
        if gbDebugOutput: print("  5: m->s %s" % oSelf);
      if oSelf.iMicroseconds:
        oSelf.iSeconds +=1; # will remain negative or become zero
        oSelf.iMicroseconds -= 1000 * 1000; # will become negative
        if gbDebugOutput: print("  6: s->u %s" % oSelf);
    if gbDebugOutput: print("=> result: %s" % str(oSelf));
  def foNormalized(oSelf):
    oNormalized = cTimeDuration.foClone(oSelf);
    cTimeDuration.fNormalize(oNormalized);
    return oNormalized;
  def fnToSeconds(oSelf):
    return ((oSelf.iHours * 60) + oSelf.iMinutes * 60) + oSelf.iSeconds + (oSelf.iMicroseconds / 1000.0 / 1000);
  
  def fbIsZero(oSelf, iSignMultiplier = None):
    iSignMultiplier = oSelf.__fiSignMultiplier() if iSignMultiplier is None else iSignMultiplier;
    assert cTimeDuration.fbIsSignNormalized(oSelf, iSignMultiplier), \
        "This method only works on sign-normalized instances";
    return iSignMultiplier == 0;
  def fbIsPositive(oSelf, iSignMultiplier = None):
    iSignMultiplier = oSelf.__fiSignMultiplier() if iSignMultiplier is None else iSignMultiplier;
    assert cTimeDuration.fbIsSignNormalized(oSelf, iSignMultiplier), \
        "This method only works on sign-normalized instances";
    return iSignMultiplier == 1;
  def fbIsNegative(oSelf, iSignMultiplier = None):
    iSignMultiplier = oSelf.__fiSignMultiplier() if iSignMultiplier is None else iSignMultiplier;
    assert cTimeDuration.fbIsSignNormalized(oSelf, iSignMultiplier), \
        "This method only works on sign-normalized instances";
    return iSignMultiplier == -1;
  
  def fbIsSignNormalized(oSelf, iSignMultiplier = None):
    iSignMultiplier = oSelf.__fiSignMultiplier() if iSignMultiplier is None else iSignMultiplier;
    return iSignMultiplier == 0 or (
      oSelf.iMinutes * iSignMultiplier >= 0 and
      oSelf.iSeconds * iSignMultiplier >= 0 and
      oSelf.iMicroseconds * iSignMultiplier >= 0
    );
  def fbIsNormalized(oSelf, iSignMultiplier = None):
    iSignMultiplier = oSelf.__fiSignMultiplier() if iSignMultiplier is None else iSignMultiplier;
    return iSignMultiplier == 0 or (
      0 < oSelf.iMinutes * iSignMultiplier < 60 and
      0 < oSelf.iSeconds * iSignMultiplier < 60 and
      0 < oSelf.iMicroseconds * iSignMultiplier < 1000 * 1000
    );
  
  def fasToHumanReadableStrings(oSelf):
    assert cTimeDuration.fbIsSignNormalized(oSelf), \
        "Duration must be sign-normalized before converting to human readable string!";
    # Show positive and negative durations the same.
    uHours = abs(oSelf.iHours); uMinutes = abs(oSelf.iMinutes); uSeconds = abs(oSelf.iSeconds);
    uMilliAndMicroseconds = abs(oSelf.iMicroseconds);
    uMicroseconds = uMilliAndMicroseconds % 1000;
    uMilliseconds = (uMilliAndMicroseconds - uMicroseconds) / 1000;
    return [sComponent for sComponent in [
      ("%d hour%s"        % (uHours,        "" if uHours == 1        else "s")) if uHours        else None,
      ("%d minute%s"      % (uMinutes,      "" if uMinutes == 1      else "s")) if uMinutes      else None,
      ("%d second%s"      % (uSeconds,      "" if uSeconds == 1      else "s")) if uSeconds      else None,
      ("%d millisecond%s" % (uMilliseconds, "" if uMilliseconds == 1 else "s")) if uMilliseconds else None,
      ("%d microsecond%s" % (uMicroseconds, "" if uMicroseconds == 1 else "s")) if uMicroseconds else None,
    ] if sComponent];
  def fsToHumanReadableString(oSelf, u0MaxNumberOfUnitsInOutput = None):
    asComponents = oSelf.fasToHumanReadableStrings();
    if u0MaxNumberOfUnitsInOutput is not None:
      asComponents = asComponents[:u0MaxNumberOfUnitsInOutput];
    if len(asComponents) == 0:
      return "0 seconds";
    return (
      (", ".join(asComponents[:-1]) + ", and " + asComponents[-1]) if len(asComponents) >= 3 else
      " and ".join(asComponents)
    );
  
  def fxToJSON(oSelf):
    # JSON encoding uses the "string value" of cTimeDuration.
    return cTimeDuration.fsToString(oSelf);
  def fsToMySQL(oSelf):
    # MySQL encoding uses the "string value" of cTimeDuration.
    return cTimeDuration.fsToString(oSelf);
  def fsToString(oSelf):
    return "".join([
      "%+d%s" % (iValue, sUnit)
      for (iValue, sUnit) in (
        (oSelf.iHours, "h"),
        (oSelf.iMinutes, "m"),
        (oSelf.iSeconds, "s"),
        (oSelf.iMicroseconds, "u"),
      )
      if iValue != 0
    ]) or "0s";
  def __str__(oSelf):
    return cTimeDuration.fsToString(oSelf);
  
  def __cmp__(oSelf, oOther):
    assert isinstance(oOther, cTimeDuration), \
        "Cannot compare %s to %s" % (oSelf, oOther);
    if oSelf.iHours != oSelf.iHours: return oSelf.iHours - oOther.iHours;
    if oSelf.iMinutes != oSelf.iMinutes: return oSelf.iMinutes - oOther.iMinutes;
    if oSelf.iSeconds != oSelf.iSeconds: return oSelf.iSeconds - oOther.iSeconds;
    if oSelf.iMicroseconds != oSelf.iMicroseconds: return oSelf.iMicroseconds - oOther.iMicroseconds;
    return 0;
