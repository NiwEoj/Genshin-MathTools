var totalHp = [],
    totalAttack = [],
    totalDefence = [];


function getHp() {

    var total = 0;

    for (i = 0; i < totalHp.length; i++) {
        total += totalHp[i];
    }

    return total;
}

function getAttack() {

    var total = 0;

    for (i = 0; i < totalAttack.length; i++) {
        total += totalAttack[i];
    }

    return total;
}

function getDefence() {

    var total = 0;

    for (i = 0; i < totalDefence.length; i++) {
        total += totalDefence[i];
    }

    return total;
}

function setHp(hp, index) {

    totalHp[index] = hp;
    $("#character_hp").text(getHp())

}

function setAttack(attack, index) {

    totalAttack[index] = attack;
    $("#character_attack").text(getAttack())

}

function setDefence(defence, index) {

    totalDefence[index] = defence;
    $("#character_defence").text(getDefence())
}
