'use strict';

import fetch from "node-fetch";

data_json = fetch("https://download.data.grandlyon.com/wfs/rdata?SERVICE=WFS&VERSION=1.1.0&outputformat=GEOJSON&request=GetFeature&typename=jcd_jcdecaux.jcdvelov&SRSNAME=urn%3Aogc%3Adef%3Acrs%3AEPSG%3A%3A4171&fbclid=IwAR1qE58gRLmkdiAe7PVO-0Xd_LmECLwhsUWEle8hIA9Iw2HqIeuvatJ0F5E");

console.log(data_json);