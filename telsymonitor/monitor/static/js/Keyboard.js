var CurrentFrame = document.location.pathname;
const Keyboard = {
    elements: {
        main: null,
        keysContainer: null,
        keys: []
    },

    eventHandlers: {
        oninput: null,
        onclose: null
    },

    properties: {
        value: "",
        capsLock: false
    },

    init() {
        // Create main elements
        this.elements.main = document.createElement("div");
        this.elements.keysContainer = document.createElement("div");

        // Setup main elements
        this.elements.main.classList.add("keyboard", "keyboard--hidden");
        this.elements.keysContainer.classList.add("keyboard__keys");
        this.elements.keysContainer.appendChild(this._createKeys());

        this.elements.keys = this.elements.keysContainer.querySelectorAll(".keyboard__key");

        // Add to DOM
        this.elements.main.appendChild(this.elements.keysContainer);
        document.body.appendChild(this.elements.main);

        // Automatically use keyboard for elements with .use-keyboard-input
        document.querySelectorAll(".use-keyboard-input").forEach(element => {
            element.addEventListener("focus", () => {
                this.open(element.value, currentValue => {
                    element.value = currentValue;
                });
            });
        });
    },

    _createKeys() {
        const fragment = document.createDocumentFragment();
        const keyLayout = [
            "!", "@", "#", "$", "%", "&", "(", ")", "=" ,"?", "¡", " ", "7", "8", "9",
            "q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "'", " ", "4", "5", "6",
            "a", "s", "d", "f", "g", "h", "j", "k", "l", "ñ", "+", " ", "1", "2", "3",
            "z", "x", "c", "v", "b", "n", "m", ",", ".", "-", "_", " ", "/", "0", "*",
            "caps", "space", "backspace", " ",/*"clear",*/"done"/*, "enter"*/
        ];

        // Creates HTML for an icon
        const createIconHTML = (icon_name) => {
            //return `<i class="material-icons">${icon_name}</i>`;
            return `<i class="fas fa-${icon_name}"></i>`;
        };

        keyLayout.forEach(key => {
            const keyElement = document.createElement("button");
            const insertLineBreak = ["3", "6", "9", "*"].indexOf(key) !== -1;
            //const insertSpaceBreak = ["?", "¡", "*", "_"].indexOf(key) !== -1;

            // Add attributes/classes
            keyElement.setAttribute("type", "button");
            //keyElement.classList.add("keyboard__key", "button", "square", "s40", "gradient-vertical");
            //if(CurrentFrame == "/F1-agregar-medicamento/") keyElement.classList.add("keyboard__key", "button", "button-small", "square", "Med", "gradient-vertical");
            keyElement.classList.add("keyboard__key", "button", "button-small", "square", "s40", "gradient-vertical");

            switch (key) {
                case " ":
                    keyElement.classList.add("space");
                    keyElement.classList.remove("gradient-vertical", "square", "s40");
                    break;

                case "backspace":
                    keyElement.classList.remove("gradient-vertical", "square", "s40");
                    if(CurrentFrame == "/F1-agregar-medicamento/") keyElement.classList.add("keyboard__key--wide", "qwerty_rectangleMed", "yellow");
                    else keyElement.classList.add("keyboard__key--wide", "qwerty_rectangle", "yellow");
                    keyElement.innerHTML = createIconHTML("backspace");

                    keyElement.addEventListener("click", () => {
                        this.properties.value = this.properties.value.substring(0, this.properties.value.length - 1);
                        this._triggerEvent("oninput");
                    });

                    break;


                /*case "clear":
                keyElement.classList.remove("gradient-vertical");
                    keyElement.classList.add("keyboard__key--wide", "red");
                    keyElement.innerHTML = createIconHTML("clear");

                    keyElement.addEventListener("click", () => {
                        this.properties.value = "";
                        this._triggerEvent("oninput");
                    });

                    break;*/

                case "caps":
                    keyElement.classList.remove("gradient-vertical");
                    if(CurrentFrame == "/F1-agregar-medicamento/") keyElement.classList.add("keyboard__key--wide", "keyboard__key--activatableMed", "cyan");
                    else keyElement.classList.add("keyboard__key--wide", "keyboard__key--activatable", "cyan");
                    //keyElement.innerHTML = createIconHTML("keyboard_capslock");
                    keyElement.innerHTML = createIconHTML("shift");


                    keyElement.addEventListener("click", () => {
                        this._toggleCapsLock();
                        keyElement.classList.toggle("keyboard__key--active", this.properties.capsLock);
                    });

                    break;

                /*case "enter":
                    keyElement.classList.remove("gradient-vertical", "square", "s40");
                    keyElement.classList.add("keyboard__key--wide", "qwerty_rectangle", "green");
                    keyElement.innerHTML = createIconHTML("keyboard_return");

                    keyElement.addEventListener("click", () => {
                        this.properties.value += "\n";
                        this._triggerEvent("oninput");
                    });

                    break;*/

                case "space":
                    keyElement.classList.remove("square");
                    keyElement.classList.add("keyboard__key--extra-wide", "qwerty_rectangle", "space_bar");
                    keyElement.innerHTML = createIconHTML("blankspace");

                    keyElement.addEventListener("click", () => {
                        this.properties.value += " ";
                        this._triggerEvent("oninput");
                    });

                    break;

                case "done":
                    keyElement.classList.add("keyboard__key--wide", "keyboard__key--dark");
                    //keyElement.innerHTML = createIconHTML("check_circle");
                    keyElement.innerHTML = createIconHTML("check-square");
                    if (CurrentFrame == "/login/") keyElement.innerHTML += "Aceptar";
                    else keyElement.innerHTML += "Conectar";


                    keyElement.addEventListener("click", () => {
                        this.close();
                        this._triggerEvent("onclose");
                        if (CurrentFrame == "/login/") LoginUser();
                        else document.getElementById("ConnectNetwork").submit();
                    });

                    break;

                default:
                    keyElement.textContent = key.toLowerCase();

                    keyElement.addEventListener("click", () => {
                        this.properties.value += this.properties.capsLock ? key.toUpperCase() : key.toLowerCase();
                        this._triggerEvent("oninput");
                    });

                    break;
            }

            fragment.appendChild(keyElement);
            if (insertLineBreak) {
                fragment.appendChild(document.createElement("br"));
            }

        });

        return fragment;
    },

    _triggerEvent(handlerName) {
        if (typeof this.eventHandlers[handlerName] == "function") {
            this.eventHandlers[handlerName](this.properties.value);
        }
    },

    _toggleCapsLock() {
        this.properties.capsLock = !this.properties.capsLock;
        for (const key of this.elements.keys) {
            if (key.childElementCount === 0) {
                key.textContent = this.properties.capsLock ? key.textContent.toUpperCase() : key.textContent.toLowerCase();
            }
        }
    },

    open(initialValue, oninput, onclose) {
        this.properties.value = initialValue || "";
        this.eventHandlers.oninput = oninput;
        this.eventHandlers.onclose = onclose;
        this.elements.main.classList.remove("keyboard--hidden");
    },

    close() {
        this.properties.value = "";
        this.eventHandlers.oninput = oninput;
        this.eventHandlers.onclose = onclose;
        this.elements.main.classList.add("keyboard--hidden");
    }
};

window.addEventListener("DOMContentLoaded", function () {
    Keyboard.init();
});
