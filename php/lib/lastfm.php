<?php 
/**
 * Last.Fm class to connect with the vendor's API to return their data.
 **
 * @author Humberto Moreira <humberto.mn@gmail.com>
 * @package lib
 * @access public
 */
require_once( "musicvendor.php" );


class LastFm implements MusicVendor {

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

        // Prepares params
		$data['method'] = 'geo.gettopartists';
		$data['country'] = urlencode( $country );
		$data['page'] = urlencode( $page );
		$data['limit'] = 5;
		$data['api_key'] = urlencode( $this->key );

        // Sends request
        $xml = $this->sendRequest( $data );

        // Builds array for response
        $xml = $xml->topartists;
        $response = array();
        $response['totalPages'] = (int) $xml['totalPages'];
        $response['artists'] = array();
        foreach ( $xml->artist as $artist ) {

            $response['artists'][] = array(
                'id' => (string) $artist->mbid,
                'name' => (string) $artist->name,
                'img' => (string) $artist->image[1],
            );
        }
        return $response;
	}

	/**
	 * Returns details from an artist ID
	 *
	 * @param String[Required] $id
	 * @access public
	 * @return Array
	 */
	public function getArtistDetails( $id ){

        // Prepares params
        $data['method'] = 'artist.getinfo';
        $data['mbid'] = urlencode( $id );
        $data['api_key'] = urlencode( $this->key );

        // Sends request
        $xml = $this->sendRequest( $data );

        // Builds array for response
        $response = array();
        $response['name'] = (string) $xml->artist->name;
        $response['img'] = (string) $xml->artist->image[2];
        $response['id'] = (string) $xml->artist->mbid;
        return $response;

	}

    /**
     * Returns top tracks by artist ID
     *
     * @param String[Required] $id
     * @access public
     * @return Array
     */
    public function getTopTracks( $id ){

        // Prepares params
        $data['method'] = 'artist.gettoptracks';
        $data['mbid'] = urlencode( $id );
        $data['limit'] = 5;
        $data['api_key'] = urlencode( $this->key );

        // Sends request
        $xml = $this->sendRequest( $data );

        // Builds array for response
        $xml = $xml->toptracks;
        $response = array();
        foreach ( $xml->track as $track ) {

            $response[] = array(
                'id' => (string) $track->mbid,
                'name' => (string) $track->name
            );
        }
        return $response;

    }

}