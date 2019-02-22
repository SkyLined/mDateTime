<?php
  error_reporting(E_ALL); // Treat all notices, warnings and errors as exceptions
  require_once("cDate.php");
  require_once("cDateDuration.php");
  use mDateTime\cDate;
  use mDateTime\cDateDuration;
  function fMustBeEqual($xValue1, $xValue2, $sErrorMessage) {
    if (!(
      ($xValue1 instanceof cDate || $xValue1 instanceof cDateDuration)
      && ($xValue2 instanceof cDate || $xValue2 instanceof cDateDuration)
      && (string)$xValue1 == (string)$xValue2
    )) {
      error_log("xValue1 is " . (($xValue1 instanceof cDate) ? "" : "not ") . "a date.");
      error_log("xValue2 is " . (($xValue2 instanceof cDate) ? "" : "not ") . "a date.");
      error_log("xValue1 " . (((string)$xValue1 == (string)$xValue2) ? "==" : "!=") . " xValue2.");
      throw new Exception($sErrorMessage);
    };
  };
  function fDatePlustDurationMustEqual($sStartDate, $sDuration, $sEndDate, $sNormalizedDuration = NULL) {
    $oStartDate = cDate::foFromString($sStartDate);
    $oDuration = cDateDuration::foFromString($sDuration);
    $oEndDate = cDate::foFromString($sEndDate);
    $oCalculatedEndDate = $oStartDate->foGetEndDateForDuration($oDuration);
    $oCalculatedDuration = $oStartDate->foGetDurationForEndDate($oEndDate);
    $oNormalizedDuration = $oDuration->foNormalizedForDate($oStartDate);
    fMustBeEqual(
      $oEndDate,
      $oCalculatedEndDate,
      (string)$sStartDate . " + " . $sDuration . " == " . (string)$oCalculatedEndDate . " (NOT " . $sEndDate . ")"
    );
    fMustBeEqual(
      $oCalculatedDuration,
      $oNormalizedDuration,
      (string)$sStartDate . " -> " . $sEndDate . " == " . (string)$oCalculatedDuration . " (NOT " . (string)$oNormalizedDuration . ")"
    );
    if ($sNormalizedDuration && $sNormalizedDuration != (string)$oNormalizedDuration) {
      throw new Exception(
        (string)$sStartDate . " -> " . $sEndDate . " == " . (string)$oNormalizedDuration . " (NOT " . $sNormalizedDuration . ")"
      );
    };
  };
  function fNormalizedDurationForDateMustEqual($sDuration, $sDate, $sNormalizedDuration) {
    $oNormalizedDuration = cDateDuration::foFromString($sDuration)->foNormalizedForDate(cDate::foFromString($sDate));
    fMustBeEqual(
      $oNormalizedDuration,
      cDateDuration::foFromString($sNormalizedDuration),
      $sDuration . " normalized for " . $sDate . " == " . (string)$oNormalizedDuration . " (NOT " . $sNormalizedDuration . ")"
    );
  };
  fDatePlustDurationMustEqual("2000-01-01", "+1y", "2001-01-01");
  fDatePlustDurationMustEqual("2000-01-01", "+12m", "2001-01-01");
  fDatePlustDurationMustEqual("2000-01-01", "+366d", "2001-01-01"); // 2000 is a leap year.
  fDatePlustDurationMustEqual("2001-01-01", "+1y", "2002-01-01");
  fDatePlustDurationMustEqual("2001-01-01", "+12m", "2002-01-01");
  fDatePlustDurationMustEqual("2001-01-01", "+365d", "2002-01-01"); // 2001 is not a leap year.
  
  fDatePlustDurationMustEqual("2000-02-01", "+28d", "2000-02-29"); // 2000 is a leap year.
  fDatePlustDurationMustEqual("2000-02-01", "+29d", "2000-03-01"); // 2000 is a leap year.
  fDatePlustDurationMustEqual("2001-02-01", "+28d", "2001-03-01"); // 2001 is not a leap year.
  fDatePlustDurationMustEqual("2000-01-01", "+1y+1m+28d", "2001-03-01"); // 2001 is not a leap year; days are applied last.
  
  fDatePlustDurationMustEqual("2000-01-01", "+1m", "2000-02-01");
  fDatePlustDurationMustEqual("2000-01-01", "+31d", "2000-02-01");
  
  fDatePlustDurationMustEqual("2000-01-01", "+1d", "2000-01-02");
  
  fDatePlustDurationMustEqual("2000-01-01", "+1y1m1d", "2001-02-02");
  
  fNormalizedDurationForDateMustEqual("1y1m1d", "2000-01-01", "1y1m1d");
  fNormalizedDurationForDateMustEqual("+1y-1m+31d", "2000-01-01", "1y");
  fNormalizedDurationForDateMustEqual("+2 years, -12 months, -366 day", "2000-01-01", "0d");
  
  $oTestDate = new cDate(2000, 2, 28);
  $oFromStringTestDate = cDate::foFromString("2000-02-28");
  $oFromJSONTestDate = cDate::foFromJSON("2000-02-28");
  $oFromMYSQLTestDate = cDate::foFromMYSQL("2000-02-28");
  $oClonedTestDate = $oTestDate->foClone();
  fMustBeEqual($oTestDate, $oFromStringTestDate, "cDate::foFromString(\"2000-02-28\") should not result in " . (string)$oFromStringTestDate);
  fMustBeEqual($oTestDate, $oFromJSONTestDate, "cDate::foFromJSON(\"2000-02-28\") should not result in " . (string)$oFromJSONTestDate);
  fMustBeEqual($oTestDate, $oFromMYSQLTestDate, "cDate::foFromMYSQL(\"2000-02-28\") should not result in " . (string)$oFromMYSQLTestDate);
  fMustBeEqual($oTestDate, $oClonedTestDate, (string)$oTestDate . " should not be cloned as " . (string)$oClonedTestDate);
  
  // Check day/month is adjusted if needed when months are added to potentially overflow the day.
  fDatePlustDurationMustEqual("2000-01-30", "1m", "2000-02-29", "30d");
  fDatePlustDurationMustEqual("2001-01-30", "1m", "2001-02-28", "29d");
  fDatePlustDurationMustEqual("2001-01-29", "1m", "2001-02-28", "30d");
  fDatePlustDurationMustEqual("2001-01-28", "1m", "2001-02-28", "1m");
  
  $oTestDate->uDay = 29;
  $bHasThrownException = false;
  try {
    $oTestDate->uYear = 2001;
  } catch (Exception $e) {
    $bHasThrownException = true;
  };
  if (!$bHasThrownException) throw new Exception((string)$oTestDate . " should not be possible.");
  $bHasThrownException = false;
  $oTestDate->uDay = 28;
  $oTestDate->uYear = 2001;
  try {
    $oTestDate->uDay = 29;
  } catch (Exception $e) {
    $bHasThrownException = true;
  };
  if (!$bHasThrownException) throw new Exception((string)$oTestDate . " should not be possible.");
  $bHasThrownException = false;
  $oTestDate->uMonth = 1;
  $oTestDate->uDay = 29;
  try {
    $oTestDate->uMonth = 2;
  } catch (Exception $e) {
    $bHasThrownException = true;
  };
  if (!$bHasThrownException) throw new Exception((string)$oTestDate . " should not be possible.");
  
  function fCompareDates($oDate1, $sResults, $oDate2) {
    if ($sResults == "IsBefore") {
      if (!$oDate1->fbIsBefore($oDate2)) throw new Exception((string)$oDate1 . " should be before " . (string)$oDate2 . ".");
    } else {
      if ($oDate1->fbIsBefore($oDate2)) throw new Exception((string)$oDate1 . " should not be before " . (string)$oDate2 . ".");
    };
    if ($sResults == "IsEqualTo") {
      if (!$oDate1->fbIsEqualTo($oDate2)) throw new Exception((string)$oDate1 . " should be equal to " . (string)$oDate2 . ".");
    } else {
      if ($oDate1->fbIsEqualTo($oDate2)) throw new Exception((string)$oDate1 . " should not be equal to " . (string)$oDate2 . ".");
    };
    if ($sResults == "IsAfter") {
      if (!$oDate1->fbIsAfter($oDate2)) throw new Exception((string)$oDate1 . " should be after " . (string)$oDate2 . ".");
    } else {
      if ($oDate1->fbIsAfter($oDate2)) throw new Exception((string)$oDate1 . " should not be after " . (string)$oDate2 . ".");
    };
  };
  $oDate1 = new cDate(2000, 1, 1);
  $oDate2 = new cDate(2000, 1, 2);
  $oDate3 = new cDate(2000, 2, 1);
  $oDate4 = new cDate(2001, 1, 1);
  fCompareDates($oDate1, "IsEqualTo", $oDate1);
  fCompareDates($oDate1, "IsBefore", $oDate2);
  fCompareDates($oDate1, "IsBefore", $oDate3);
  fCompareDates($oDate1, "IsBefore", $oDate4);

  fCompareDates($oDate2, "IsAfter", $oDate1);
  fCompareDates($oDate2, "IsEqualTo", $oDate2);
  fCompareDates($oDate2, "IsBefore", $oDate3);
  fCompareDates($oDate2, "IsBefore", $oDate4);

  fCompareDates($oDate3, "IsAfter", $oDate1);
  fCompareDates($oDate3, "IsAfter", $oDate2);
  fCompareDates($oDate3, "IsEqualTo", $oDate3);
  fCompareDates($oDate3, "IsBefore", $oDate4);

  fCompareDates($oDate4, "IsAfter", $oDate1);
  fCompareDates($oDate4, "IsAfter", $oDate2);
  fCompareDates($oDate4, "IsAfter", $oDate3);
  fCompareDates($oDate4, "IsEqualTo", $oDate4);
  
  $o0MYSQLDate = cDate::fo0FromMYSQLDateTime(null);
  if (!is_null($o0MYSQLDate)) throw new Exception((string)$o0MYSQLDate . " should be null");
  $o0MYSQLDate = cDate::fo0FromMYSQLDateTime("2000-01-01 01:02:03");
  fMustBeEqual($o0MYSQLDate, new cDate(2000, 1, 1), "cData::fo0FromMYSQLDateTime(\"2000-01-01 01:02:03\") should not result in " . (string)$o0MYSQLDate);
  
  echo "All tests successful.";
?>