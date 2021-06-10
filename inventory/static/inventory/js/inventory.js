/*
JavaScript file supporting a Barcode Scanning Inventory Process that Pulls Data from Alma API.

Author: Terry Brady, Georgetown University Libraries

Dependencies
  1. JQuery UI Dialog:https://jqueryui.com/dialog/
  2. A web service that returns data from the Alma API based on a Barcode: https://github.com/Georgetown-University-Libraries/BarcodeInventory
  3. A Google Apps Web Service that converts CSV data into a Google Sheet: https://github.com/Georgetown-University-Libraries/PlainTextCSV_GoogleAppsScript

Credits
  This code uses a LC Call Number Sort module developed by Ray Voelker from the University of Dayton Library
  https://github.com/rayvoelker/js-loc-callnumbers
*/

/*
 * Evaluate the call number sort of an item based on the previous row that had been added to this table.
 * A CSS class will be assigned to the call number based on a comparison with the prior row.
 *
 * Params
 *   tr - the table row to be evaluated
 *
 * CSS Classes
 *   .lcfirst - no prior element exists in the table
 *   .lcequal - sorted call number matches the prior row
 *   .lcprev  - sorted call number precedes prior row (error condition)
 *   .lcnext  - sorted call number follows prior row (expected condition)
 */

document.addEventListener("DOMContentLoaded", () => {

    function setLcSortStat(call_number, prev) {
        
        var lcsorter = new locCallClass();
        var normlc = "";
        try {
          normlc = lcsorter.returnNormLcCall(call_number);
        } catch(e) {
            
        }

        try {
            prev = lcsorter.returnNormLcCall(prev);
        } catch(e) {

        }
      
         //TODO: We will find another way to read a file where we will have access to previous num
        if (prev == null || prev == "") {
        
          document.querySelector("#results").innerHTML = "lcfirst";
        } else if (normlc == prev) {
          
          document.querySelector("#results").innerHTML = "lcequal";
        } else if (normlc > prev) {
            document.querySelector("#results").innerHTML = "lcnext";
            
        } else {
            document.querySelector("#results").innerHTML = "lcprev";
          
        }
    }


    document.addEventListener("submit", (event) => {
        event.preventDefault();

        var call_number = document.querySelector("#current").value;
        var prev = document.querySelector("#prev").value;

        setLcSortStat(call_number, prev);
    });
});



