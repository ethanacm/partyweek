$("h1").css("transition","all 3s");
var arr = ["#ff6060","#f9ff60","#7aff60", "#60ffff", "#7560ff", "#f760ff"];
var current_color = 0;
function changeColor(){
   $("h1").css({
        color : arr[current_color]
      });
   current_color++;
   if(current_color > 5) {
       current_color = 0;
   }
}
changeColor();
setInterval(changeColor,3000);

