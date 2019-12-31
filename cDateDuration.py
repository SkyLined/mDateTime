import re;

rDuration = re.compile(
  "^\\s*" +
  "(?:([+-]?\\d+)\\s*y(?:ears?)?\\s*,?\\s*)?" +
  "(?:([+-]?\\d+)\\s*m(?:onths?)?\\s*,?\\s*)?" +
  "(?:([+-]?\\d+)\\s*d(?:ays?)?)?" +
  "\\s*$"
);
def fbIsValidInteger(uValue):
  return type(uValue) in [long, int, float] and uValue % 1 == 0;

class cDateDuration(object):
  def __init__(oSelf, iYears, iMonths, iDays):
    if not fbIsValidInteger(iYears): raise ValueError("Invalid number of years " + repr(iYears) + ".");
    if not fbIsValidInteger(iMonths): raise ValueError("Invalid number of months " + repr(iMonths) + ".");
    if not fbIsValidInteger(iDays): raise ValueError("Invalid number of days " + repr(iDays) + ".");
    oSelf.__iYears = iYears;
    oSelf.__iMonths = iMonths;
    oSelf.__iDays = iDays;
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
  def uMonth(oSelf, iMonths):
    if not fbIsValidInteger(iMonths): raise ValueError("Invalid number of months " + repr(iMonths) + ".");
    oSelf.__iMonths = iMonths;
  @property
  def iDays(oSelf):
    return oSelf.__iDays;
  @iDays.setter
  def uDay(oSelf, iDays):
    if not fbIsValidInteger(iDays): raise ValueError("Invalid number of days " + repr(iDays) + ".");
    oSelf.__iDays = iDays;
  # static methods
  @staticmethod
  def fbIsValidDurationString(sDuration):
    oDurationMatch = rDuration.match(sDuration) if type(sDuration) in [str, unicode] else None;
    return oDurationMatch is not None and any([sComponent is not None for sComponent in oDurationMatch.groups()]);
  
  @classmethod
  def fo0FromJSON(cClass, sDuration):
    return None if sDuration is None else cClass.foFromJSON(sDuration);
  @classmethod
  def foFromJSON(cClass, sDuration):
    # JSON encoding uses the "string value" of cDateDuration.
    return cClass.foFromString(sDuration);
  
  @classmethod
  def fo0FromMySQL(cClass, sDuration):
    return None if sDuration is None else cClass.foFromMySQL(sDuration);
  @classmethod
  def foFromMySQL(cClass, sDuration):
    # MySQL encoding uses the "string value" of cDateDuration.
    return cClass.foFromString(sMySQL);
  
  @classmethod
  def fo0FromString(cClass, sDuration):
    return None if sDuration is None else cClass.foFromString(sDuration);
  @classmethod
  def foFromString(cClass, sDuration):
    oDurationMatch = rDuration.match(sDuration) if type(sDuration) in [str, unicode] else None;
    asDurationMatchGroups = oDurationMatch.groups() if oDurationMatch is not None else None
    if oDurationMatch is None or all([sComponent is None for sComponent in asDurationMatchGroups]):
      raise ValueError("Invalid duration string " + repr(sDuration));
    return cDateDuration(*[0 if sComponent is None else long(sComponent) for sComponent in asDurationMatchGroups]);
  # methods
  def foClone(oSelf):
    return oSelf.__class__(oSelf.iYears, oSelf.iMonths, oSelf.iDays);
  def fSet(oSelf, iYears = None, iMonths = None, iDays = None):
    if iYears is None: iYears = oSelf.__iYears;
    elif not fbIsValidInteger(iYears): raise ValueError("Invalid number of years " + repr(iYears) + ".");
    if iMonths is None: iMonths = oSelf.__iMonths;
    elif not fbIsValidInteger(iMonths): raise ValueError("Invalid number of months " + repr(iMonths) + ".");
    if iDays is None: iDays = oSelf.__iDays;
    elif not fbIsValidInteger(iDays): raise ValueError("Invalid number of days " + repr(iDays) + ".");
    oSelf.__iYears = iYears;
    oSelf.__iMonths = iMonths;
    oSelf.__iDays = iDays;
  def foNormalizedForDate(oSelf, oDate):
    # Adjust duration to make all numbers either all positive or negative and minimze days, months and years.
    # e.g. "+2y-12m+32d" for "2000-01-01" => "+1y+1m+1d"
    return oDate.foGetDurationForEndDate(oDate.foGetEndDateForDuration(oSelf));
  
  def foAdd(oSelf, oOtherDuration):
    oSelf.fSet(oSelf.iYears + oOtherDuration.iYears, oSelf.iMonths + oOtherDuration.iMonths, oSelf.iDays + oOtherDuration.iDays);
    return oSelf;
  def foSubtract(oSelf, oOtherDuration):
    oSelf.fSet(oSelf.iYears - oOtherDuration.iYears, oSelf.iMonths - oOtherDuration.iMonths, oSelf.iDays - oOtherDuration.iDays);
    return oSelf;
  def foPlus(oSelf, oOtherDuration):
    return oSelf.foClone().foAdd(oOtherDuration);
  def foMinus(oSelf, oOtherDuration):
    return oSelf.foClone().foSubtract(oOtherDuration);
  
  def fbIsZero(oSelf):
    return oSelf.iYears == 0 and oSelf.iMonths == 0 and oSelf.iDays == 0;
  def fbIsPositive(oSelf):
    return oSelf.iYears >= 0 and oSelf.iMonths >= 0 and oSelf.iDays >= 0 and not oSelf.fbIsZero();
  def fbIsNegative(oSelf):
    return oSelf.iYears <= 0 and oSelf.iMonths <= 0 and oSelf.iDays <= 0 and not oSelf.fbIsZero();
  def fbIsNormalized(oSelf):
    return oSelf.fbIsZero() or oSelf.fbIsPositive() or oSelf.fbIsNegative();
  
  def fsToHumanReadableString(oSelf):
    if oSelf.fbIsZero(): return "0 days";
    if not oSelf.fbIsNormalized(): raise Error("Duration must be normalized before converting to human readable string!");
    # Show positive and negative durations the same.
    iYears = abs(oSelf.__iYears); iMonths = abs(oSelf.__iMonths); iDays = abs(oSelf.__iDays);
    asComponents = [sComponent for sComponent in [
      "1 year" if iYears == 1 else ("%d years" % iYears if iYears else ""),
      "1 month" if iMonths == 1 else ("%d months" % iMonths if iMonths else ""),
      "1 day" if iDays == 1 else ("%d days" % iDays if iDays else ""),
    ] if sComponent]
    return (asComponents[0] + ", " + asComponents[1] + ", and " + asComponents[2]) \
        if len(asComponents) == 3 else " and ".join(asComponents);
  
  def fxToJSON(oSelf):
    # JSON encoding uses the "string value" of cDateDuration.
    return oSelf.fsToString();
  def fsToMySQL(oSelf):
    # MySQL encoding uses the "string value" of cDateDuration.
    return oSelf.fsToString();
  def fsToString(oSelf):
    if oSelf.fbIsZero(): return "0d";
    # months sign is required if months are negative, or months are positive and years are negative.
    sMonthsSign = "-" if oSelf.__iMonths < 0 else "+" if oSelf.__iYears < 0 else "";
    # days sign is required if days are negative or days are positive and months are negative or if months are zero and years are negative.
    sDaysSign = "-" if oSelf.__iDays < 0 else "+" if oSelf.__iMonths < 0 or (oSelf.__iMonths == 0 and oSelf.__iYears < 0) else "";
    return "".join([
      "%sy" % oSelf.__iYears if oSelf.__iYears else "",
      "%s%dm" % (sMonthsSign, abs(oSelf.__iMonths)) if oSelf.__iMonths else "",
      "%s%dd" % (sDaysSign, abs(oSelf.__iDays)) if oSelf.__iDays else "",
    ]);
  def __str__(oSelf):
    return oSelf.fsToString();
