<?php
  namespace mDateTime;
  use \DateTime;
  use \DateTimeZone;
  use \Exception;
  use \JsonSerializable;
  CONST cDate_srDate = (
    "/^\\s*" .
    "(\\d{4})" . "[\\-\\/]" .
    "(\\d{1,2})" . "[\\-\\/]" . 
    "(\\d{1,2})" .
    "\\s*$/"
  );
  CONST cDate_asMonths = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
  ];
  CONST cDate_asOrdinalPostfixes = [
    "th", "st", "nd", "rd", "th", "th", "th", "th", "th", "th"
  ];
  function fbIsValidYear($xYear) {
    return is_int($xYear);
  };
  function fbIsValidMonth($xMonth) {
    return is_int($xMonth) && $xMonth >= 1 && $xMonth <= 12;
  };
  function fbIsValidDay($xDay) {
    return is_int($xDay) && $xDay >= 1 && $xDay <= 31;
  };
  function fbIsValidDate($uYear, $uMonth, $uDay) {
    return $uDay <= cal_days_in_month(CAL_GREGORIAN, $uMonth, $uYear);
  };
  function fsGetDataString($uYear, $uMonth, $uDay) {
    return (
      str_pad($uYear, 4, "0", STR_PAD_LEFT)
      . "-" . str_pad($uMonth, 2, "0", STR_PAD_LEFT)
      . "-" . str_pad($uDay, 2, "0", STR_PAD_LEFT)
    );
  };
  
  class cDate implements JsonSerializable {
    
    private $__uYear = null;
    private $__uMonth = null; // 1 = January
    private $__uDay = null; // 1 = first day of month
    
    # constructor
    function __construct($uYear, $uMonth, $uDay) {
      if (!fbIsValidYear($uYear)) throw new Exception("Invalid year " . json_encode($uYear) . ".");
      if (!fbIsValidMonth($uMonth)) throw new Exception("Invalid month " . json_encode($uMonth) . ".");
      if (!fbIsValidDay($uDay)) throw new Exception("Invalid day " . json_encode($uDay) . ".");
      if (!fbIsValidDate($uYear, $uMonth, $uDay)) throw new Exception("Invalid date " . fsGetDataString($uYear, $uMonth, $uDay) . ".");
      $this->__uYear = $uYear;
      $this->__uMonth = $uMonth;
      $this->__uDay = $uDay;
    }
    # properties
    function __get($sPropertyName) {
      if ($sPropertyName == "uYear") {
        return $this->__uYear;
      } else if ($sPropertyName == "uMonth") {
        return $this->__uMonth;
      } else if ($sPropertyName == "uDay") {
        return $this->__uDay;
      };
    }
    function __set($sPropertyName, $xValue) {
      if ($sPropertyName == "uYear") {
        if (!fbIsValidYear($xValue)) throw new Exception("Invalid year " . json_encode($xValue) . ".");
        if (!fbIsValidDate($xValue, $this->uMonth, $this->uDay))
            throw new Exception("Invalid year in date " . fsGetDataString($xValue, $this->uMonth, $this->uDay) . ".");
        $this->__uYear = $xValue;
      } else if ($sPropertyName == "uMonth") {
        if (!fbIsValidMonth($xValue)) throw new Exception("Invalid month " . json_encode($xValue) . ".");
        if (!fbIsValidDate($this->uYear, $xValue, $this->uDay))
            throw new Exception("Invalid month in date " . fsGetDataString($this->uYear, $xValue, $this->uDay) . ".");
        $this->__uMonth = $xValue;
      } else if ($sPropertyName == "uDay") {
        if (!fbIsValidDay($xValue)) throw new Exception("Invalid day " . json_encode($xValue) . ".");
        if (!fbIsValidDate($this->uYear, $this->uMonth, $xValue))
            throw new Exception("Invalid day in date " . fsGetDataString($this->uYear, $this->uMonth, $xValue) . ".");
        $this->__uDay = $xValue;
      };
    }
    # static methods
    public static function fo0FromPHPDateTime($oDateTime) {
      return is_null($oDateTime) ? null : cDate::foFromPHPDateTime($oDateTime);
    }
    public static function foFromPHPDateTime($oDateTime) {
      return new cDate((int)$oDateTime->format("Y"), (int)$oDateTime->format("m"), (int)$oDateTime->format("d"));
    }
    
    public static function fo0FromMYSQL($sDate) {
      return is_null($sDate) ? null : cDate::foFromMYSQL($sDate);
    }
    public static function foFromMYSQL($sDate) {
      // MYSQL happens to use the same serialization format as cDate does.
      return cDate::foFromString($sDate);
    }
    public static function fo0FromMYSQLDateTime($sDateTime) {
      return is_null($sDateTime) ? null : cDate::foFromMYSQLDateTime($sDateTime);
    }
    public static function foFromMYSQLDateTime($sDateTime) {
      // MYSQL format is "YYYY-MM-DD hh:mm:ss", so we can just split it at the space and use the first part:
      return cDate::foFromString(explode(" ", $sDateTime)[0]);
    }
    
    public static function fo0FromJSON($sDate) {
      return is_null($sDate) ? null : cDate::foFromJSON($sDate);
    }
    public static function foFromJSON($sDate) {
      // JSON encoding uses the "string value" of cDate.
      return cDate::foFromString($sDate);
    }
    
    public static function fbIsValidDateString($sDate) {
      return is_string($sDate) && preg_match(cDate_srDate, $sDate, $asMatch);
    }
    public static function fo0FromString($sDate) {
      return is_null($sDate) ? null : cDate::foFromString($sDate);
    }
    public static function foFromString($sDate) {
      if (!is_string($sDate) || !preg_match(cDate_srDate, $sDate, $asMatch)) {
        throw new Exception(json_encode($sDate) . " is not a valid date string.");
      };
      return new cDate((int)$asMatch[1], (int)$asMatch[2], (int)$asMatch[3]);
    }
    public static function foNow() {
      return cDate::foFromPHPDateTime(new DateTime());
    }
    public static function foNowUTC() {
      return cDate::foFromPHPDateTime(new DateTime("now", new DateTimeZone('UTC')));
    }
    # methods
    public function foClone() {
      $cClass = get_class($this);
      return new $cClass($this->uYear, $this->uMonth, $this->uDay);
    }
    
    public function fSet($uYear, $uMonth, $uDay) {
      if (!fbIsValidYear($uYear)) throw new Exception("Invalid year " . json_encode($uYear) . ".");
      if (!fbIsValidMonth($uMonth)) throw new Exception("Invalid month " . json_encode($uMonth) . ".");
      if (!fbIsValidDay($uDay)) throw new Exception("Invalid day " . json_encode($uDay) . ".");
      if (!fbIsValidDate($uYear, $uMonth, $uDay)) throw new Exception("Invalid date " . fsGetDateString($uYear, $uMonth, $uDay) . ".");
      $this->__uYear = $uYear;
      $this->__uMonth = $uMonth;
      $this->__uDay = $uDay;
    }
    
    public function foGetEndDateForDuration($oDateDuration) {
      // Native functions exist to do this; reuse them.
      $oEndPHPDateTime = $this->foToPHPDateTime();
      $oEndPHPDateTime->modify(
        (string)$oDateDuration->iYears . " year " .
        (string)$oDateDuration->iMonths . " month " .
        (string)$oDateDuration->iDays . " day"
      );
      $oEndDate = cDate::foFromPHPDateTime($oEndPHPDateTime);
      return $oEndDate;
    }
    public function foStartDateForDuration($oDuration) {
      $oStartPHPDateTime = $this->foToPHPDateTime();
      $oStartPHPDateTime->modify(
        (string)(-$oDateDuration->iYears) . " years " .
        (string)(-$oDateDuration->iMonths) . " months " .
        (string)(-$oDateDuration->iDays) . " days"
      );
      return cDate::foFromPHPDateTime($oStartPHPDateTime);
    }
    public function foGetDurationForEndDate($oEndDate) {
      $oStartPHPDateTime = $this->foToPHPDateTime();
      $oEndPHPDateTime = $oEndDate->foToPHPDateTime();
      $oPHPDateInterval = $oStartPHPDateTime->diff($oEndPHPDateTime);
      require_once("cDateDuration.php");
      return cDateDuration::foFromPHPDateInterval($oPHPDateInterval);
    }
    
    // This object has valueOf(), which returns the number of milliseconds since the epoch, so you can also
    // use ($this->valueOf() < $oDate->valueOf(), $this->valueOf() == $oDate->valueOf(), and $this->valueOf() > $oDate->valueOf())
    public function fbIsBefore($oDate) {
      if ($this->__uYear < $oDate->uYear) return True;
      if ($this->__uYear > $oDate->uYear) return False;
      if ($this->__uMonth < $oDate->uMonth) return True;
      if ($this->__uMonth > $oDate->uMonth) return False;
      if ($this->__uDay < $oDate->uDay) return True;
      //if ($this->__uDay > $oDate->uDay) return False;
      return False;
    }
    public function fbIsEqualTo($oDate) {
      return $this->__uYear == $oDate->uYear && $this->__uMonth == $oDate->uMonth && $this->__uDay == $oDate->uDay;
    }
    public function fbIsAfter($oDate) {
      if ($this->__uYear > $oDate->uYear) return True;
      if ($this->__uYear < $oDate->uYear) return False;
      if ($this->__uMonth > $oDate->uMonth) return True;
      if ($this->__uMonth < $oDate->uMonth) return False;
      if ($this->__uDay > $oDate->uDay) return True;
      //if ($this->__uDay < $oDate->uDay) return False;
      return False;
    }
    
    public function fbIsInThePast() {
      return $this->fbIsBefore($this->foNow());
    }
    public function fbIsInThePastUTC() {
      return $this->fbIsBefore($this->foNowUTC());
    }
    public function fbIsToday() {
      return $this->fbIsEqualTo($this->foNow());
    }
    public function fbIsTodayUTC() {
      return $this->fbIsEqualTo($this->foNowUTC());
    }
    public function fbIsInTheFuture() {
      return $this->fbIsAfter($this->foNow());
    }
    public function fbIsInTheFutureUTC() {
      return $this->fbIsAfter($this->foNowUTC());
    }
    
    public function fsToHumanReadableString() {
      // Month <day>th, <year>
      return (
        cDate_asMonths[$this->uMonth - 1]
        . " " . (string)$this->uDay . cDate_asOrdinalPostfixes[$this->uDay % 10]
        . ", " . (string)$this->uYear
      );
    }
    public function foToPHPDateTime() {
      return new DateTime($this->fsToString());
    }
    public function foToPHPDateTimeUTC() {
      return new DateTime($this->fsToString() + "T0:0Z");
    }
    public function fsToMYSQL() {
      return $this->fsToString();
    }
    public function fxToJSON() {
      return $this->fsToString();
    }
    public function jsonSerialize() {
      return $this->fsToString();
    }
    public function fsToString() {
      return (
        str_pad($this->uYear, 4, "0", STR_PAD_LEFT)
        . "-" . str_pad($this->uMonth, 2, "0", STR_PAD_LEFT)
        . "-" . str_pad($this->uDay, 2, "0", STR_PAD_LEFT)
      );
    }
    public function __toString() {
      return $this->fsToString();
    }
  };
?>