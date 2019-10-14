"use strict";
const cDate = (function() {
  const rDate = new RegExp(
          "^\\s*" +
          "(\\d{4})" + "[\\-\\/]" +
          "(\\d{1,2})" + "[\\-\\/]" + 
          "(\\d{1,2})" +
          "\\s*$"
        ),
        asMonths = [
          "January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"
        ],
        asOrdinalPostfixes = [
          "st", "nd", "rd", "th", "th", "th", "th", "th", "th", "th", # 1-10
          "th", "th", "th", "th", "th", "th", "th", "th", "th", "th", # 11-20
          "st", "nd", "rd", "th", "th", "th", "th", "th", "th", "th", # 21-30
          "st"                                                        # 31
        ];
  function fbIsValidYear(xYear) {
    return typeof(xYear) == "number" && !isNaN(xYear);
  };
  function fbIsValidMonth(xMonth) {
    return typeof(xMonth) == "number" && !isNaN(xMonth) && xMonth >= 1 && xMonth <= 12;
  };
  function fbIsValidDay(xDay) {
    return typeof(xDay) == "number" && !isNaN(xDay) && xDay >= 1 && xDay <= 31;
  };
  function fbIsValidDate(uYear, uMonth, uDay) {
    return uDay <= new Date(uYear, uMonth, 0).getDate();
  };
  function fsGetDateString(uYear, uMonth, uDay) {
    return [
      uYear.toString().padStart(4, "0"), 
      uMonth.toString().padStart(2, "0"), 
      uDay.toString().padStart(2, "0"),
    ].join("-");
  };
  function fuGetLastDayInMonth0Based(uYear, uMonth0Based) {
    return new Date(uYear, uMonth0Based + 1, 0).getDate();
  };
  
  // constructor
  function cDate(uYear, uMonth, uDay) {
    if (!this) return new cDate(uYear, uMonth, uDay);
    if (!fbIsValidYear(uYear)) throw new Error("Invalid year " + JSON.stringify(uYear) + ".");
    if (!fbIsValidMonth(uMonth)) throw new Error("Invalid month " + JSON.stringify(uMonth) + ".");
    if (!fbIsValidDay(uDay)) throw new Error("Invalid day " + JSON.stringify(uDay) + ".");
    if (!fbIsValidDate(uYear, uMonth, uDay)) throw new Error("Invalid date " + fsGetDateString(uYear, uMonth, uDay) + ".");
    this.__uYear = uYear;
    this.__uMonth = uMonth; // 1 = January
    this.__uDay = uDay; // 1 = first day of month
  };
  // properties
  Object.defineProperty(cDate.prototype, "uYear", {
    "get": function() { return this.__uYear; },
    "set": function(uYear) {
      if (!fbIsValidYear(uYear)) throw new Error("Invalid year " + JSON.stringify(uYear) + ".");
      if (!fbIsValidDate(uYear, this.__uMonth, this.__uDay)) throw new Error("Invalid year in date " + fsGetDateString(uYear, this.__uMonth, this.__uDay) + ".");
      this.__uYear = uYear;
    },
  });
  Object.defineProperty(cDate.prototype, "uMonth", {
    "get": function() { return this.__uMonth; },
    "set": function(uMonth) {
      if (!fbIsValidMonth(uMonth)) throw new Error("Invalid month " + JSON.stringify(uMonth) + ".");
      if (!fbIsValidDate(this.__uYear, uMonth, this.__uDay)) throw new Error("Invalid month in date " + fsGetDateString(this.__uYear, uMonth, this.__uDay) + ".");
      this.__uMonth = uMonth;
    },
  });
  Object.defineProperty(cDate.prototype, "uDay", {
    "get": function() { return this.__uDay; },
    "set": function(uDay) {
      if (!fbIsValidDay(uDay)) throw new Error("Invalid day " + JSON.stringify(uDay) + ".");
      if (!fbIsValidDate(this.__uYear, this.__uMonth, uDay)) throw new Error("Invalid day in date " + fsGetDateString(this.__uYear, this.__uMonth, uDay) + ".");
      this.__uDay = uDay;
    },
  });
  // static methods
  cDate.fo0FromJSDate = function cDate_fo0FromJSDate(oDate) {
    return oDate === null ? null : cDate.foFromJSDate(oDate);
  };
  cDate.foFromJSDate = function cDate_foFromJSDate(oDate) {
    return new cDate(oDate.getFullYear(), oDate.getMonth() + 1, oDate.getDate());
  };
  cDate.fo0FromJSON = function cDate_fo0FromJSON(s0Date) {
    return s0Date === null ? null : cDate.foFromJSON(s0Date);
  };
  cDate.foFromJSON = function cDate_foFromJSON(sDate) {
    return cDate.foFromString(sDate);
  };
  cDate.fbIsValidDateString = function cDate_fbIsValidDateString(sDate) {
    return typeof(sDate) === "string" && sDate.match(rDate) !== null;
  };
  cDate.fo0FromString = function cDate_fo0FromString(s0Date) {
    return s0Date === null ? null : cDate.foFromString(s0Date);
  };
  cDate.foFromString = function cDate_foFromString(sDate) {
    const oDateMatch = typeof(sDate) === "string" ? sDate.match(rDate) : null;
    if (oDateMatch === null) throw new Error("Invalid date string " + JSON.stringify(sDate) + ".");
    return new cDate(parseInt(oDateMatch[1]), parseInt(oDateMatch[2]), parseInt(oDateMatch[3]));
  };
  cDate.foNow = function cDate_foNow() {
    const oNow = new Date();
    return new cDate(oNow.getFullYear(), oNow.getMonth() + 1, oNow.getDate());
  };
  cDate.foNowUTC = function cDate_foNowUTC() {
    const oNow = new Date();
    return new cDate(oNow.getUTCFullYear(), oNow.getUTCMonth() + 1, oNow.getUTCDate());
  };
  // methods
  cDate.prototype.foClone = function cDate_foClone() {
    return new this.constructor(this.__uYear, this.__uMonth, this.__uDay);
  };
  cDate.prototype.fSet = function cDate_fSet(uYear, uMonth, uDay) {
    if (uYear === undefined || uYear === null) uYear = this.__uYear;
    else if (!fbIsValidYear(uYear)) throw new Error("Invalid year " + JSON.stringify(uYear) + ".");
    if (uMonth === undefined || uMonth === null) uMonth = this.__uMonth;
    else if (!fbIsValidMonth(uMonth)) throw new Error("Invalid month " + JSON.stringify(uMonth) + ".");
    if (uDay === undefined || uDay === null) uDay = this.__uDay;
    else if (!fbIsValidDay(uDay)) throw new Error("Invalid day " + JSON.stringify(uDay) + ".");
    if (!fbIsValidDate(uYear, this.__uMonth, this.__uDay)) throw new Error("Invalid date " + fsGetDateString(uYear, this.__uMonth, this.__uDay) + ".");
    this.__uYear = uYear;
    this.__uMonth = uMonth;
    this.__uDay = uDay;
  };
  cDate.prototype.foGetEndDateForDuration = function cDate_foEndDateForDuration(oDuration) {
    // Note that this code ignores the time (if any) in oDuration
    // Add the year and month:
    let uNewYear = this.__uYear + oDuration.iYears;
    let uNewMonth0Based = this.__uMonth - 1 + oDuration.iMonths;
    // If uNewMonth < 0 or > 11, convert the excess to years and add it.
    uNewYear += Math.floor(uNewMonth0Based / 12);
    uNewMonth0Based = ((uNewMonth0Based % 12) + (uNewMonth0Based < 0 ? 12 : 0)) % 12;
    // If we added months and ended up in another month in which the current day does not exist (e.g. Feb 31st)
    // reduce the day (i.e. Feb 28th/29th)
    const uLastDayInNewMonth = fuGetLastDayInMonth0Based(uNewYear, uNewMonth0Based),
          uNewDayInNewMonth = this.uDay <= uLastDayInNewMonth ? this.__uDay : uLastDayInNewMonth;
    // Add the days by creating the Python datetime.date equivalent and adding the days using datetime.timedelta, then
    // converting back to cDate. This allows us to reuse the Python API for tracking the number of days in each month.
    const oEndDate = cDate.foFromJSDate(
      new Date(uNewYear, uNewMonth0Based, uNewDayInNewMonth + oDuration.iDays)
    );
    return oEndDate;
  };
  cDate.prototype.foGetDurationForEndDate = function cDate_foGetDurationForEndDate(oEndDate) {
    // If the end date is before this date, the duration is going to be negative.
    // To keep this code simple to review, we always calculate the positive duration between the two dates
    // and later invert it should the real result be a negative duration.
    const bNegativeDuration = oEndDate.fbIsBefore(this),
          uDurationMultiplier = bNegativeDuration ? -1 : 1, // Used to potentially invert the duration later.
          oFirstDate = bNegativeDuration ? oEndDate : this,
          oLastDate = bNegativeDuration ? this : oEndDate;
    let uDurationYears = oLastDate.uYear - oFirstDate.uYear,
        uDurationMonths = oLastDate.uMonth - oFirstDate.uMonth,
        uDurationDays = oLastDate.uDay - oFirstDate.uDay,
        // The number of days in the last month various
        uDaysInLastDatesPreviousMonth = new Date(oLastDate.uYear - (oLastDate.uMonth == 1 ? 1 : 0), ((oLastDate.uMonth + 10) % 12 + 1), 0).getDate();
    if (uDurationDays >= oLastDate.uDay) {
      // If uDurationDays > last date's day, adding the days moved it into a new month; convert this into a month and adjust the days.
      // e.g. 2000-1-31 -> 2000-2-2 => -1m+29d (at this point) => +2d (after this adjustment)
      uDurationMonths += 1;
      uDurationDays = uDaysInLastDatesPreviousMonth - uDurationDays;
    } else if (uDurationDays < 0) {
      // If uDurationDays < 0, the day is before adding the days moved it into a new month; convert this into a month and adjust the days.
      // e.g. 2000-1-2 -> 2000-2-1 => +1m-1d (at this point) => +30d (after this adjustment)
      uDurationMonths -= 1;
      uDurationDays += uDaysInLastDatesPreviousMonth;
    };
    // If uDurationMonths < 0 or >= 12, convert the excess to years and add them.
    if (uDurationMonths < 0 || uDurationMonths >= 12) {
      uDurationYears += Math.floor(uDurationMonths / 12) + (uDurationMonths < 0 ? -1 : 0);
      uDurationMonths = (uDurationMonths % 12) + (uDurationMonths < 0 ? 12 : 0);
    };
    const oDuration = new cDateDuration(
            uDurationYears * uDurationMultiplier,
            uDurationMonths * uDurationMultiplier,
            uDurationDays * uDurationMultiplier,
          );
    return oDuration;
  };

  // This object has valueOf(), which returns the number of milliseconds since the epoch, so you can also
  // use (this.valueOf() < oDate.valueOf(), this.valueOf() == oDate.valueOf(), and this.valueOf() > oDate.valueOf())
  cDate.prototype.fbIsBefore = function cDate_fbIsBefore(oDate) {
    if (this.__uYear < oDate.uYear) return true;
    if (this.__uYear > oDate.uYear) return false;
    if (this.__uMonth < oDate.uMonth) return true;
    if (this.__uMonth > oDate.uMonth) return false;
    if (this.__uDay < oDate.uDay) return true;
    //if (this.__uDay > oDate.uDay) return false;
    return false;
  };
  cDate.prototype.fbIsEqualTo = function cDate_fbIsBefore(oDate) {
    return this.__uYear == oDate.uYear && this.__uMonth == oDate.uMonth && this.__uDay == oDate.uDay;
  };
  cDate.prototype.fbIsAfter = function cDate_fbIsAfter(oDate) {
    if (this.__uYear > oDate.uYear) return true;
    if (this.__uYear < oDate.uYear) return false;
    if (this.__uMonth > oDate.uMonth) return true;
    if (this.__uMonth < oDate.uMonth) return false;
    if (this.__uDay > oDate.uDay) return true;
    //if (this.__uDay < oDate.uDay) return false;
    return false;
  };

  cDate.prototype.fbIsInThePast = function cDate_fbIsInThePast() {
    return this.fbIsBefore(cDate.foNow());
  };
  cDate.prototype.fbIsInThePastUTC = function cDate_fbIsInThePastUTC() {
    return this.fbIsBefore(cDate.foNowUTC());
  };
  cDate.prototype.fbIsToday = function cDate_fbIsToday() {
    return this.fbIsEqualTo(cDate.foNow());
  };
  cDate.prototype.fbIsTodayUTC = function cDate_fbIsTodayUTC() {
    return this.fbIsEqualTo(cDate.foNowUTC());
  };
  cDate.prototype.fbIsInTheFuture = function cDate_fbIsInTheFuture() {
    return this.fbIsAfter(cDate.foNow());
  };
  cDate.prototype.fbIsInTheFutureUTC = function cDate_fbIsInTheFutureUTC() {
    return this.fbIsAfter(cDate.foNowUTC());
  };

  cDate.prototype.fsToHumanReadableString = function cDate_fsToHumanReadableString() {
    // Month <day>th, <year>
    return (
      asMonths[this.__uMonth - 1]
      + " " + this.__uDay.toString() + asOrdinalPostfixes[this.__uDay]
      + ", " + this.__uYear.toString()
    );
  };
  cDate.prototype.foToJSDate = function cDate_toJSDate() {
    return new Date(this.fsToString());
  };
  cDate.prototype.foToJSDateUTC = function cDate_toJSDateUTC() {
    return new Date(this.fsToString() + "T0:0Z");
  };
  cDate.prototype.fxToJSON = function cDate_fxToJSON() {
    return this.fsToString();
  };
  cDate.prototype.fsToString = function cDate_fsToString() {
    return fsGetDateString(this.__uYear, this.__uMonth, this.__uDay);
  };
  cDate.prototype.toString = function cDate_toString() {
    return this.fsToString();
  };
  cDate.prototype.valueOf = function cDate_valueOf() {
    return this.foToJSDate().valueOf();
  };
  return cDate;
})();
