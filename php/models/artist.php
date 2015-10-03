<?php 
/**
 * Artist Model.
 *
 * This class will connect to one of the vendors APIs (lastfm, etc)
 * to get information from musicians around the world.
 * 
 * @author Humberto Moreira <humberto.mn@gmail.com>
 * @package models
 * @access public
 */

require_once( "base.php" );
require_once( "config/settings.php" );

class Artist extends Base {

	/**
     * Name of Artist
     * @var string
     */
	public $name = null;

	/**
	 * URL of image for the the Artist
	 * @var string
	 */
	public $imgUrl = null;


	/**
	 * Constructor.
	 * Calls parent constructor to set correct vendor API
	 * 
	 * @access public
	 */
	public function __construct(){
		parent::__construct();
	}
	
	/**
	 * Get artist's name
	 *
	 * @access public
	 * @return String
	 */
	public function getName(){
        return $this->name;
	}

    /**
     * Set artist's name
     *
     * @param String[Required] $name
     * @access public
     * @return String
     */
    public function setName( $name ){
        $this->name = $name;
    }

    /**
     * Get artist's name
     *
     * @access public
     * @return String
     */
    public function getImgUrl(){
        return $this->imgUrl;
    }

    /**
     * Set artist's name
     *
     * @param String[Required] $name
     * @access public
     * @return String
     */
    public function setImgUrl( $imgUrl ){
        $this->imgUrl = $imgUrl;
    }

    /**
     * Searches for artists
     *
     * @param String[Required] $country_name
     * @param Int[Optional] $page
     * @param Int[Optional] $limit
     * @access public
     * @return Array
     */
    public function search( $countryName, $page = 1, $limit = PAGINATION_ITEMS_PER_PAGE ){

        $api = $this->getApi();
        return $api->getTopArtists( $countryName, $page, $limit );

    }

    /**
     * Gets Artist By ID
     *
     * @param String[Required] $id
     * @access public
     * @return Array
     */
    public function getById( $id ){

        $api = $this->getApi();
        return $api->getArtistDetails( $id );

    }

    /**
     * Gets Top Tracks By Artist ID
     *
     * @param String[Required] $id
     * @access public
     * @return String
     */
    public function getTopTracks( $id ){
        $api = $this->getApi();
        return $api->getTopTracks( $id );

    }


}