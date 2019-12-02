var one = 'HELLO_+JQuery__??!!!!';


console.log(one);
//document.getElementById('message').innerHTML = one;
//alert('Hello!!!!?');

$('#test').text(one);
$('#test').fadeOut("slow");


//$('.myclass').text(one);

document.getElementsByClassName("myclass")[0].innerHTML = one;
