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
        $scope.add_txn = function (transaction) {
            var newTxn = {
                item_id : $scope.transaction.id,
                quantity : $scope.transaction.quantity,
                adjustment : $scope.transaction.adjustment
            };
            var res = $http.post('/transactions', newTxn);
            res.success(function(data, status, headers, config) {
                $scope.items[newTxn.item_id - 1].count += newTxn.quantity;
                console.log(newTxn);
            });
            res.error(function(data, status, headers, config) {
                alert( "failure message: " + JSON.stringify({data: data}));
            });
            $scope.transaction.id = '';
            $scope.transaction.quantity = '';
        }
    }]);

diabetesControllers.controller('TransactionCtrl', ['$scope', '$http',
    function ($scope, $http) {
        $scope.transactionList = [];
        $http.get('transactions').success(function (data) {
            $scope.transactionList = data.transactions;

        })

        $scope.config = {
            itemsPerPage: 10,
            maxPages: 5,
            fillLastPage: "yes"
        }
    }]);
