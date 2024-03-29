<?php
  // If all is well, this should work in PHP without the calendar module.
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
    "st", "nd", "rd", "th", "th", "th", "th", "th", "th", "th", # 1-10
    "th", "th", "th", "th", "th", "th", "th", "th", "th", "th", # 11-20
    "st", "nd", "rd", "th", "th", "th", "th", "th", "th", "th", # 21-30
    "st"                                                        # 31
  ];
  function fbIsValidYear($xYear): bool {
    return is_int($xYear);
  };
  function fbIsValidMonth($xMonth): bool {
    return is_int($xMonth) && $xMonth >= 1 && $xMonth <= 12;
  };
  function fbIsValidDay($xDay): bool {
    return is_int($xDay) && $xDay >= 1 && $xDay <= 31;
  };
  function fbIsValidDate($uYear, $uMonth, $uDay): bool {
    return $uDay <= fuGetLastDayInMonth0Based($uYear, $uMonth - 1);
  };
  function fsGetDataString($uYear, $uMonth, $uDay): string {
    return (
      str_pad($uYear, 4, "0", STR_PAD_LEFT)
      . "-" . str_pad($uMonth, 2, "0", STR_PAD_LEFT)
      . "-" . str_pad($uDay, 2, "0", STR_PAD_LEFT)
    );
  };
  
  function fuGetLastDayInMonth0Based($uYear, $uMonth0Based): int {
    $bIsLeapYear = $uYear % 4 == 0 && ($uYear % 100 != 0 || $uYear % 400 == 0);
    return $uMonth0Based == 1 ? ($bIsLeapYear ? 29 : 28) : (($uMonth0Based) % 7 % 2 ? 30 : 31); 
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
        if (!fbIsValidDate($xValue, $this->__uMonth, $this->__uDay))
            throw new Exception("Invalid year in date " . fsGetDataString($xValue, $this->__uMonth, $this->__uDay) . ".");
        $this->__uYear = $xValue;
      } else if ($sPropertyName == "uMonth") {
        if (!fbIsValidMonth($xValue)) throw new Exception("Invalid month " . json_encode($xValue) . ".");
        if (!fbIsValidDate($this->__uYear, $xValue, $this->__uDay))
            throw new Exception("Invalid month in date " . fsGetDataString($this->__uYear, $xValue, $this->__uDay) . ".");
        $this->__uMonth = $xValue;
      } else if ($sPropertyName == "uDay") {
        if (!fbIsValidDay($xValue)) throw new Exception("Invalid day " . json_encode($xValue) . ".");
        if (!fbIsValidDate($this->__uYear, $this->__uMonth, $xValue))
            throw new Exception("Invalid day in date " . fsGetDataString($this->__uYear, $this->__uMonth, $xValue) . ".");
        $this->__uDay = $xValue;
      };
    }
    # static methods
    public static function fo0FromPHPDateTime($oDateTime) {
      return is_null($oDateTime) ? null : cDate::foFromPHPDateTime($oDateTime);
    }
    public static function foFromPHPDateTime($oDateTime): cDate {
      return new cDate((int)$oDateTime->format("Y"), (int)$oDateTime->format("m"), (int)$oDateTime->format("d"));
    }
    
    public static function fo0FromJSON($sDate) {
      return is_null($sDate) ? null : cDate::foFromJSON($sDate);
    }
    public static function foFromJSON($sDate): cDate {
      // JSON encoding uses the "string value" of cDate.
      return cDate::foFromString($sDate);
    }
    
    public static function fo0FromMySQL($sDate) {
      return is_null($sDate) ? null : cDate::foFromMySQL($sDate);
    }
    public static function foFromMySQL($sDate): cDate {
      // MySQL encoding uses the "string value" of cDate.
      return cDate::foFromString($sDate);
    }
    public static function fo0FromMySQLDateTime($sDateTime) {
      return is_null($sDateTime) ? null : cDate::foFromMySQLDateTime($sDateTime);
    }
    public static function foFromMySQLDateTime($sDateTime): cDate {
      // MySQL format is "YYYY-MM-DD hh:mm:ss", so we can just split it at the space and use the first part:
      return cDate::foFromString(explode(" ", $sDateTime)[0]);
    }
    
    public static function fbIsValidDateString($sDate): bool {
      return is_string($sDate) && preg_match(cDate_srDate, $sDate, $asMatch);
    }
    public static function fo0FromString($sDate): cDate {
      return is_null($sDate) ? null : cDate::foFromString($sDate);
    }
    public static function foFromString($sDate): cDate {
      if (!is_string($sDate) || !preg_match(cDate_srDate, $sDate, $asMatch)) {
        throw new Exception(json_encode($sDate) . " is not a valid date string.");
      };
      return new cDate((int)$asMatch[1], (int)$asMatch[2], (int)$asMatch[3]);
    }
    public static function foNow(): cDate {
      return cDate::foFromPHPDateTime(new DateTime());
    }
    public static function foNowUTC(): cDate {
      return cDate::foFromPHPDateTime(new DateTime("now", new DateTimeZone('UTC')));
    }
    # methods
    public function foClone() {
      $cClass = get_class($this);
      return new $cClass($this->__uYear, $this->__uMonth, $this->__uDay);
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
    
    public function foGetEndDateForDuration($oDuration): cDate {
      // Native functions exist to do this but they believe 2001-01-30 + 1m == 2001-03-02, which I personally
      // do not think is correct, so we do it manually.
      // Note that this code ignores the time (if any) in oDuration
      // Add the year and month:
      $uNewYear = $this->__uYear + $oDuration->iYears;
      $uNewMonth0Based = $this->__uMonth - 1 + $oDuration->iMonths;
      # If uNewMonth < 0 or > 11, convert the excess to years and add it.
      $uNewYear += (int)floor($uNewMonth0Based / 12);
      $uNewMonth0Based = (($uNewMonth0Based % 12) + ($uNewMonth0Based < 0 ? 12 : 0)) % 12;
      # If we added months and ended up in another month in which the current day does not exist (e.g. Feb 31st)
      # reduce the day (i.e. Feb 28th/29th)
      $uLastDayInNewMonth = fuGetLastDayInMonth0Based($uNewYear, $uNewMonth0Based);
      $uNewDay = $this->uDay <= $uLastDayInNewMonth ? $this->__uDay : $uLastDayInNewMonth;
      # Add the days by creating the Python datetime.date equivalent and adding the days using datetime.timedelta, then
      # converting back to cDate. This allows us to reuse the Python API for tracking the number of days in each month.
      $oEndPHPDateTime = (new cDate($uNewYear, $uNewMonth0Based + 1, $uNewDay))->foToPHPDateTime();
      $oEndPHPDateTime->modify((string)$oDuration->iDays . " day");
      $oEndDate = cDate::foFromPHPDateTime($oEndPHPDateTime);
      return $oEndDate;
      #############
      $oEndPHPDateTime = $this->foToPHPDateTime();
      $oEndPHPDateTime->modify(
        (string)$oDuration->iYears . " year " .
        (string)$oDuration->iMonths . " month " .
        (string)$oDuration->iDays . " day"
      );
      $oEndDate = cDate::foFromPHPDateTime($oEndPHPDateTime);
      return $oEndDate;
    }
    public function foStartDateForDuration($oDuration): cDate {
      $oStartPHPDateTime = $this->foToPHPDateTime();
      $oStartPHPDateTime->modify(
        (string)(-$oDuration->iYears) . " years " .
        (string)(-$oDuration->iMonths) . " months " .
        (string)(-$oDuration->iDays) . " days"
      );
      return cDate::foFromPHPDateTime($oStartPHPDateTime);
    }
    public function foGetDurationForEndDate($oEndDate): cDateDuration {
      $oStartPHPDateTime = $this->foToPHPDateTime();
      $oEndPHPDateTime = $oEndDate->foToPHPDateTime();
      $oPHPDateInterval = $oStartPHPDateTime->diff($oEndPHPDateTime);
      require_once("cDateDuration.php");
      return cDateDuration::foFromPHPDateInterval($oPHPDateInterval);
    }
    
    // This object has valueOf(), which returns the number of milliseconds since the epoch, so you can also
    // use ($this->valueOf() < $oDate->valueOf(), $this->valueOf() == $oDate->valueOf(), and $this->valueOf() > $oDate->valueOf())
    public function fbIsBefore($oDate): bool {
      if ($this->__uYear < $oDate->uYear) return True;
      if ($this->__uYear > $oDate->uYear) return False;
      if ($this->__uMonth < $oDate->uMonth) return True;
      if ($this->__uMonth > $oDate->uMonth) return False;
      if ($this->__uDay < $oDate->uDay) return True;
      //if ($this->__uDay > $oDate->uDay) return False;
      return False;
    }
    public function fbIsEqualTo($oDate): bool {
      return $this->__uYear == $oDate->uYear && $this->__uMonth == $oDate->uMonth && $this->__uDay == $oDate->uDay;
    }
    public function fbIsAfter($oDate): bool {
      if ($this->__uYear > $oDate->uYear) return True;
      if ($this->__uYear < $oDate->uYear) return False;
      if ($this->__uMonth > $oDate->uMonth) return True;
      if ($this->__uMonth < $oDate->uMonth) return False;
      if ($this->__uDay > $oDate->uDay) return True;
      //if ($this->__uDay < $oDate->uDay) return False;
      return False;
    }
    
    public function fbIsInThePast(): bool {
      return $this->fbIsBefore($this->foNow());
    }
    public function fbIsInThePastUTC(): bool {
      return $this->fbIsBefore($this->foNowUTC());
    }
    public function fbIsToday(): bool {
      return $this->fbIsEqualTo($this->foNow());
    }
    public function fbIsTodayUTC(): bool {
      return $this->fbIsEqualTo($this->foNowUTC());
    }
    public function fbIsInTheFuture(): bool {
      return $this->fbIsAfter($this->foNow());
    }
    public function fbIsInTheFutureUTC(): bool {
      return $this->fbIsAfter($this->foNowUTC());
    }
    
    public function fsToHumanReadableString(): string {
      // Month <day>th, <year>
      return (
        cDate_asMonths[$this->__uMonth - 1]
        . " " . (string)$this->__uDay . cDate_asOrdinalPostfixes[$this->__uDay]
        . ", " . (string)$this->__uYear
      );
    }
    public function foToPHPDateTime(): DateTime {
      return new DateTime($this->fsToString());
    }
    public function foToPHPDateTimeUTC(): DateTime {
      return new DateTime($this->fsToString() + "T0:0Z");
    }
    public function fxToJSON(): string {
      // JSON encoding uses the "string value" of cDate.
      return $this->fsToString();
    }
    public function fsToMySQL(): string {
      // MySQL encoding uses the "string value" of cDate.
      return $this->fsToString();
    }
    public function jsonSerialize(): string {
      return $this->fsToString();
    }
    public function fsToString(): string {
      return (
        str_pad($this->__uYear, 4, "0", STR_PAD_LEFT)
        . "-" . str_pad($this->__uMonth, 2, "0", STR_PAD_LEFT)
        . "-" . str_pad($this->__uDay, 2, "0", STR_PAD_LEFT)
      );
    }
    public function __toString(): string {
      return $this->fsToString();
    }
  };
?>