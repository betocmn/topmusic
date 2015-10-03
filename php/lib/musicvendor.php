<?php 
/**
 * Interface for all 3rd party Music classes
 *
 * @author Humberto Moreira <humberto.mn@gmail.com>
 * @package lib
 * @access public
 */


interface MusicVendor {

	public function getTopArtists( $country, $page = 1, $limit = 50 );
	public function getArtistDetails( $id );
	public function getTopTracks( $id );

}