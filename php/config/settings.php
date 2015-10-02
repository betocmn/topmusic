<?php
/**
 * General APP Settings
 *
 * @author: Humberto Moreira <humberto.mn@gmail.com>
 */


// Defines environment
define( "MODE", "local" ); // local or remote

// 3rd party music API settings
define( "API_VENDOR", "lastfm" ); // lastfm, spotify, etc
define( "API_KEY", "57ee3318536b23ee81d6b27e36997cde" );
define( "API_URL", "http://ws.audioscrobbler.com/2.0/" );

// Pagination settings
define( "PAGINATION_ITEMS_PER_PAGE", 5 );
define( "PAGINATION_PAGES_DISPLAY", 10 );