var diabetesControllers = angular.module('diabetesControllers', []);

diabetesControllers.controller('ItemListCtrl', ['$scope', '$http',
    function ($scope, $http) {
        $scope.tableHidden = true;

        $scope.transaction = {
            adjustment: false,
            quantity: -1
        };

        $scope.updateInventory = function () {
            for (var i = $scope.items.length - 1; i >= 0; i--) {
                var uriString = 'items/' + $scope.items[i].id + '/inventory'
                $http.get(uriString).success(function (countDocument){
                    $scope.items[countDocument.item.id - 1].count = countDocument.item.count;
                });
            };
        };

        $http.get('items').success(function (data){
            $scope.items = data.items;
            $scope.updateInventory();
            $scope.tableHidden = false;
        });

        $scope.add_txn = function (transaction) {
            var newTxn = {
                item_id : $scope.transaction.id,
                quantity : $scope.transaction.quantity,
                adjustment : $scope.transaction.adjustment
            };

            $scope.items[newTxn.item_id - 1].count += newTxn.quantity;

            var res = $http.post('/transactions', newTxn);
            res.success(function(data, status, headers, config) {
                console.log(newTxn);
                $http.get('items/' + newTxn.item_id + '/inventory').success(function (countDocument) {
                    $scope.items[countDocument.item.id - 1].count = countDocument.item.count;
                });
            });
            res.error(function(data, status, headers, config) {
                alert( "failure message: " + JSON.stringify({data: data}));
                $http.get('items/' + newTxn.item_id + '/inventory').success(function (countDocument) {
                    $scope.items[countDocument.item.id - 1].count = countDocument.item.count;
                });
            });

            $scope.transaction = {
                id: '',
                quantity: -1,
                adjustment: false
            };
        }
    }]);

diabetesControllers.controller('DoseCalcCtrl', ['$scope',
    function ($scope) {
        $scope.carbs = 0;
        $scope.ic = 7.5;
        $scope.insulinOB = 0;
        $scope.activityMultiplier = 1.0;
        $scope.currentBG = 10;
        $scope.targetBG = 8;
        $scope.correctionSensitivity = 2.8;

        $scope.calcDose = function () {
            var correctionDose = Math.max(0, ((($scope.currentBG - $scope.targetBG) / $scope.correctionSensitivity) - $scope.insulinOB));
            var foodDose = $scope.carbs / $scope.ic;
            $scope.dose = (foodDose + correctionDose) * $scope.activityMultiplier;
        };

        $scope.calcDose();

    }]);
