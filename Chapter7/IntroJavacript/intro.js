// Declare

var foo = 4;
var bar = "other"
let number = 3; 
const pi = 3.1416;
// let number = 5;

// If sentence

if (foo > 4){
    console.log("Is greater than 4")
}else if(foo == 4) {
    console.log("Is equal 4")
}else {
    console.log("Is lower than 4")
}

// For sentence

for(let i= 0; i<=10 ; i++){
    console.log("For :", i)
}

// Let scope , is not possible
// console.log(i)
let j = 0
while(j<10){
    console.log("While j", j)
    j++
}

// Function
function myFunction(name){
    // Reverse ` and place holder ${} 
    console.log(`Hello ${name}, How are you ${name}?`)
}
myFunction("Eduardo")

// Lists
const list = []
list.push("Red")
list.push("White")
console.log(`First element list : ${list[0]}`) // Get an element
// list = ["A"] not allow change the reference

// other for using list as a direct element
for (element in list){
    console.log(`Element of list: ${element}`)
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


