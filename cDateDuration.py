import re;

rDateDuration = re.compile(
  "^\\s*" +
  "(?:([+-]?\\d+)\\s*y(?:ears?)?\\s*,?\\s*)?" +
  "(?:([+-]?\\d+)\\s*m(?:onths?)?\\s*,?\\s*)?" +
  "(?:([+-]?\\d+)\\s*d(?:ays?)?)?" +
  "\\s*$"
);
def fbIsValidInteger(uValue):
  return type(uValue) in [long, int, float] and uValue % 1 == 0;

class cDateDuration(object):
  # static methods
  @staticmethod
  def fo0FromJSON(sDuration):
    return None if sDuration is None else cDateDuration.foFromJSON(sDuration);
  @staticmethod
  def foFromJSON(sDuration):
    # JSON encoding uses the "string value" of cDateDuration.
    return cDateDuration.foFromString(sDuration);
  
  @staticmethod
  def fo0FromMySQL(sDuration):
    return None if sDuration is None else cDateDuration.foFromMySQL(sDuration);
  @staticmethod
  def foFromMySQL(sDuration):
    # MySQL encoding uses the "string value" of cDateDuration.
    return cDateDuration.foFromString(sMySQL);
  
  @staticmethod
  def fbIsValidDurationString(sDuration):
    oDurationMatch = rDateDuration.match(sDuration) if type(sDuration) in [str, unicode] else None;
    return oDurationMatch is not None and any([sComponent is not None for sComponent in oDurationMatch.groups()]);
  @staticmethod
  def fo0FromString(sDuration):
    return None if sDuration is None else cDateDuration.foFromString(sDuration);
  @staticmethod
  def foFromString(sDuration):
    oDurationMatch = rDateDuration.match(sDuration) if type(sDuration) in [str, unicode] else None;
    asDurationMatchGroups = oDurationMatch.groups() if oDurationMatch is not None else None
    if oDurationMatch is None or all([sComponent is None for sComponent in asDurationMatchGroups]):
      raise ValueError("Invalid duration string " + repr(sDuration));
    sYears, sMonths, sDays = oDurationMatch.groups();
    # Values may not contain a sign, in which case the sign is assumed to be +
    # "-1y2m+3d" => "-1y+2m+3d"
    iYears = long(sYears) if sYears else 0;
    iMonths = long(sMonths) if sMonths else 0;
    iDays = long(sDays) if sDays else 0;
    return cDateDuration(iYears, iMonths, iDays);
  # Constructor
  def __init__(oSelf, iYears, iMonths, iDays):
    if not fbIsValidInteger(iYears): raise ValueError("Invalid number of years " + repr(iYears) + ".");
    if not fbIsValidInteger(iMonths): raise ValueError("Invalid number of months " + repr(iMonths) + ".");
    if not fbIsValidInteger(iDays): raise ValueError("Invalid number of days " + repr(iDays) + ".");
    oSelf.__iYears = iYears;
    oSelf.__iMonths = iMonths;
    oSelf.__iDays = iDays;
  # Properties
  @property
  def iYears(oSelf):
    return oSelf.__iYears;
  @iYears.setter
  def iYears(oSelf, iYears):
    if not fbIsValidInteger(iYears): raise ValueError("Invalid number of years " + repr(iYears) + ".");
    oSelf.__iYears = iYears;
  @property
  def iMonths(oSelf):
    return oSelf.__iMonths;
  @iMonths.setter
  def iMonths(oSelf, iMonths):
    if not fbIsValidInteger(iMonths): raise ValueError("Invalid number of months " + repr(iMonths) + ".");
    oSelf.__iMonths = iMonths;
  @property
  def iDays(oSelf):
    return oSelf.__iDays;
  @iDays.setter
  def iDays(oSelf, iDays):
    if not fbIsValidInteger(iDays): raise ValueError("Invalid number of days " + repr(iDays) + ".");
    oSelf.__iDays = iDays;
  # methods
  def foClone(oSelf):
    return cDateDuration(oSelf.iYears, oSelf.iMonths, oSelf.iDays);
  def foGetReversed(oSelf):
    return cDateDuration(-oSelf.iYears, -oSelf.iMonths, -oSelf.iDays);
  def fSet(oSelf, iYears = None, iMonths = None, iDays = None):
    if iYears is not None:
      oSelf.iYears = iYears;
    if iMonths is not None:
      oSelf.iMonths = iMonths;
    if iDays is not None:
      oSelf.iDays = iDays;
  def foAdd(oSelf, oOtherDuration):
    cDateDuration.fSet(oSelf,
      oSelf.iYears + oOtherDuration.iYears,
      oSelf.iMonths + oOtherDuration.iMonths,
      oSelf.iDays + oOtherDuration.iDays
    );
    return oSelf;
  def foSubtract(oSelf, oOtherDuration):
    cDateDuration.fSet(oSelf,
      oSelf.iYears - oOtherDuration.iYears,
      oSelf.iMonths - oOtherDuration.iMonths,
      oSelf.iDays - oOtherDuration.iDays
    );
    return oSelf;
  def foPlus(oSelf, oOtherDuration):
    return cDateDuration.fAdd(oSelf.foClone, oOtherDuration);
  def foMinus(oSelf, oOtherDuration):
    return cDateDuration.foSubtract(oSelf.foClone(), oOtherDuration);
  
  def __fiSignMultiplier(oSelf):
    iSignNumber = oSelf.iYears or oSelf.iMonths or oSelf.iDays;
    return -1 if iSignNumber < 0 else 0 if iSignNumber == 0 else 1;
  def fNormalize(oSelf):
    # Normalize ranges ("13m" -> "1y,1m")
    # We cannot do this for days, as the number of days in a month varies by month.
    def ftxGetValueInRangeAndOverflow(iValue, uMaxValue):
      iValueInRange = iValue % uMaxValue;
      iOverflow = (iValue - iValueInRange) / uMaxValue;
      return (iValueInRange, iOverflow);
    oSelf.iMonths, iOverflowedYears = ftxGetValueInRangeAndOverflow(oSelf.iMonths, 12);
    oSelf.iYears = oSelf.iYears + iOverflowedYears;
#    print "m->y: %s" % oSelf;
    # Normalize signs ("1y,-1m" -> "11m")
    # We cannot do this for days, as the number of days in a month varies by month.
    iSignMultiplier = oSelf.__fiSignMultiplier();
    def ftxGetCorrectlySignedValueInRangeAndOverflow(iValue, uMaxValue):
      if iValue * iSignMultiplier >= 0:
        return (iValue, 0); # Already correctly signed, no overflow
      return (
        iValue + uMaxValue * iSignMultiplier, # Fix sign
        iSignMultiplier # overflow
      );
    (oSelf.iMonths, iOverflowYears) = ftxGetCorrectlySignedValueInRangeAndOverflow(oSelf.iMonths, 12);
    oSelf.iYears += iOverflowYears;
#    print "+-m->y: %s" % oSelf;
  def foNormalized(oSelf):
    oNormalized = oSelf.foClone();
    cDateDuration.fNormalize(oNormalized);
    return oNormalized;
  def foNormalizedForDate(oSelf, oDate):
    # Adjust duration to make all numbers either all positive or negative and minimize days, months and years.
    # e.g. "+2y-12m+32d" for "2000-01-01" => "+1y+1m+1d"
    return cDate.foGetDurationForEndDate(oDate, cDate.foGetEndDateForDuration(oDate, oSelf));
  def fnToSecondsForDate(oSelf, oDate):
    oEndDate = oDate.foGetEndDateForDuration(oSelf);
    return oEndDate.fnToTimestamp() - oDate.fnToTimestamp();
  
  def fbIsZero(oSelf, iSignMultiplier = None):
    iSignMultiplier = oSelf.__fiSignMultiplier() if iSignMultiplier is None else iSignMultiplier;
    assert cDateDuration.fbIsSignNormalized(oSelf, iSignMultiplier), \
        "This method only works on sign-normalized instances";
    return iSignMultiplier == 0;
  def fbIsPositive(oSelf, iSignMultiplier = None):
    iSignMultiplier = oSelf.__fiSignMultiplier() if iSignMultiplier is None else iSignMultiplier;
    assert cDateDuration.fbIsSignNormalized(oSelf, iSignMultiplier), \
        "This method only works on sign-normalized instances";
    return iSignMultiplier == 1;
  def fbIsNegative(oSelf, iSignMultiplier = None):
    iSignMultiplier = oSelf.__fiSignMultiplier() if iSignMultiplier is None else iSignMultiplier;
    assert cDateDuration.fbIsSignNormalized(oSelf, iSignMultiplier), \
        "This method only works on sign-normalized instances";
    return iSignMultiplier == -1;
  
  def fbIsSignNormalized(oSelf, iSignMultiplier = None):
    iSignMultiplier = oSelf.__fiSignMultiplier();
    return (
      oSelf.iMonths * iSignMultiplier >= 0 and
      oSelf.iDays * iSignMultiplier >= 0
    );
  def fbIsNormalized(oSelf, iSignMultiplier = None):
    iSignMultiplier = oSelf.__fiSignMultiplier() if iSignMultiplier is None else iSignMultiplier;
    return iSignMultiplier == 0 or (
      0 < oSelf.iMonths * iSignMultiplier < 12 and
      0 < oSelf.iDays * iSignMultiplier < 28 # We can only know for sure if the number of days is small enough
    );
  
  def fsToHumanReadableString(oSelf):
    iSignMultiplier = oSelf.__fiSignMultiplier();
    if iSignMultiplier == 0: return "0 days";
    assert cDateDuration.fbIsSignNormalized(oSelf, iSignMultiplier), \
        "Duration must be sign-normalized before converting to human readable string!";
    # Show positive and negative durations the same.
    uYears = abs(oSelf.iYears); uMonths = abs(oSelf.iMonths); uDays = abs(oSelf.iDays);
    asComponents = [sComponent for sComponent in [
      ("%d year%s"  % (uYears,  "" if uYears == 1  else "s")) if uYears  else None,
      ("%d month%s" % (uMonths, "" if uMonths == 1 else "s")) if uMonths else None,
      ("%d day%s"   % (uDays,   "" if uDays == 1   else "s")) if uDays   else None,
    ] if sComponent]
    return (
      (", ".join(asComponents[:-1]) + ", and " + asComponents[-1]) if len(asComponents) >= 3 else
      " and ".join(asComponents)
    );
  
  def fxToJSON(oSelf):
    # JSON encoding uses the "string value" of cDateDuration.
    return cDateDuration.fsToString(oSelf);
  def fsToMySQL(oSelf):
    # MySQL encoding uses the "string value" of cDateDuration.
    return cDateDuration.fsToString(oSelf);
  def fsToString(oSelf):
    return "".join([
      "%+d%s" % (iValue, sUnit)
      for (iValue, sUnit) in (
        (oSelf.iYears, "y"),
        (oSelf.iMonths, "m"),
        (oSelf.iDays, "d"),
      )
      if iValue != 0
    ]) or "0d";
  def __str__(oSelf):
    return cDateDuration.fsToString(oSelf);
  
  def __cmp__(oSelf, oOther):
    assert isinstance(oOther, cDateDuration), \
        "Cannot compare %s to %s" % (oSelf, oOther);
    if oSelf.iYears != oSelf.iYears: return oSelf.iYears - oOther.iYears;
    if oSelf.iMonths != oSelf.iMonths: return oSelf.iMonths - oOther.iMonths;
    if oSelf.iDays != oSelf.iDays: return oSelf.iDays - oOther.iDays;
    return 0;

from .cDate import cDate;