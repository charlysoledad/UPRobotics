angular.module('Dashboard').directive("commChart", function(){
    return {
        restrict: 'E',
        scope:{
            state: '=',
            width: '=',
            height: '='
        },
        template: "<canvas id='canvas' width='size.width' height='size.height'/>",
        link: function(scope, element, attrs) {
            scope.canvas = element.find('canvas')[0];
            scope.ctx = scope.canvas.getContext('2d');
            /* console.log(element);
            console.log(scope.ctx); */

            scope.canvas.width = scope.width;
            scope.canvas.height = scope.height;

            var ctx = scope.ctx;
            var state = scope.state;

            var width = scope.canvas.offsetWidth;
            var height = scope.canvas.offsetHeight;
            var centerX = width / 2;
            var centerY = height / 2;

            var startColor = '#FF0000';
            var endColor= '#0DBE16';
            var backgroundColor = '#FF0000';

            function drawGraph(state) {
                var gradient = ctx.createLinearGradient(0,0,width,0)
                gradient.addColorStop(1,endColor);

                var ratio = 0;

                if(state > 1)
                    ratio = 1;
                else if(state < 0)
                    ratio = 0;
                else
                    ratio = (state - 0) / (1 - 0);

                ctx.clearRect(0,0,width,height);
                ctx.strokeStyle = gradient;
                ctx.lineWidth = height;
                ctx.beginPath();
                ctx.moveTo(0,centerY);
                ctx.lineTo(width*ratio,centerY)
                ctx.stroke();

                ctx.strokeStyle = backgroundColor;
                ctx.beginPath();
                ctx.moveTo(width * ratio, centerY);
                ctx.lineTo(width, centerY);
                ctx.stroke();
            }

            scope.$watch('state', function(newValue) {
                drawGraph(parseFloat(newValue), scope.min, scope.max);
              });
            
        }
    };

});