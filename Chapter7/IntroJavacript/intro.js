// Declare

var foo = 4;
var bar = "other" // ; optional
let number = 3; 
const pi = 3.1416;
// let number = 5;
// pi = 2.4;

// If sentence

if (foo > 4){
    console.log("Is greater than 4")
}else if(foo == 4) {
    console.log("Is equal 4")
}else {
    console.log("Is lower than 4")
}

// For sentence

for(let i= 0; i<=10 ; i= i+1){
    console.log("For :", i)
}
// Let scope , is not possible
// console.log(i)

let j = "";
while(j!="AAA"){
    console.log("While j", j);
    j = j+"A"
}

// Function
function myFunction(name){
    // Reverse ` and place holder ${} 
    console.log(`Hello ${name}, How are you ${name}?`);
}
myFunction("Eduardo")

// Lists
const list = [];
list.push("Red")
list.push("White")
console.log(`First element list : ${list[0]}`) // Get an element
// list = ["A"] not allow change the reference

// By value
let n = 0
function add(n,times){
    for (let i= 1; i<= times; i++){
        n = n +1;
    }    
    console.log(`N inside add fun ${n}`);
    return n;
}
add(n, 20)
console.log(`N after call fun ${n}`)

// By reference
const listNames = ["Eduardo", "Carlos"];

function addNames(list,newName){
    listNames.push(newName);
}
addNames(listNames,"Camila");
console.log(`listNames after call fun ${listNames}`);


// other for using list as index in
for (index in listNames){
    console.log(`Index of list: ${index}, 
        element of the list ${listNames[index]}`)
}

// direct element
for (const element of listNames){
    console.log(`Element of list ${element}`)
}

// print list with limits
for (let i = 0; i<listNames.length ; i++){
    console.log(`Elemento ${i}, ${listNames[i]}`)
}

// JSON 
const dev = {
    name : "Eduardo",
    lastName : "Arias",
    age : 28,
    contactInfo: {
        phone: 3000000,
        email: "julianeduardoarias@outlook.com"
    },
    experience: {
        languages: ["Python", "Scala", "Clojure", "Java"] 
    }
}


const devs = [dev,{name: "Camila", experience: ["Typescript","Angular"]}]
// Access data, root properties
console.log(`Name: ${dev.name}`)
console.log(`Contact Info: ${dev.contactinfo}`) // It's case sensitive !!! 
console.log(`Contact Info: ${dev.contactInfo}`) // Is a object print 
console.log(`Contact Info: ${JSON.stringify(dev.contactInfo)}`) // Force to cast to String
console.log(`Email: ${dev.contactInfo.email}`) // Nested basic type
console.log(`Email: ${dev.experience.languages[1]}`) // Get a element of nested array

// Access of root object array
console.log(`Camila experience: ${devs[1].experience}`) // Get a array from array, dont show a []


