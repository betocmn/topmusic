<?php 
/**
 * Base Model.
 *
 * All other models should extend this class.
 *
 * It's responsible for creating the connection with 3rd party
 * APIs
 * 
 * @author Humberto Moreira <humberto.mn@gmail.com>
 * @package models
 * @access public
 */
require_once(  "config/settings.php" );
require_once(  "lib/lastfm.php" );
require_once(  "lib/spotify.php" );


abstract class Base {

	/**
	 * Class Attributes
	 *
	 * @var String
	 */
	protected $api = '';

	/**
	 * Constructor.
	 * Instantiates the vendor API specified on settings
	 *
	 * @access public
	 */
	public function __construct( $data = null ){

		if ( API_VENDOR == 'lastfm' ){
			$this->api = new LastFm( API_URL, API_KEY );
		} else if ( API_VENDOR == 'spotify' ){
			$this->api = new Spotify( API_URL, API_KEY );
		}

	}

	/**
	 * Returns the 3rd party music API
	 *
	 * @access public
	 * @return Object
	 */
	public function getApi() {

		return $this->api;

	}

}