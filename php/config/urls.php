<?php
/**
 * Edit only this file when there's a need to change url paths
 *
 * @author: Humberto Moreira <humberto.mn@gmail.com>
 */


// Base URL
define( "URL_LOCAL", "http://127.0.0.1" );
define( "URL_REMOTE", "http://topmusic.humbertomn.com" );
define( "URL_BASE", MODE == 'local' ? URL_LOCAL : URL_REMOTE );

// URLs settings
$URLS = array(

    '/' => array(
        'name' => 'home', 'controller' => 'ArtistController', 'method' => 'get_listing'
    ),
    '/artist/details/([0-9]*)/' => array(
        'name' => 'artist_details', 'controller' => 'ArtistController', 'method' => 'get_details'
    ),

);