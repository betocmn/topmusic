<?php
/**
 * Spotify class to connect with the vendor's API to return their data.
 *
 * @author Humberto Moreira <humberto.mn@gmail.com>
 * @package lib
 * @access public
 */
require_once( "musicvendor.php" );


class Spotify implements MusicVendor {

	/**
	 * API Url
	 * @var string
	 */
	private $url = null;

	/**
	 * API Key
	 * @var string
	 */
	private $key = null;

	/**
	 * Constructor.
	 * Sets class atributes
	 *
	 * @param String[Required] $url
	 * @param String[Required] $key
	 * @access public
	 */
	public function __construct( $url, $key ){
		$this->url = $url;
		$this->key = $key;
	}

	/**
	 * Constructor.
	 * Sets class atributes
	 *
	 * @param Array[Required] $data
	 * @return SimpleXMLElement Object
	 * @access public
	 */
	public function sendRequest( $data ){

		// Builds GET url
		$params =   http_build_query( $data );
		$url    =   "{$this->url}?{$params}";
		$xml    =   file_get_contents( $url );

		// If request Failed
		if ( !$xml ) {
			return false;
		}

		// Returns XML Element
		return new SimpleXMLElement( $xml );

	}

	/**
	 * Returns artists per country name
	 *
	 * @param String[Required] $country
	 * @param Int[Optional] $page
	 * @param Int[Optional] $limit
	 * @access public
	 * @return Array
	 */
	public function getTopArtists( $country, $page = 1, $limit = 50 ){

		//@TODO
	}

	/**
	 * Returns details from an artist ID
	 *
	 * @param String[Required] $id
	 * @access public
	 * @return Array
	 */
	public function getArtistDetails( $id ){

		//@TODO

	}

	/**
	 * Returns top tracks by artist ID
	 *
	 * @param String[Required] $id
	 * @access public
	 * @return Array
	 */
	public function getTopTracks( $id ){

		//@TODO

	}

}