angular.module( 'topmusic' ).controller( "DetailsController", function( $scope, $http ){

    // initializes controller as view model
    var vm = this;
    vm.name = '';
    vm.img = '';
    vm.tracks = []
    vm.status = ''

    // Gets Artist Details
    $scope.$watch( 'id', function( value ) {
        $http.post( '/artist/details/' + value + '/', { 'id': value } ).
            success( function( data, status ) {
                vm.status = status;
                vm.name = data['name'];
                vm.img = data['img'];
                vm.tracks = data['tracks'];
            })
            .
            error( function( data, status ) {
                vm.status = "Request failed";
                vm.tracks = [];
            });
    });

});