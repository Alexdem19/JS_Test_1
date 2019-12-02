let money, time;

function start(){
    money = +prompt(" Ваш бюжет на месяц? ", ''); 
    time = prompt('Введите дату в формате YYYY-MM-DD ', '');

    while(isNaN(money) || money =="" || money == null) {
       money = +prompt(" Ваш бюжет на месяц? ", ''); 

    }

}
start();


appData = {
    budjet:money,
    timeData : time,
    expenses : { },
    optionalExpenses : {},
    income :[],
    savings : true
};

function chooseExpenses() {
    for (let i = 0; i <2; i++) {
        let a = prompt('Статья расходов',''),
            b = prompt('Во сколько обойдется?','');
        
        if ( (typeof(a)) === 'string' && (typeof(a)) != null 
            && (typeof(b)) != null  && a != '' && b != '' && a.length <50 ) {
            console.log("done");
            appData.expenses[a] = b;
        }else{
            //i--;
    
        }
    }
}
chooseExpenses();


appData.moneyPerDay = (appData.budjet / 30).toFixed(2);

alert("Ежедневный бюджет : " + appData.moneyPerDay )

// console.log(appData);
// console.log(money);
// console.log(time);

console.log(appData.moneyPerDay);
console.log(typeof(appData.moneyPerDay));
if (appData.moneyPerDay < 100 ) {
    console.log ('Минимальный уровень достатка');
} else if (appData.moneyPerDay > 100 && appData.moneyPerDay < 2000) {
    console.log ('Средний уровень достатка');
} else if (appData.moneyPerDay >= 2000) {
    console.log ('Высокий уровень достатка');
} else {
    console.log(" Произошла ошибка")
    console.log(appData.moneyPerDay);
}


console.log(appData);

function checkSavings() {
    if (appData.savings == true) {
        let save = +prompt("Какова сумма накоплений?"),
            percent = +prompt("Под какой процент?");

        appData.monthIncome = save/100/12*percent;
        alert(' Доход в месяц с вашего депозита :' + appData.monthIncome);
    }
}

checkSavings();