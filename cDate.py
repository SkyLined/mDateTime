import calendar, datetime, math, re;

gbDebugOutput = False;

rDate = re.compile(
  r"^\s*" +
  r"(\d{4})" +
  r"[\-\/]" +
  r"(\d{1,2})" +
  r"[\-\/]" + 
  r"(\d{1,2})" +
  r"\s*$"
);
asMonths = [
  "January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December"
];
asOrdinalPostfixes = [
  "st", "nd", "rd", "th", "th", "th", "th", "th", "th", "th", # 1-10
  "th", "th", "th", "th", "th", "th", "th", "th", "th", "th", # 11-20
  "st", "nd", "rd", "th", "th", "th", "th", "th", "th", "th", # 21-30
  "st"                                                        # 31
];
def fbIsValidInteger(uValue, uMinValueInclusive = None, uMaxValueExclusive = None):
  return (
    isinstance(uValue, int)
    and (uValue % 1 == 0)
    and (uValue >= uMinValueInclusive if uMinValueInclusive is not None else True)
    and (uValue < uMaxValueExclusive if uMaxValueExclusive is not None else True)
  );

class cDate(object):
  # Static methods
  @staticmethod
  def fbIsValidYear(uValue):
    return fbIsValidInteger(uValue, 0);
  @staticmethod
  def fbIsValidMonth(uValue):
    return fbIsValidInteger(uValue, 1, 13);
  @staticmethod
  def fbIsValidDay(uValue):
    return fbIsValidInteger(uValue, 1, 32); # We do not know the month but 32 is never valid.
  @staticmethod
  def fbIsValidDate(uYear, uMonth, uDay):
    return (
      cDate.fbIsValidYear(uYear)
      and cDate.fbIsValidMonth(uMonth)
      and fbIsValidInteger(uDay, 1, cDate.fuGetLastDayInMonth(uYear, uMonth) + 1)
    );
  @staticmethod
  def fsGetDateString(uYear, uMonth, uDay):
    return "%04d-%02d-%02d" % (uYear, uMonth, uDay);
  @staticmethod
  def fuGetLastDayInMonth(uYear, uMonth):
    return calendar.monthrange(uYear, uMonth)[1];
  
  @staticmethod
  def fo0FromPyDate(oDate):
    return None if oDate is None else cDate.foFromPyDate(oDate);
  @staticmethod
  def foFromPyDate(oDate):
    return cDate(oDate.year, oDate.month, oDate.day);
  
  @staticmethod
  def fo0FromJSON(s0Date):
    return None if s0Date is None else cDate.foFromJSON(s0Date);
  @staticmethod
  def foFromJSON(sDate):
    # JSON encoding uses the "string value" of cDate.
    return cDate.foFromString(sDate);
  
  @staticmethod
  def fo0FromMySQL(s0Date):
    return None if s0Date is None else cDate.foFromMySQL(s0Date);
  @staticmethod
  def foFromMySQL(sDate):
    # MySQL encoding uses the "string value" of cDate.
    return cDate.foFromMySQL(sDate);
  @staticmethod
  def fo0FromMySQLDateTime(s0DateTime):
    return None if s0DateTime is None else cDate.foFromMySQLDateTime(s0DateTime);
  @staticmethod
  def foFromMySQLDateTime(sDateTime):
    # MySQL format is "YYYY-MM-DD hh:mm:ss", so we can just split it at the space and use the first part:
    return cDate.foFromMySQL(sDateTime.split(" ")[0]);
  
  @staticmethod
  def fbIsValidDateString(sDate):
    return isinstance(sDate, str) and rDate.match(sDate) is not None;
  @staticmethod
  def fo0FromString(s0Date):
    return None if s0Date is None else cDate.foFromString(s0Date);
  @staticmethod
  def foFromString(sDate):
    oDateMatch = rDate.match(sDate) if isinstance(sDate, str) else None;
    if oDateMatch is None: raise ValueError("Invalid date string " + repr(sDate) + ".");
    return cDate(int(oDateMatch.group(1)), int(oDateMatch.group(2)), int(oDateMatch.group(3)));
  
  @staticmethod
  def foNow():
    return cDate.foFromPyDate(datetime.datetime.now());
  @staticmethod
  def foNowUTC():
    return cDate.foFromPyDate(datetime.datetime.utcnow());
  
  # Constructor
  def __init__(oSelf, uYear, uMonth, uDay):
    if not cDate.fbIsValidDate(uYear, uMonth, uDay): raise ValueError("Invalid date (%s, %s, %s)." % (repr(uYear), repr(uMonth), uDay));
    oSelf.__uYear = uYear;
    oSelf.__uMonth = uMonth; # 1 = January
    oSelf.__uDay = uDay; # 1 = first day of month
  # Properties
  @property
  def uYear(oSelf):
    return oSelf.__uYear;
  @uYear.setter
  def uYear(oSelf, uYear):
    if not cDate.fbIsValidYear(uYear): raise ValueError("Invalid year " + repr(uYear) + ".");
    if not cDate.fbIsValidDate(uYear, oSelf.__uMonth, oSelf.__uDay): raise ValueError("Invalid year in date %s." % cDate.fsGetDateString(uYear, oSelf.__uMonth, oSelf.__uDay));
    oSelf.__uYear = uYear;
  @property
  def uMonth(oSelf):
    return oSelf.__uMonth;
  @uMonth.setter
  def uMonth(oSelf, uMonth):
    if not cDate.fbIsValidMonth(uMonth): raise ValueError("Invalid month " + repr(uMonth) + ".");
    if not cDate.fbIsValidDate(oSelf.__uYear, uMonth, oSelf.__uDay): raise ValueError("Invalid month in date %s." % cDate.fsGetDateString(oSelf.__uYear, uMonth, oSelf.__uDay));
    oSelf.__uMonth = uMonth;
  @property
  def uDay(oSelf):
    return oSelf.__uDay;
  @uDay.setter
  def uDay(oSelf, uDay):
    if not cDate.fbIsValidDay(uDay): raise ValueError("Invalid day " + repr(uDay) + ".");
    if not cDate.fbIsValidDate(oSelf.__uYear, oSelf.__uMonth, uDay): raise ValueError("Invalid day in date %s." % cDate.fsGetDateString(uYear, uMonth, uDay));
    oSelf.__uDay = uDay;
  #methods
  def foClone(oSelf):
    return cDate(oSelf.__uYear, oSelf.__uMonth, oSelf.__uDay);
  
  def fSet(oSelf, uYear, uMonth, uDay):
    if not cDate.fbIsValidDate(uYear, uMonth, uDay): raise ValueError("Invalid date (%s, %s, %s)." % (repr(uYear), repr(uMonth), uDay));
    oSelf.__uYear = uYear;
    oSelf.__uMonth = uMonth;
    oSelf.__uDay = uDay;
  
  def foGetEndDateForDuration(oSelf, oDuration):
    # Note that this code ignores the time (if any) in oDuration
    # Add the year and month:
    iNewYear = oSelf.__uYear + oDuration.iYears;
    iNewMonth0Based = oSelf.__uMonth - 1 + oDuration.iMonths;
    if gbDebugOutput: print("year %s %s %s => %s, month (base 0) %s %s %s => %s" % (
      repr(oSelf.__uYear), "-" if oDuration.iYears < 0 else "+", abs(oDuration.iYears), repr(iNewYear),
      repr(oSelf.__uMonth - 1), "-" if oDuration.iMonths < 0 else "+", abs(oDuration.iMonths), repr(iNewMonth0Based),
    ));
    # If uNewMonth < 0 or > 11, convert the excess/shortage to years and add it.
    iMonthsExcessOrShortageInYears = math.floor(iNewMonth0Based / 12);
    iNewYear += iMonthsExcessOrShortageInYears;
    assert iNewYear > 0, \
        "Year cannot be < 0 (%s)" % iNewYear;
    uNewYear = iNewYear;
    uNewMonth0Based = iNewMonth0Based % 12;
    uNewMonth = uNewMonth0Based + 1;
    if gbDebugOutput: print("year %s= %s => %s, month (base 0) %s => %s => base 1: %s" % (
      "-" if iMonthsExcessOrShortageInYears < 0 else "+", abs(iMonthsExcessOrShortageInYears), repr(uNewYear),
      repr(iNewMonth0Based), repr(uNewMonth0Based), repr(uNewMonth),
    ));
    # If we added months and ended up in another month in which the current day does not exist (e.g. Feb 31st)
    # reduce the day (i.e. Feb 28th/29th)
    uLastDayInNewMonth = cDate.fuGetLastDayInMonth(uNewYear, uNewMonth);
    uNewDayInNewMonth = oSelf.__uDay if oSelf.uDay <= uLastDayInNewMonth else uLastDayInNewMonth;
    if gbDebugOutput and uNewDayInNewMonth != oSelf.__uDay: print("day %d => %d" % (
      oSelf.__uDay, uNewDayInNewMonth
    ));
    # Add the days by creating the Python datetime.date equivalent and adding the days using datetime.timedelta, then
    # converting back to cDate. This allows us to reuse the Python API for tracking the number of days in each month.
    oEndDate = cDate.foFromPyDate(
      datetime.date(uNewYear, uNewMonth, uNewDayInNewMonth)
      + datetime.timedelta(oDuration.iDays)
    );
    return oEndDate;
  
  def foGetDurationForEndDate(oSelf, oEndDate):
    if gbDebugOutput: print("=== cDate.foGetDurationForEndDate(%s, %s) ===" % (str(oSelf), str(oEndDate)));
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
    if gbDebugOutput: print("  1: %+dy%+dm%+dd*%+d" % (uDurationYears, uDurationMonths, uDurationDays, uDurationMultiplier));
    # The number of days in the last month various
    uDaysInLastDatesPreviousMonth = cDate.fuGetLastDayInMonth(oLastDate.uYear - (1 if oLastDate.uMonth == 1 else 0), ((oLastDate.uMonth + 10) % 12) + 1);
    if uDurationDays >= oLastDate.uDay:
      # If uDurationDays > last date's day, adding the days moved it into a new month; convert this into a month and adjust the days.
      # e.g. 2000-1-31 -> 2000-2-2 => -1m+29d (at this point) => +2d (after this adjustment)
      uDurationMonths += 1;
      uDurationDays = uDaysInLastDatesPreviousMonth - uDurationDays;
      if gbDebugOutput: print("  2: d->m: %+dy%+dm%+dd*%+d" % (uDurationYears, uDurationMonths, uDurationDays, uDurationMultiplier));
    elif uDurationDays < 0:
      # If uDurationDays < 0, the day is before adding the days moved it into a new month; convert this into a month and adjust the days.
      # e.g. 2000-1-2 -> 2000-2-1 => +1m-1d (at this point) => +30d (after this adjustment)
      uDurationMonths -= 1;
      uDurationDays += uDaysInLastDatesPreviousMonth;
      if gbDebugOutput: print("  2: d->m: %+dy%+dm%+dd*%+d" % (uDurationYears, uDurationMonths, uDurationDays, uDurationMultiplier));
    # If uDurationMonths < 0 or >= 12, convert the excess to years and add them.
    if uDurationMonths < 0 or uDurationMonths >= 12:
      uDurationYears += math.floor(uDurationMonths / 12);
      uDurationMonths = uDurationMonths % 12;
      if gbDebugOutput: print("  3: m->y: %+dy%+dm%+dd*%+d" % (uDurationYears, uDurationMonths, uDurationDays, uDurationMultiplier));
    from .cDateDuration import cDateDuration;
    oDuration = cDateDuration(
      uDurationYears * uDurationMultiplier,
      uDurationMonths * uDurationMultiplier,
      uDurationDays * uDurationMultiplier,
    );
    if gbDebugOutput: print("=> return %s" % oDuration);
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
    return cDate.fbIsBefore(oSelf, cDate.foNow());
  def fbIsInThePastUTC(oSelf):
    return cDate.fbIsBefore(oSelf, cDate.foNowUTC());
  def fbIsToday(oSelf):
    return cDate.fbIsEqualTo(oSelf, cDate.foNow());
  def fbIsTodayUTC(oSelf):
    return cDate.fbIsEqualTo(oSelf, cDate.foNowUTC());
  def fbIsInTheFuture(oSelf):
    return cDate.fbIsAfter(oSelf, cDate.foNow());
  def fbIsInTheFutureUTC(oSelf):
    return cDate.fbIsAfter(oSelf, cDate.foNowUTC());
  
  def fsToHumanReadableString(oSelf):
    # Month <day>th, <year>
    return "%s %d%s, %d" % (
      asMonths[oSelf.__uMonth - 1],
      oSelf.__uDay, asOrdinalPostfixes[oSelf.__uDay],
      oSelf.__uYear,
    );
  def foToPyDate(oSelf):
    return datetime.date(oSelf.__uYear, oSelf.__uMonth, oSelf.__uDay);
  def fnToTimestamp(oSelf):
    return time.mktime(cDate.foToPyDate(oSelf).timetuple()) + (oSelf.uMicrosecond / 1000.0 / 1000);
  def fxToJSON(oSelf):
    # JSON encoding uses the "string value" of cDate.
    return cDate.fsToString(oSelf);
  def fsToMySQL(oSelf):
    # MySQL encoding uses the "string value" of cDate.
    return cDate.fsToString(oSelf);
  def fsToString(oSelf):
    return cDate.fsGetDateString(oSelf.__uYear, oSelf.__uMonth, oSelf.__uDay);
  def __str__(oSelf):
    return cDate.fsToString(oSelf);
  
  def __cmp__(oSelf, oOther):
    assert isinstance(oOther, cDate), \
        "Cannot compare %s to %s" % (oSelf, oOther);
    if oSelf.uYear != oSelf.uYear: return oSelf.uYear - oOther.uYear;
    if oSelf.uMonth != oSelf.uMonth: return oSelf.uMonth - oOther.uMonth;
    if oSelf.uDay != oSelf.uDay: return oSelf.uDay - oOther.uDay;
    return 0;
