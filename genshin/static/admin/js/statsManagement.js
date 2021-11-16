var total_hp = [],
    total_attack = [],
    total_defence = [],
    total_em = [],
    total_critRate = [],
    total_critDmg = [],
    total_selfHeal = [],
    total_recharge = [],
    total_cryoDmg = [],
    total_anemoDmg = [],
    total_geoDmg = [],
    total_physDmg = [];

var hpPercent = [],
    attackPercent = [],
    defencePercent = [];

// index(source): 0 - character, 1 - weapon, 2 - artifacts
function setPercent(value, stat, index) {

    switch (stat) {
        case "hp":
            hpPercent[index] = value;
            break;
        case "attack":
            attackPercent[index] = value;
            break;
        case "defence":
            defencePercent[index] = value;
            break;
    };

}

function setStats(value, stat, index) {

    if (index == 1) {
        if (stat == "-") {
            $("#weapon_stat").text("-")
            return;
        } else {
            $("#weapon_stat").text((value * 100).toFixed(2))
        }

    }

    var temp;
    eval("temp = total_" + stat)

    temp[index] = value;

    let total = 0;

    for (i = 0; i < temp.length; i++) {
        total += temp[i];
    }

    switch (stat) {
        case "em":
            $("#character_" + stat).text(total);
            break;
        case "critRate":
            $("#character_" + stat).text(((total + 0.05) * 100).toFixed(2));
            break;
        case "critDmg":
            $("#character_" + stat).text(((total + 0.5) * 100).toFixed(2));
            break;
        default:
            $("#character_" + stat).text(total.toFixed(2));
    }

}

function setHp(hp, index) {

    total_hp[index] = hp;

    let base = 0,
        totalPercent = 0;

    for (i = 0; i < total_hp.length; i++) {
        base += total_hp[i];
    }

    for (i = 0; i < hpPercent.length; i++) {
        totalPercent += hpPercent[i];
    }

    let result = Math.floor(base * (1 + totalPercent));

    $("#character_hp").text(result);

}

function setAttack(attack, index) {

    total_attack[index] = attack;

    let base = 0,
        totalPercent = 0;

    for (i = 0; i < total_attack.length; i++) {
        base += total_attack[i];
    }

    for (i = 0; i < attackPercent.length; i++) {
        totalPercent += attackPercent[i];
    }

    if (index == 1) {
        $("#weapon_attack").text(total_attack[1]);
    }

    /** 
     * base - Base Attack
     * totalPercent - ascension + weapon bonus + artifacts(%)
     * flat - feather + artifacts
     * */

    let result = Math.floor(base * (1 + totalPercent));
    // return total * (1 + totalPercent) + flat;

    $("#character_attack").text(result);

}

function setDefence(defence, index) {

    total_defence[index] = defence;

    let total = 0,
        totalPercent = 0;

    for (i = 0; i < total_defence.length; i++) {
        total += total_defence[i];
    }

    for (i = 0; i < defencePercent.length; i++) {
        totalPercent += defencePercent[i];
    }

    let result = total * (totalPercent + 1);

    $("#character_defence").text(result);
}