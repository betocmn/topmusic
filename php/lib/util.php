<?php
/**
 * Utility functions to be used around the system
 *
 * @author: Humberto Moreira <humberto.mn@gmail.com>
 */


/**
 * Grabs the request URL path and searches in $URLS from
 * our settings/urls.php file.
 *
 * @param Array $urls
 * @return Array
 */
function get_url_data( $urls ){

    $path = $_SERVER['REQUEST_URI'];
    foreach ( $urls as $key => $value ){
        $regex = "#^{$key}$#";
        if ( preg_match( $regex, $path ) ){
            return $value;
        }
    }
    return array();

}

/**
 * Returns file name of controller class name
 *
 * Class Name: ArtistController
 * File Name should be: artist.php
 *
 * @param String $class_name
 * @return String
 */
function get_controller_file_name( $class_name ){

    return str_replace( 'controller', '', strtolower( $class_name ) ) . '.php';

}