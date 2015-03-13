var diabetesControllers = angular.module('diabetesControllers', []);

diabetesControllers.controller('ItemListCtrl', ['$scope', '$http',
    function ($scope, $http) {
        $http.get('items').success(function (data){
            $scope.items = data.items;
            for (var i = data.items.length - 1; i >= 0; i--) {
                var httpget = 'items/' + data.items[i].id + '/inventory'
                $http.get(httpget).success(function (countDocument){
                    $scope.items[countDocument.item.id - 1].count = countDocument.item.count;
                });
            };
        });
    }]);

diabetesControllers.controller('TransactionCtrl', ['$scope', '$http',
    function ($scope, $http) {
        $http.get('items').success(function (data) {
            $scope.chooseItem = data.items;
        });
        $scope.add = function (transaction) {
            var newTxn = {
                item_id : $scope.transaction.id,
                quantity : $scope.transaction.quantity
            };
            var res = $http.post('/transactions', newTxn);
            res.success(function(data, status, headers, config) {
                console.log(newTxn);
            });
            res.error(function(data, status, headers, config) {
                alert( "failure message: " + JSON.stringify({data: data}));
            });
            $scope.item_id = '';
            $scope.quantity = '';
        };
    }]);
