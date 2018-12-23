import calendar, datetime, re;

rDate = re.compile(
  "^\\s*" +
  "(\\d{4})" + "[\\-\\/]" +
  "(\\d{1,2})" + "[\\-\\/]" + 
  "(\\d{1,2})" +
  "\\s*$"
);
asMonths = [
  "January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December"
];
asOrdinalPostfixes = [
  "th", "st", "nd", "rd", "th", "th", "th", "th", "th", "th"
];
def fbIsValidYear(uYear):
  return type(uYear) in [long, int, float] and uYear % 1 == 0;
def fbIsValidMonth(uMonth):
  return type(uMonth) in [long, int, float] and uMonth % 1 == 0 and uMonth >= 1 and uMonth <= 12;
def fbIsValidDay(uDay):
  return type(uDay) in [long, int, float] and uDay % 1 == 0 and uDay >= 1 and uDay <= 31;
def fbIsValidDate(uYear, uMonth, uDay):
  return type(uDay) in [long, int, float] and uMonth % 1 == 0 and uDay >= 1 and uDay <= calendar.monthrange(uYear, uMonth)[1];
def fsGetDateString(uYear, uMonth, uDay):
  return "%04d-%02d-%02d" % (uYear, uMonth, uDay);

class cDate(object):
  # constructor
  def __init__(oSelf, uYear, uMonth, uDay):
    if not fbIsValidYear(uYear): raise ValueError("Invalid year " + repr(uYear) + ".");
    if not fbIsValidMonth(uMonth): raise ValueError("Invalid month " + repr(uMonth) + ".");
    if not fbIsValidDay(uDay): raise ValueError("Invalid day " + repr(uDay) + ".");
    if not fbIsValidDate(uYear, uMonth, uDay): raise ValueError("Invalid date %s." % fsGetDateString(uYear, uMonth, uDay));
    oSelf.__uYear = uYear;
    oSelf.__uMonth = uMonth; # 1 = January
    oSelf.__uDay = uDay; # 1 = first day of month
  #properties
  @property
  def uYear(oSelf):
    return oSelf.__uYear;
  @uYear.setter
  def uYear(oSelf, uYear):
    if not fbIsValidYear(uYear): raise ValueError("Invalid year " + repr(uYear) + ".");
    if not fbIsValidDate(uYear, oSelf.uMonth, oSelf.uDay): raise ValueError("Invalid year in date %s." % fsGetDateString(uYear, oSelf.uMonth, oSelf.uDay));
    oSelf.__uYear = uYear;
  @property
  def uMonth(oSelf):
    return oSelf.__uMonth;
  @uMonth.setter
  def uMonth(oSelf, uMonth):
    if not fbIsValidMonth(uMonth): raise ValueError("Invalid month " + repr(uMonth) + ".");
    if not fbIsValidDate(oSelf.uYear, uMonth, oSelf.uDay): raise ValueError("Invalid month in date %s." % fsGetDateString(oSelf.uYear, uMonth, oSelf.uDay));
    oSelf.__uMonth = uMonth;
  @property
  def uDay(oSelf):
    return oSelf.__uDay;
  @uDay.setter
  def uDay(oSelf, uDay):
    if not fbIsValidDay(uDay): raise ValueError("Invalid day " + repr(uDay) + ".");
    if not fbIsValidDate(oSelf.uYear, oSelf.uMonth, uDay): raise ValueError("Invalid day in date %s." % fsGetDateString(uYear, uMonth, uDay));
    oSelf.__uDay = uDay;
  #static
  @classmethod
  def fo0FromPyDate(cClass, oDate):
    return None if oDate is None else cClass.foFromJSDate(oDate);
  @classmethod
  def foFromPyDate(cClass, oDate):
    return cClass(oDate.year, oDate.month, oDate.day);
  @classmethod
  def fo0FromJSON(cClass, s0Date):
    return None if s0Date is None else cClass.foFromJSON(s0Date);
  @classmethod
  def foFromJSON(cClass, sDate):
    return cClass.foFromString(sDate);
  @staticmethod
  def fbIsValidDateString(sDate):
    return type(sDate) in [str, unicode] and rDate.match(sDate) is not None;
  @classmethod
  def fo0FromString(cClass, s0Date):
    return None if s0Date is None else cClass.foFromString(s0Date);
  @classmethod
  def foFromString(cClass, sDate):
    oDateMatch = rDate.match(sDate) if type(sDate) in [str, unicode] else None;
    if oDateMatch is None: raise ValueError("Invalid date string " + repr(sDate) + ".");
    return cDate(long(oDateMatch.group(1)), long(oDateMatch.group(2)), long(oDateMatch.group(3)));
  @classmethod
  def foNow(cClass):
    return cClass.foFromPyDate(datetime.datetime.now());
  @classmethod
  def foUTCNow(cClass):
    return cClass.foFromPyDate(datetime.datetime.utcnow());
  #methods
  def foClone(oSelf):
    return oSelf.__class__(oSelf.uYear, oSelf.uMonth, oSelf.uDay);
  
  def fSet(oSelf, uYear, uMonth, uDay):
    if not fbIsValidYear(uYear): raise ValueError("Invalid year " + repr(uYear) + ".");
    if not fbIsValidMonth(uMonth): raise ValueError("Invalid month " + repr(uMonth) + ".");
    if not fbIsValidDay(uDay): raise ValueError("Invalid day " + repr(uDay) + ".");
    if not fbIsValidDate(uYear, uMonth, uDay): raise ValueError("Invalid date " + fsGetDateString(uYear, uMonth, uDay) + ".");
    oSelf.__uYear = uYear;
    oSelf.__uMonth = uMonth;
    oSelf.__uDay = uDay;
  
  def foGetEndDateForDuration(oSelf, oDuration):
    # Note that this code ignores the time (if any) in oDuration
    # Add the year and month:
    uNewYear = oSelf.uYear + oDuration.iYears;
    uNewMonth0Based = oSelf.uMonth - 1 + oDuration.iMonths;
    # If uNewMonth < 0 or > 11, convert the excess to years and add it.
    uNewYear += long(uNewMonth0Based / 12);
    uNewMonth0Based = ((uNewMonth0Based % 12) + (12 if uNewMonth0Based < 0 else 0)) % 12;
    # Add the days by creating the Python datetime.date equivalent and adding the days using datetime.timedelta, then
    # converting back to cDate. This allows us to reuse the Python API for tracking the number of days in each month.
    oEndDate = oSelf.foFromPyDate(
      datetime.date(uNewYear, (uNewMonth0Based + 1), oSelf.uDay)
      + datetime.timedelta(oDuration.iDays)
    );
    return oEndDate;
  
  def foGetDurationForEndDate(oSelf, oEndDate):
    # If the end date is before this date, the duration is going to be negative.
    # To keep this code simple to review, we always calculate the positive duration between the two dates
    # and later invert it should the real result be a negative duration.
    bNegativeDuration = oEndDate.fbIsBefore(oSelf);
    uDurationMultiplier = -1 if bNegativeDuration else 1; # Used to potentially invert the duration later.
    oFirstDate = oEndDate if bNegativeDuration else oSelf;
    oLastDate = oSelf if bNegativeDuration else oEndDate;
    uDurationYears = oLastDate.uYear - oFirstDate.uYear;
    uDurationMonths = oLastDate.uMonth - oFirstDate.uMonth;
    uDurationDays = oLastDate.uDay - oFirstDate.uDay;
    # The number of days in the last month various
    uDaysInLastDatesPreviousMonth = calendar.monthrange(oLastDate.uYear - (1 if oLastDate.uMonth == 1 else 0), ((oLastDate.uMonth + 10) % 12) + 1)[1];
    if uDurationDays >= oLastDate.uDay:
      # If uDurationDays > last date's day, adding the days moved it into a new month; convert this into a month and adjust the days.
      # e.g. 2000-1-31 -> 2000-2-2 => -1m+29d (at this point) => +2d (after this adjustment)
      uDurationMonths += 1;
      uDurationDays = uDaysInLastDatesPreviousMonth - uDurationDays;
    elif uDurationDays < 0:
      # If uDurationDays < 0, the day is before adding the days moved it into a new month; convert this into a month and adjust the days.
      # e.g. 2000-1-2 -> 2000-2-1 => +1m-1d (at this point) => +30d (after this adjustment)
      uDurationMonths -= 1;
      uDurationDays += uDaysInLastDatesPreviousMonth;
    # If uDurationMonths < 0 or >= 12, convert the excess to years and add them.
    if uDurationMonths < 0 or uDurationMonths >= 12:
      uDurationYears += Math.floor(uDurationMonths / 12) + (-1 if uDurationMonths < 0 else 0);
      uDurationMonths = (uDurationMonths % 12) + (12 if uDurationMonths < 0 else 0);
    from cDateDuration import cDateDuration;
    oDuration = cDateDuration(
      uDurationYears * uDurationMultiplier,
      uDurationMonths * uDurationMultiplier,
      uDurationDays * uDurationMultiplier,
    );
    return oDuration;
  
  def fbIsBefore(oSelf, oDate):
    if oSelf.__uYear < oDate.uYear: return True;
    if oSelf.__uYear > oDate.uYear: return False;
    if oSelf.__uMonth < oDate.uMonth: return True;
    if oSelf.__uMonth > oDate.uMonth: return False;
    if oSelf.__uDay < oDate.uDay: return True;
    #if oSelf.__uDay > oDate.uDay: return False;
    return False;
  def fbIsEqualTo(oSelf, oDate):
    return oSelf.__uYear == oDate.uYear and oSelf.__uMonth == oDate.uMonth and oSelf.__uDay == oDate.uDay;
  def fbIsAfter(oSelf, oDate):
    if oSelf.__uYear > oDate.uYear: return True;
    if oSelf.__uYear < oDate.uYear: return False;
    if oSelf.__uMonth > oDate.uMonth: return True;
    if oSelf.__uMonth < oDate.uMonth: return False;
    if oSelf.__uDay > oDate.uDay: return True;
    #if oSelf.__uDay < oDate.uDay: return False;
    return False;
  
  def fbIsInThePast(oSelf):
    return oSelf.fbIsBefore(oSelf.foNow());
  def fbIsInThePast(oSelf):
    return oSelf.fbIsBefore(oSelf.foNowUTC());
  def fbIsToday(oSelf):
    return oSelf.fbIsEqualTo(oSelf.foNow());
  def fbIsTodayUTC(oSelf):
    return oSelf.fbIsEqualTo(oSelf.foNowUTC());
  def fbIsInTheFuture(oSelf):
    return oSelf.fbIsAfter(oSelf.foNow());
  def fbIsInTheFutureUTC(oSelf):
    return oSelf.fbIsAfter(oSelf.foNowUTC());

  def fsToHumanReadableString(oSelf):
    # Month <day>th, <year>
    return "%s %d%s, %d" % (
      asMonths[oSelf.uMonth - 1],
      oSelf.uDay, asOrdinalPostfixes[oSelf.uDay % 10],
      oSelf.uYear,
    );
  def foToPyDate(oSelf):
    return datetime.date(oSelf.uYear, oSelf.uMonth, oSelf.uDay);
  def fxToJSON(oSelf):
    return str(oSelf);
  def fsToString(oSelf):
    return fsGetDateString(oSelf.uYear, oSelf.uMonth, oSelf.uDay);
  def __str__(oSelf):
    return oSelf.fsToString();
