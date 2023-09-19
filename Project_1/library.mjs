/** Class for remembering of one state of objects, user doesn't interfere with this Class directly */
class Memento {
    #state;
    /**
     * Remembers state
     * @param state
     */
    constructor(state) {
        this.#state = state;
    }

    /**
     * Get state
     * @returns {*} state
     */
    getState() {
        return this.#state;
    }
}

/** Class for working with mementos */
class Caretaker {
    #id;
    #mementos;
    /**
     * Create array for mementos and id for their indexing
     */
    constructor() {
        this.#id = 0;
        this.#mementos = [];
    }

    /**
     * Push new memento in array if object didn't have memento yet, otherwise rewrite old memento
     * @param instance of object for memento
     */
    saveState(instance) {
        let id = instance.getID();
        if (id === undefined) {
            instance.setID(this.#id++);
            this.#mementos.push(instance.saveState())
        } else {
            this.#mementos[id] = instance.saveState();
        }
    }

    /**
     * Call saveState for every instance in Array
     * @param {Array} instances
     */
    saveStates(instances) {
        instances.forEach(instance => this.saveState(instance));
    }

    /**
     * Load old state of instance from memento if it exists
     * @param instance of recovering object
     */
    loadState(instance) {
        let id = instance.getID();
        if (id !== undefined)
            instance.loadState(this.#mementos[id]);
    }

    /**
     * Call loadState for every instance in Array
     * @param {Array} instances
     */
    loadStates(instances) {
        instances.forEach(instance => this.loadState(instance));
    }
}

/** Base class for classes that Caretaker can take care of */
class OriginatorBase {
    #id;

    /**
     * get ID for indexing of memento in Caretaker
     * @returns {Number}
     */
    getID() {
        return this.#id;
    }

    /**
     * set ID for indexing of memento in Caretaker
     * @param {Number} value
     */
    setID(value) {
        this.#id = value;
    }
}

/** Class for elements of nature */
class Element extends OriginatorBase {
    /**
     * constructor description
     * @param {String} element
     */
    constructor(element) {
        super();
        this._element = element;
    }

    /**
     * @public
     * @param {String} value name of element
     */
    set element(value) {
        this._element = value;
    }

    /**
     * @returns {String} name of element
     */
    get element() {
        return this._element;
    }

    /**
     * @returns {Memento} with actual state
     */
    saveState() {
        return new Memento(this._element);
    }

    /**
     * @param {Memento} memento restores old state
     */
    loadState(memento) {
        this._element = memento.getState();
    }
}

/** Class for magic spells */
class Spell extends OriginatorBase {
    /**
     * @param {String} spell
     * @param {Element} element
     * @param {Number} mana
     */
    constructor(spell, element, mana) {
        super();
        this._spell = spell;
        this._element = element;
        this._mana = mana;
    }

    /**
     * @public
     * @param {String} value
     */
    set spell(value) {
        this._spell = value;
    }

    /**
     * @returns {String}
     */
    get spell() {
        return this._spell;
    }

    /**
     * @public
     * @param {Element} value
     */
    set element(value) {
        this._element = value;
    }

    /**
     * @returns {Element}
     */
    get element() {
        return this._element;
    }

    /**
     * @public
     * @param {Number} value
     */
    set mana(value) {
        this._mana = value;
    }

    /**
     * @returns {Number}
     */
    get mana() {
        return this._mana;
    }

    /**
     * @returns {Memento} with actual state
     */
    saveState() {
        return new Memento([this._spell, this._element, this._mana]);
    }

    /**
     * @param {Memento} memento restores old state
     */
    loadState(memento) {
        [this._spell, this._element, this._mana] = memento.getState();
    }
}

/** Class for wizards */
class Wizard extends OriginatorBase {
    /**
     * @param {String} name
     * @param {Number} mana
     * @param {[Element] | Element} synergies
     */
    constructor(name, mana, synergies) {
        super();
        if (!(synergies instanceof Array))
            synergies = [synergies];

        this._name = name;
        this._synergies = synergies;
        this._mana = mana;
    }

    /**
     * @public
     * @param {String} value
     */
    set name(value) {
        this._name = value;
    }

    /**
     * @returns {String}
     */
    get name() {
        return this._name;
    }

    /**
     * @public
     * @param {Number} value
     */
    set mana(value) {
        this._mana = value;
    }

    /**
     *
     * @returns {Number}
     */
    get mana() {
        return this._mana;
    }

    /**
     * @public
     * @param {[Element] | Element} value
     */
    set synergies(value) {
        this._synergies = value instanceof Array ? value : [value];
    }

    /**
     * @returns {[Element]}
     */
    get synergies() {
        return this._synergies;
    }

    /**
     * @returns {Memento} with actual state
     */
    saveState() {
        return new Memento([this._name, this._synergies, this._mana]);
    }

    /**
     * @param {Memento} memento restores old state
     */
    loadState(memento) {
        [this._name, this._synergies, this._mana] = memento.getState();
    }
}

/** Class for grimoars with magic spells */
class Grimoar extends OriginatorBase {
    /**
     * @param {Wizard} owner
     * @param {[Spell] | Spell} spells
     */
    constructor(owner, spells) {
        super();
        if (!(spells instanceof Array))
            spells = [spells];

        this._owner = owner;
        this._spells = spells;
    }

    /**
     * @public
     * @param {Wizard} value
     */
    set owner(value) {
        this._owner = value;
    }

    /**
     * @returns {Wizard}
     */
    get owner() {
        return this._owner;
    }

    /**
     * @public
     * @param {[Spell] | Spell} value
     */
    set spells(value) {
        this._spells = (value instanceof Array) ? value : [value];
    }

    /**
     * @returns {[Spell]}
     */
    get spells() {
        return this._spells;
    }

    /**
     * @returns {Memento} with actual state
     */
    saveState() {
        return new Memento([this._owner, this._spells]);
    }

    /**
     * @param {Memento} memento restores old state
     */
    loadState(memento) {
        [this._owner, this._spells] = memento.getState();
    }
}


export { Element, Spell, Grimoar, Wizard, Caretaker };