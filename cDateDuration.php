<?php
  namespace mDateTime;
  use \DateInterval;
  use \Exception;
  use \JsonSerializable;
  // PHP internal DateInterval
  CONST cDateDuration_srDateDuration = (
    "/^\\s*" .
    "(?:([+-]?\\d+)\\s*y(?:ears?)?\\s*,?\\s*)?" .
    "(?:([+-]?\\d+)\\s*m(?:onths?)?\\s*,?\\s*)?" .
    "(?:([+-]?\\d+)\\s*d(?:ays?)?)?" .
    "\\s*$/"
  );
  function fbIsValidInteger($xValue) {
    return is_int($xValue);
  };
  class cDateDuration implements JsonSerializable {
    private $__iYears = null;
    private $__iMonths = null;
    private $__iDays = null;
    
    # constructor
    function __construct($iYears, $iMonths, $iDays) {
      if (!fbIsValidInteger($iYears)) throw new Exception("Invalid number of years " . json_encode($iYears) . ".");
      if (!fbIsValidInteger($iMonths)) throw new Exception("Invalid number of months " . json_encode($iMonths) . ".");
      if (!fbIsValidInteger($iDays)) throw new Exception("Invalid number of days " . json_encode($iDays) . ".");
      $this->__iYears = $iYears;
      $this->__iMonths = $iMonths;
      $this->__iDays = $iDays;
    }
    # properties
    function __get($sPropertyName) {
      if ($sPropertyName == "iYears") {
        return $this->__iYears;
      } else if ($sPropertyName == "iMonths") {
        return $this->__iMonths;
      } else if ($sPropertyName == "iDays") {
        return $this->__iDays;
      };
    }
    function __set($sPropertyName, $xValue) {
      if ($sPropertyName == "iYears") {
        if (!fbIsValidInteger($xValue)) throw new Exception("Invalid number of years " . json_encode($xValue) . ".");
        $this->__iYears = $xValue;
      } else if ($sPropertyName == "iMonths") {
        if (!fbIsValidInteger($xValue)) throw new Exception("Invalid number of months " . json_encode($xValue) . ".");
        $this->__iMonths = $xValue;
      } else if ($sPropertyName == "iDays") {
        if (!fbIsValidInteger($xValue)) throw new Exception("Invalid number of days " . json_encode($xValue) . ".");
        $this->__iDays = $xValue;
      };
    }
    // static methods
    public static function fbIsValidDateDurationString($sDateDuration) {
      return (
        is_string($sDateDuration)
        && preg_match(cDateDuration_srDateDuration, $sDateDuration, $asMatch)
        && count($asMatch[1]) > 1
      );
    }
    
    public static function fo0FromPHPDateInterval($oDateInterval) {
      return is_null($oDateInterval) ? null : cDateDuration::foFromPHPDateInterval($oDateInterval);
    }
    public static function foFromPHPDateInterval($oDateInterval) {
      return new cDateDuration($oDateInterval->y, $oDateInterval->m, $oDateInterval->d);
    }
    
    public static function fo0FromJSON($sDateDuration) {
      return is_null($sDateDuration) ? null : cDate::foFromJSON($sDateDuration);
    }
    public static function foFromJSON($sDateDuration) {
      // JSON encoding uses the "string value" of cDateDuration.
      return cDateDuration::foFromString($sDateDuration);
    }
    
    public static function fo0FromMySQL($sDateDuration) {
      return is_null($sDateDuration) ? null : cDateDuration::foFromMySQL($sDateDuration);
    }
    public static function foFromMySQL($sDateDuration) {
      // MySQL encoding uses the "string value" of cDateDuration.
      return cDateDuration::foFromString($sDateDuration);
    }
    
    public static function fo0FromString($sDateDuration) {
      return is_null($sDateDuration) ? null : cDateDuration::foFromString($sDateDuration);
    }
    public static function foFromString($sDateDuration) {
      if (
        !is_string($sDateDuration)
        || !preg_match(cDateDuration_srDateDuration, $sDateDuration, $asMatch)
        || count($asMatch) == 1
      ) {
        throw new Exception(json_encode($sDateDuration) . " is not a valid date duration string.");
      };
      return new cDateDuration(
        (count($asMatch) < 2 || is_null($asMatch[1])) ? 0 : (int)$asMatch[1],
        (count($asMatch) < 3 || is_null($asMatch[2])) ? 0 : (int)$asMatch[2],
        (count($asMatch) < 4 || is_null($asMatch[3])) ? 0 : (int)$asMatch[3]
      );
    }
    ##
    // methods
    public function foClone() {
      $cClass = get_class($this);
      return new $cClass($this->__iYears, $this->__iMonths, $this->__iDays);
    }
    
    public function fSet($iYears, $iMonths, $iDays) {
      if (is_null($iYears)) $iYears = $this->__iYears;
      else if (!fbIsValidInteger($iYears)) throw new Exception("Invalid number of years " . json_encode($iYears) . ".");
      if (is_null($iMonths)) $iMonths = $this->__iMonths;
      else if (!fbIsValidInteger($iMonths)) throw new Exception("Invalid number of months " . json_encode($iMonths) . ".");
      if (is_null($iDays)) $iDays = $this->__iDays;
      else if (!fbIsValidInteger($iDays)) throw new Exception("Invalid number of days " . json_encode($iDays) . ".");
      $this->__iYears = $iYears;
      $this->__iMonths = $iMonths;
      $this->__iDays = $iDays;
    }
    
    public function foNormalizedForDate($oDate) {
      // Adjust duration to make all numbers either all positive or negative and minimze days, months and years.
      // e.g. "+2y-12m+32d" for "2000-01-01" => "+1y+1m+1d"
      return $oDate->foGetDurationForEndDate($oDate->foGetEndDateForDuration($this));
    }
    
    public function foAdd($oOtherDateDuration) {
      $this->fSet($this->__iYears + $oOtherDuration->iYears, $this->__iMonths + $oOtherDuration->iMonths, $this->__iDays + $oOtherDuration->iDays);
      return $this;
    }
    public function foSubtract($oOtherDuration) {
      $this->fSet($this->__iYears - $oOtherDuration->iYears, $this->__iMonths - $oOtherDuration->iMonths, $this->__iDays - $oOtherDuration->iDays);
      return $this;
    }
    public function foPlus($oOtherDuration) {
      return $this->foClone().foAdd($oOtherDuration);
    }
    public function foMinus($oOtherDuration) {
      return $this->foClone().foSubtract($oOtherDuration);
    }
    
    public function fbIsZero() {
      return $this->__iYears == 0 && $this->__iMonths == 0 && $this->__iDays == 0;
    }
    public function fbIsPositive() {
      return $this->__iYears >= 0 && $this->__iMonths >= 0 && $this->__iDays >= 0 && !$this->fbIsZero();
    }
    public function fbIsNegative() {
      return $this->__iYears <= 0 && $this->__iMonths <= 0 && $this->__iDays <= 0 && !$this->fbIsZero();
    }
    public function fbIsNormalized() {
      return $this->fbIsZero() || $this->fbIsPositive() || $this->fbIsNegative();
    }
    
    public function fsToHumanReadableString() {
      if ($this->fbIsZero()) return "0 days";
      if (!$this->fbIsNormalized()) throw new Exception("Duration must be normalized before converting to human readable string!");
      // Show positive and negative durations the same.
      $iYears = abs($this->__iYears); $iMonths = abs($this->__iMonths); $iDays = abs($this->__iDays);
      $asComponents = array_filter([
        ($iYears == 1 ? "1 year" : ($iYears ? (string)$iYears . " years" : "")),
        ($iMonths == 1 ? "1 month" : ($iMonths ? (string)$iMonths . " months" : "")),
        ($iDays == 1 ? "1 day" : ($iDays ? (string)$iDays . " days" : "")),
      ]);
      return (
        count($asComponents) == 3
        ? $asComponents[0] . ", " . $asComponents[1] . ", and " . $asComponents[2]
        : implode(" and ", $asComponents)
      );
    }
    
    public function fxToJSON() {
      // JSON encoding uses the "string value" of cDateDuration.
      return $this->fsToString();
    }
    public function fsToMySQL() {
      // MySQL encoding uses the "string value" of cDateDuration.
      return $this->fsToString();
    }
    public function jsonSerialize() {
      return $this->fsToString();
    }
    public function fsToString() {
      if ($this->fbIsZero()) return "0d";
      // months sign is required if months are negative, or months are positive and years are negative.
      $sMonthsSign = ($this->__iMonths < 0 ? "-" : ($this->__iYears < 0 ? "+" : ""));
            // days sign is required if days are negative or days are positive and months are negative or if months are zero and years are negative.
      $sDaysSign = ($this->__iDays < 0 ? "-" : ($this->__iMonths < 0 || ($this->__iMonths == 0 && $this->__iYears < 0) ? "+" : ""));
      return implode("", [
        $this->__iYears ? $this->__iYears . "y" : "",
        $this->__iMonths ? $sMonthsSign . abs($this->__iMonths) . "m" : "",
        $this->__iDays ? $sDaysSign . abs($this->__iDays) . "d" : "",
      ]);
    }
    public function __toString() {
      return $this->fsToString();
    }
  };
?>