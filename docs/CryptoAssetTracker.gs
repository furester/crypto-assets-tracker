// This program is free software; you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation; either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program; if not, write to the Free Software
// Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
//
// author: https://github.com/furester
// source: https://github.com/furester/crypto-assets-tracker

function onOpen() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet();
  var entries = [{ name : "Update Rate", functionName : "Balance" }];
  //sheet.addMenu("Crypto Asset Tracker", entries);
};

function CryptoAssetTracker(symbol) {
  var vs_currencies = "usd";

  var getLiveData = function(symbol) {
    // https://mixedanalytics.com/knowledge-base/import-coingecko-data-to-google-sheets/
    var f_symbol = symbol || "";

    var url = "https://api.coingecko.com/api/v3/simple/price/?ids=" + f_symbol;
        url += "&vs_currencies=" + vs_currencies;
    var fetchOptions = {
      muteHttpExceptions: true, 
      validateHttpsCertificates: true,
      contentType: 'application/json', 
      headers: {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0'}
    };
    
    // Send request
    var response = UrlFetchApp.fetch(url, fetchOptions)
    if (response.getContentText() == {}) {
      throw new Error("Symbol non riconosciuto.");
    }
    if (response.getContentText() == "error code: 1015") {
      throw new Error("Troppe chiamate, riprova più tardi.");
    }

    var data = [];
    try {
      var data = JSON.parse(response.getContentText());
    }
    catch (e) {
      throw new Error("Impossibile leggere la risposta." + e);
    }

    return response.getContentText();
  }

  var getCachedData = function(symbol) {
    var data = {};
    var cache = CacheService.getUserCache();

    var CACHE_KEY = "CAT__"+ symbol.toLowerCase() + "_usd";
    var cached = cache.get(CACHE_KEY);

    return cached;
  }

  var putCachedData = function(symbol, data, caching_time) {
    var cache = CacheService.getUserCache();

    var CACHE_KEY = "CAT__"+ symbol.toLowerCase() + "_usd";
    cache.put(CACHE_KEY, data, caching_time || 1500) // cache for 25 minutes
  }

  var delCachedData = function(symbol) {
    var cache = CacheService.getUserCache();

    var CACHE_KEY = "CAT__"+ symbol.toLowerCase() + "_usd";
    cache.remove(CACHE_KEY)
  }

  var data = {};
  var symbol = symbol || "";
  if (symbol == "") {
    throw new Error("Necessario specificare il simbolo della valuta. https://api.coingecko.com/api/v3/coins/list")
  }

  // First check if we have a cached version
  var cached = getCachedData(symbol);
  if (cached && cached != null && cached.length > 2) {
    console.log("using cache", cached);
    data = JSON.parse(cached)
  }
  else {
    console.log("get live data");
    var raw_data = getLiveData(symbol);
    // If everything went fine, cache the raw data returned
    putCachedData(symbol, raw_data);
    
    data = JSON.parse(raw_data);
  }

  if (data[symbol] == undefined) {
    delCachedData(symbol);
    return "-";
  }
  var out = data[symbol][vs_currencies];
  return parseFloat(out);
}
