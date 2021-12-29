import math, re;

gbDebugOutput = False;

rDateDuration = re.compile(
  "^\\s*" +
  "(?:([+-]?\\d+)\\s*y(?:ears?)?\\s*,?\\s*)?" +
  "(?:([+-]?\\d+)\\s*m(?:onths?)?\\s*,?\\s*)?" +
  "(?:([+-]?\\d+)\\s*d(?:ays?)?)?" +
  "\\s*$"
);
def fbIsValidInteger(uValue):
  return isinstance(uValue, (int, float)) and uValue % 1 == 0;

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
    oDurationMatch = rDateDuration.match(sDuration) if isinstance(sDuration, str) else None;
    return oDurationMatch is not None and any([sComponent is not None for sComponent in oDurationMatch.groups()]);
  @staticmethod
  def fo0FromString(sDuration):
    return None if sDuration is None else cDateDuration.foFromString(sDuration);
  @staticmethod
  def foFromString(sDuration):
    oDurationMatch = rDateDuration.match(sDuration) if isinstance(sDuration, str) else None;
    asDurationMatchGroups = oDurationMatch.groups() if oDurationMatch is not None else None
    if oDurationMatch is None or all([sComponent is None for sComponent in asDurationMatchGroups]):
      raise ValueError("Invalid duration string " + repr(sDuration));
    sYears, sMonths, sDays = oDurationMatch.groups();
    # Values may not contain a sign, in which case the sign is assumed to be +
    # "-1y2m+3d" => "-1y+2m+3d"
    iYears = int(sYears) if sYears else 0;
    iMonths = int(sMonths) if sMonths else 0;
    iDays = int(sDays) if sDays else 0;
    return cDateDuration(iYears, iMonths, iDays);
  # Constructor
  def __init__(oSelf, iYears = 0, iMonths = 0, iDays = 0):
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
    # We cannot do this for days, as the number of days in a month varies by month.
    def ftxGetValueInRangeAndOverflow(iValue, uMaxValue):
      iValueInRange = iValue % uMaxValue;
      iOverflow = math.floor((iValue - iValueInRange) / uMaxValue);
      return (iValueInRange, iOverflow);
    oSelf.iMonths, iOverflowedYears = ftxGetValueInRangeAndOverflow(oSelf.iMonths, 12);
    oSelf.iYears = oSelf.iYears + iOverflowedYears;
    if gbDebugOutput: print("m->y: %s" % oSelf);
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
    if gbDebugOutput: print("+-m->y: %s" % oSelf);
  def foNormalized(oSelf):
    oNormalized = oSelf.foClone();
    cDateDuration.fNormalize(oNormalized);
    return oNormalized;
  def foNormalizedForDate(oSelf, oDate):
    # Adjust duration to make all numbers either all positive or negative and minimize days, months and years.
    # e.g. "+2y-12m+32d" for "2000-01-01" => "+1y+1m+1d"
    oEndDate = cDate.foGetEndDateForDuration(oDate, oSelf);
    if gbDebugOutput: print("%s + %s == %s" % (oDate, oSelf, oEndDate));
    oNormalizedDuration = cDate.foGetDurationForEndDate(oDate, oEndDate);
    if gbDebugOutput: print("%s == %s + %s" % (oEndDate, oDate, oNormalizedDuration));
    return oNormalizedDuration;
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
  
  def fasToHumanReadableStrings(oSelf):
    assert cDateDuration.fbIsSignNormalized(oSelf), \
        "Duration must be sign-normalized before converting to human readable string!";
    # Show positive and negative durations the same.
    uYears = abs(oSelf.iYears); uMonths = abs(oSelf.iMonths); uDays = abs(oSelf.iDays);
    return [sComponent for sComponent in [
      ("%d year%s"  % (uYears,  "" if uYears == 1  else "s")) if uYears  else None,
      ("%d month%s" % (uMonths, "" if uMonths == 1 else "s")) if uMonths else None,
      ("%d day%s"   % (uDays,   "" if uDays == 1   else "s")) if uDays   else None,
    ] if sComponent]
  def fsToHumanReadableString(oSelf, u0MaxNumberOfUnitsInOutput = None):
    asComponents = oSelf.fasToHumanReadableStrings();
    if u0MaxNumberOfUnitsInOutput is not None:
      asComponents = asComponents[:u0MaxNumberOfUnitsInOutput];
    if len(asComponents) == 0:
      return "0 days";
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
  def fasGetDetails(oSelf):
    return [oSelf.fsToString(), "%snormalized" % ("" if oSelf.fbIsNormalized() else "sign " if oSelf.fbIsSignNormalized() else "not ")];
  def __repr__(oSelf):
    sModuleName = ".".join(oSelf.__class__.__module__.split(".")[:-1]);
    return "<%s.%s#%X|%s>" % (sModuleName, oSelf.__class__.__name__, id(oSelf), "|".join(oSelf.fasGetDetails()));
  
  def __lt__(oSelf, oOther):
    assert isinstance(oOther, oSelf.__class__), \
        "Cannot compare %s to %s" % (oSelf, oOther);
    if oSelf.iDays < 28 and oOther.iDays < 28:
      return oSelf.iYears * 12 + oSelf.iMonths < oOther.iYears * 12 + oOther.iMonths;
    else:
      assert oSelf.iYears * 12 + oSelf.iMonths == oOther.iYears * 12 + oOther.iMonths, \
          "Cannot compare %s to %s because the number of years/months are different and the number of days > 28" % (
            oSelf, oOther
          );
      return oSelf.iDays < oOther.iDays
  def __le__(oSelf, oOther):
    return oSelf < oOther or oSelf == oOther;
  def __eq__(oSelf, oOther):
    assert isinstance(oOther, oSelf.__class__), \
        "Cannot compare %s to %s" % (oSelf, oOther);
    if oSelf.iDays < 28 and oOther.iDays < 28:
      return oSelf.iYears * 12 + oSelf.iMonths == oOther.iYears * 12 + oOther.iMonths;
    else:
      assert oSelf.iYears * 12 + oSelf.iMonths == oOther.iYears * 12 + oOther.iMonths, \
          "Cannot compare %s to %s because the number of years/months are different and the number of days > 28" % (
            oSelf, oOther
          );
      return oSelf.iDays == oOther.iDays
  def __gt__(oSelf, oOther):
    assert isinstance(oOther, oSelf.__class__), \
        "Cannot compare %s to %s" % (oSelf, oOther);
    if oSelf.iDays < 28 and oOther.iDays < 28:
      return oSelf.iYears * 12 + oSelf.iMonths > oOther.iYears * 12 + oOther.iMonths;
    else:
      assert oSelf.iYears * 12 + oSelf.iMonths == oOther.iYears * 12 + oOther.iMonths, \
          "Cannot compare %s to %s because the number of years/months are different and the number of days > 28" % (
            oSelf, oOther
          );
      return oSelf.iDays > oOther.iDays
  def __ge__(oSelf, oOther):
    return oSelf > oOther or oSelf == oOther;

from .cDate import cDate;