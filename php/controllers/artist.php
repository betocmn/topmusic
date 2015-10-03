<?php
/**
 * Artist controller - Here we will be able to list and display
 * details of musicians, accordingly to the user's request.
 *
 * This class will basically demand data from the model class.
 *
 * @author Humberto Moreira <humberto.mn@gmail.com>
 * @package controllers
 * @access public
 */
require_once( "models/artist.php" );

class ArtistController {

    /**
     * Lists all artists based on a search per country
     *
     * @return String
     */
    public function getListing() {

        // If it's an ajax search
        $json_content = file_get_contents( 'php://input' );
        if ( $json_content ){

            // Gets JSON request to read country name typed
            $data = json_decode( $json_content );
            $country = $data->country;
            $page = $data->page;
            $response = array();

            // Performs search
            $artist = new Artist();
            $artists = $artist->search( $country, $page );

            // Returns JSON for AngularJS
            print json_encode( $artists );
            exit();

        }

        // If it's a GET request, just displays the HTML
        $template = 'views/artist/listing.html';
        print file_get_contents( $template );

    }

    /**
     * Gets details from the referenced artist
     *
     * @param String[Required] $id
     * @return String
     */
    public function getDetails( $id ) {

        // If it's an ajax search
        $json_content = file_get_contents( 'php://input' );
        if ( $json_content ){

            // Gets JSON request to read country name typed
            $data = json_decode( $json_content );
            $id = $data->id;
            $response = array();

            // Gets details from artist
            $artist = new Artist();
            $artist_info = $artist->getById( $id );
            $response['name'] = $artist_info['name'];
            $response['img'] = $artist_info['img'];

            // Gets top tracks
            $response['tracks'] = $artist->getTopTracks( $id );

            // Returns JSON for AngularJS
            print json_encode( $response );
            exit();
        }

        // If it's a GET request, just displays the HTML
        $template = 'views/artist/details.html';
        $html = file_get_contents( $template );
        $html = str_replace( '$id', $id, $html );
        print $html;

    }

}