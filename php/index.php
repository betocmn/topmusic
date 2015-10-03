<?php
/**
 * All URL requests come to this script which searches for
 * the correct controller and method to handle and return a
 * response
 *
 * @author: Humberto Moreira <humberto.mn@gmail.com>
 */
require_once( "config/settings.php" );
require_once( "lib/util.php" );
require_once( "config/urls.php" );


// Grabs path from url and search on our config/urls or the correct controller/method
$url_info = get_url_data( $URLS );
if ( sizeof( $url_info ) ) {

    require_once ( "controllers/" . get_controller_file_name( $url_info['controller'] ) );
    $method = array( $url_info['controller'], $url_info['method'] );
    if ( is_callable( $method ) ) {
        call_user_func_array( $method, $url_info['params'] );
        exit();
    }

}

// No valid URL was found for this request
echo "Invalid Request";
exit();

