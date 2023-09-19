import {Element, Spell, Wizard, Grimoar, Caretaker} from "./library.mjs";

// Creating objects
let fire = new Element("Fire");
let water = new Element("Water");
let lightning = new Element("Lightning");

let fireball = new Spell("Fireball", fire, 50);
let waterBarrier = new Spell("Water Barrier", water, 20);
let thunder = new Spell("Thunder", lightning, 100);
let energeticPrison = new Spell("Energetic Prison", lightning, 80);

let sualcatnas = new Wizard("Sualcatnas", 500, [water, lightning]);
let yelserpsivle = new Wizard("Yelserpsivle", 400, fire);

let book = new Grimoar(sualcatnas, [fireball, thunder, waterBarrier, energeticPrison]);

// Create instance of caretaker
let states = new Caretaker();

console.log("-----Show starting state of book, fireball and yelserpsivle in console-----");
console.log(book);
console.log(fireball);
console.log(yelserpsivle);

// Save state of one object
states.saveState(book);
states.saveState(yelserpsivle);
//Save states of array of objects
states.saveStates([book, sualcatnas, lightning, fireball, waterBarrier]);


// Changes of various objects
book.owner = yelserpsivle;
waterBarrier.spell = "Some bad data";
fireball.element = lightning;
fireball.spell = "Energetic ball";
fireball.mana = 123;
lightning.element = "energy";
yelserpsivle.synergies = [lightning, fire, water];

console.log("-----Show actual state of book, fireball and yelserpsivle in console-----");
console.log(book);
console.log(fireball);
console.log(yelserpsivle);

// Load original state of one object
states.loadState(book);
states.loadState(sualcatnas);
// Load original states of array of objects
states.loadStates([book, yelserpsivle, lightning]);

console.log("-----Checking if actual state of book and yelserpsivle in same as in the beginning-----");
console.log(book);
console.log(yelserpsivle);

console.log("-----Checking if actual state of fireball is still changed-----");
console.log(fireball);
