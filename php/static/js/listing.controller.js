angular.module( 'topmusic' ).controller( "ListingController", function( $scope, $http ){

    // initializes controller as view model
    var vm = this;
    vm.searchInput = '';
    vm.artists = [];
    vm.status = '';
    vm.currentPage = 0;
    vm.totalPages = 0;
    vm.currentPageGroup = 0;
    vm.pageGroupSize = 6;
    vm.totalPageGroups = 0;

    // Gets top artists from AJAX call by country name and page number
    vm.search = function( page ) {

        vm.status = '';
        vm.artists = [];
        vm.currentPage = page;
        vm.currentPageGroup = Math.ceil( vm.currentPage / vm.pageGroupSize );
        $http.post( '/', { 'country': vm.searchInput, 'page': page } ).
            success( function( data ) {
                if ( data['artists'].length == 0 ) {
                    vm.status = 'Nothing found!';
                }
                else {
                    vm.artists = data['artists'];
                    vm.totalPages = data['totalPages']
                    vm.totalPageGroups = Math.floor( vm.totalPages / vm.pageGroupSize );
                }
            })
            .
            error( function( data, status ) {
                vm.status = "Request failed";
                vm.artists = [];
            });
    }

    // Updates pagination buttons
    vm.prevPageGroupDisabled = function() {
        return vm.currentPageGroup === 1 ? "disabled" : "";
    }
    vm.nextPageGroupDisabled = function() {
        return vm.currentPageGroup === vm.totalPageGroups ? "disabled" : "";
    }
    vm.prevPageGroup = function() {
        vm.search( vm.currentPage - 1 );
    }
    vm.nextPageGroup = function() {
        vm.search( vm.currentPage + 1 );
    }
    vm.pageLinks = function() {

        var pages = [];
        if ( vm.totalPages > 0 ) {
            var start = ( ( vm.currentPageGroup * vm.pageGroupSize ) - vm.pageGroupSize ) + 1;
            for ( var i = start; i < start + vm.pageGroupSize; i++) {
                pages.push( i );
            }
        }
        return pages;
    };

});