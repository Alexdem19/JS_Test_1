// let arr = ["one",2,3,"4",5];

// arr.forEach(function(item, i, mass){
//     console.log(i + ': ' + item + '(massiv: ' + mass +')');
// });

// console.log(arr);

// let mass = [1,3,4,6,7];

// for (let key of mass){
//     console.log(key)
// }


// let ans = prompt("",""),
//     arr = [];

// arr = ans.split(',');
// console.log(arr)

let arr =[1,14,23,15,55,33];
    i = arr.sort(compareNum);

// console.log(compareNum);

// function compareNum(a,b){
//     return a-b;
// }

// console.log(arr);

let soldier = {
    health: 400,
    armor: 200
};

let john = {
    health:100
};

john.__proto__ = soldier;

console.log(john);
console.log(john.armor);






