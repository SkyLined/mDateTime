"use strict";
const cDateDuration = (function(){
  const rDuration = new RegExp(
          "^\\s*" +
          "(?:([+-]?\\d+)\\s*y(?:ears?)?\\s*,?\\s*)?" +
          "(?:([+-]?\\d+)\\s*m(?:onths?)?\\s*,?\\s*)?" +
          "(?:([+-]?\\d+)\\s*d(?:ays?)?)?" +
          "\\s*$"
        );
  function fbIsValidInteger(xValue) {
    return typeof(xValue) == "number" && !isNaN(xValue) && xValue % 1 == 0;
  };
  function cDateDuration(iYears, iMonths, iDays) {
    if (!this) return new cDateDuration(iYears, iMonths, iDays);
    if (!fbIsValidInteger(iYears)) throw new Error("Invalid number of years " + JSON.stringify(iYears) + ".");
    if (!fbIsValidInteger(iMonths)) throw new Error("Invalid number of months " + JSON.stringify(iMonths) + ".");
    if (!fbIsValidInteger(iDays)) throw new Error("Invalid number of days " + JSON.stringify(iDays) + ".");
    this.__iYears = iYears;
    this.__iMonths = iMonths;
    this.__iDays = iDays;
  };
  // properties
  Object.defineProperty(cDateDuration.prototype, "iYears", {
    "get": function() { return this.__iYears; },
    "set": function(iYears) {
      if (!fbIsValidInteger(uYear)) throw new Error("Invalid number of years " + JSON.stringify(iYears) + ".");
      this.__iYears = iYears;
    },
  });
  Object.defineProperty(cDateDuration.prototype, "iMonths", {
    "get": function() { return this.__iMonths; },
    "set": function(iMonths) {
      if (!fbIsValidInteger(iMonths)) throw new Error("Invalid number of months " + JSON.stringify(iMonths) + ".");
      this.__iMonths = iMonths;
    },
  });
  Object.defineProperty(cDateDuration.prototype, "iDays", {
    "get": function() { return this.__iDays; },
    "set": function(uDasy) {
      if (!fbIsValidInteger(iDays)) throw new Error("Invalid number of days " + JSON.stringify(iDays) + ".");
      this.__iDays = iDays;
    },
  });
  // static methods
  cDateDuration.fo0FromJSON = function cDateDuration_fo0FromJSON(sDuration) {
    return sDuration === null ? null : cDateDuration.foFromJSON(sDuration);
  };
  cDateDuration.foFromJSON = function cDateDuration_foFromJSON(sDuration) {
    return cDateDuration.foFromString(sDuration);
  };
  cDateDuration.fbIsValidDurationString = function cDateDuration_fbIsValidDurationString(sDuration) {
    const oDurationMatch = typeof(sDuration) !== "string" ? null : sDuration.match(rDuration);
    return oDurationMatch !== null && (oDurationMatch[1] !== null || oDurationMatch[2] !== null || oDurationMatch[3] !== null);
  };
  cDateDuration.fo0FromString = function cDateDuration_fo0FromString(sDuration) {
    return sDuration === null ? null : this.foFromString(sDuration);
  };
  cDateDuration.foFromString = function cDateDuration_foFromString(sDuration) {
    const oDurationMatch = typeof(sDuration) !== "string" ? null : sDuration.match(rDuration);
    if (oDurationMatch === null || (oDurationMatch[1] === null && oDurationMatch[2] === null && oDurationMatch[3] === null)) {
      throw new Error("Invalid duration string " + JSON.stringify(sDuration));
    };
    return new cDateDuration(parseInt(oDurationMatch[1] || 0), parseInt(oDurationMatch[2] || 0), parseInt(oDurationMatch[3] || 0));
  };
  // methods
  cDateDuration.prototype.foClone = function cDateDuration_foClone() {
    return this.prototype.constructor(this.iYears, this.iMonths, this.iDays);
  };
  cDateDuration.prototype.fSet = function cDateDuration_fSet(iYears, iMonths, iDays) {
    if (iYears === undefined || iYears === null) iYears = this.__iYears;
    else if (!fbIsValidInteger(iYears)) throw new Error("Invalid number of years " + JSON.stringify(iYears) + ".");
    if (iMonths === undefined || iMonths === null) iMonths = this.__iMonths;
    else if (!fbIsValidInteger(iMonths)) throw new Error("Invalid number of months " + JSON.stringify(iMonths) + ".");
    if (iDays === undefined || iDays === null) iDays = this.__iDays;
    else if (!fbIsValidInteger(iDays)) throw new Error("Invalid number of days " + JSON.stringify(iDays) + ".");
    this.__iYears = iYears;
    this.__iMonths = iMonths;
    this.__iDays = iDays;
  };
  
  cDateDuration.prototype.foNormalizedForDate = function cDateDuration_foNormalizedForDate(oDate) {
    // Adjust duration to make all numbers either all positive or negative and minimze days, months and years.
    // e.g. "+2y-12m+32d" for "2000-01-01" => "+1y+1m+1d"
    return oDate.foGetDurationForEndDate(oDate.foGetEndDateForDuration(this));
  };
  
  cDateDuration.prototype.foAdd = function cDateDuration_fAdd(oOtherDuration) {
    this.fSet(this.iYears + oOtherDuration.iYears, this.iMonths + oOtherDuration.iMonths, this.iDays + oOtherDuration.iDays);
    return this;
  };
  cDateDuration.prototype.foSubtract = function cDateDuration_fSubtract(oOtherDuration) {
    this.fSet(this.iYears - oOtherDuration.iYears, this.iMonths - oOtherDuration.iMonths, this.iDays - oOtherDuration.iDays);
    return this;
  };
  cDateDuration.prototype.foPlus = function cDateDuration_fPlus(oOtherDuration) {
    return this.foClone().foAdd(oOtherDuration);
  };
  cDateDuration.prototype.foMinus = function cDateDuration_fMinus(oOtherDuration) {
    return this.foClone().foSubtract(oOtherDuration);
  };
  
  cDateDuration.prototype.fbIsZero = function cDateDuration_fbIsZero() {
    return this.iYears == 0 && this.iMonths == 0 && this.iDays == 0;
  };
  cDateDuration.prototype.fbIsPositive = function cDateDuration_fbIsPositive() {
    return this.iYears >= 0 && this.iMonths >= 0 && this.iDays >= 0 && !this.fbIsZero();
  };
  cDateDuration.prototype.fbIsNegative = function cDateDuration_fbIsNegative() {
    return this.iYears <= 0 && this.iMonths <= 0 && this.iDays <= 0 && !this.fbIsZero();
  };
  cDateDuration.prototype.fbIsNormalized = function cDateDuration_fbIsNormalized() {
    return this.fbIsZero() || this.fbIsPositive() || this.fbIsNegative();
  };
  
  
  cDateDuration.prototype.fsToHumanReadableString = function cDateDuration_fsToHumanReadableString() {
    if (this.fbIsZero()) return "0 days";
    if (!this.fbIsNormalized()) throw new Error("Duration must be normalized before converting to human readable string!");
    // Show positive and negative durations the same.
    const iYears = Math.abs(this.__iYears), iMonths = Math.abs(this.__iMonths), iDays = Math.abs(this.__iDays);
    const asComponents = [
            iYears == 1 ? "1 year" : iYears ? iYears.toString() + " years" : "",
            iMonths == 1 ? "1 month" : iMonths ? iMonths.toString() + " months" : "",
            iDays == 1 ? "1 day" : iDays ? iDays.toString() + " days" : "",
          ].filter(s => s);
    return asComponents.length == 3 ?
        asComponents[0] + ", " + asComponents[1] + ", and " + asComponents[2] :
        asComponents.join(" and ");
  };
  
  cDateDuration.prototype.fxToJSON = function cDateDuration_fxToJSON() {
    return this.fsToString();
  };
  cDateDuration.prototype.fsToString = function cDateDuration_fsToString() {
    if (this.fbIsZero()) return "0d";
    // months sign is required if months are negative, or months are positive and years are negative.
    const sMonthsSign = (this.__iMonths < 0 ? "-" : this.__iYears < 0 ? "+" : ""),
          // days sign is required if days are negative or days are positive and months are negative or if months are zero and years are negative.
          sDaysSign = (this.__iDays < 0 ? "-" : this.__iMonths < 0 || (this.__iMonths == 0 && this.__iYears < 0) ? "+" : "");
    return [
      this.__iYears ? this.__iYears.toString() + "y" : "",
      this.__iMonths ? sMonthsSign + Math.abs(this.__iMonths).toString() + "m" : "",
      this.__iDays ? sDaysSign + Math.abs(this.__iDays).toString() + "d" : "",
    ].join("");
  };
  cDateDuration.prototype.toString = function cDateDuration_toString() {
    return this.fsToString();
  };
  return cDateDuration;
})();