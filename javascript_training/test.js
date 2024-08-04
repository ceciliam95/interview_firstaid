var storeManager = {};
storeManager.age = 34;
storeManager.socialSkill = 3;


function printHaha (i) {
    var train1 = ["te","ted","deid"];
    if (i < train1.length)
    {
        console.log(train1[i]);
    }
    else 
    {   
        
        console.log(`storeManager age: ${storeManager.age}`);
        console.log(`type of storeManage age: ${typeof(storeManager.age)}`);
    }
}


for (var i = 1; i <= 4; i++)
{
    printHaha (i);
}

var i = 4;
while (i >= 1)
{   
    console.log(i);
    i -= 1;
}