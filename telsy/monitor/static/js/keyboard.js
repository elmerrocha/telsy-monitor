const CURRENT_KEYBOARD_FRAME = document.location.pathname;
const keyboard = {
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
        value: '',
        capsLock: false
    },

    init() {
        // Create main elements
        this.elements.main = document.createElement('div');
        this.elements.keysContainer = document.createElement('div');

        // Setup main elements
        this.elements.main.classList.add('keyboard', 'keyboard--hidden');
        this.elements.keysContainer.classList.add('keyboard__keys');
        this.elements.keysContainer.appendChild(this.createKeys());

        this.elements.keys = this.elements.keysContainer.querySelectorAll('.keyboard__key');

        // Add to DOM
        this.elements.main.appendChild(this.elements.keysContainer);
        document.body.appendChild(this.elements.main);

        // Automatically use keyboard for elements with .use-keyboard-input
        document.querySelectorAll('.use-keyboard-input').forEach(element => {
            element.addEventListener('focus', () => {
                this.open(element.value, currentValue => {
                    element.value = currentValue;
                });
            });
        });
    },

    createKeys() {
        const fragment = document.createDocumentFragment();
        const keyLayout = [
            '!', '@', '#', '$', '%', '&', '(', ')', '=' ,'?', '¡', ' ', '7', '8', '9',
            'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', "'", ' ', '4', '5', '6',
            'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'ñ', '+', ' ', '1', '2', '3',
            'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '-', '_', ' ', '/', '0', '*',
            'caps', 'space', 'backspace', ' ',/*'clear',*/'done'/*, 'enter'*/
        ];

        // Creates HTML for an icon
        const createHtmlIcon = (icon_name) => {
            return `<i class='fa-solid fa-${icon_name}'></i>`;
        };

        keyLayout.forEach(key => {
            const keyElement = document.createElement('button');
            const insertLineBreak = ['9', '6', '3', '*'].indexOf(key) !== -1;
            //const insertSpaceBreak = ['?', '¡', '*', '_'].indexOf(key) !== -1;

            // Add attributes/classes
            keyElement.setAttribute('type', 'button');
            //keyElement.classList.add('keyboard__key', 'button', 'square', 's40', 'gradient-vertical');
            //if(CURRENT_KEYBOARD_FRAME == '/F1-agregar-medicamento/') keyElement.classList.add('keyboard__key', 'button', 'button-small', 'square', 'Med', 'gradient-vertical');
            keyElement.classList.add('keyboard__key', 'button', 'button-small', 'square', 's40', 'gradient-vertical');

            switch (key) {
                case ' ':
                    keyElement.classList.remove('gradient-vertical', 'square', 's40');
                    keyElement.classList.add('space');
                    break;

                case 'backspace':
                    keyElement.classList.remove('gradient-vertical', 'square', 's40');
                    keyElement.classList.add('qwerty_rectangle', 'yellow', 'red-key');
                    keyElement.innerHTML = createHtmlIcon('delete-left');
                    keyElement.addEventListener('click', () => {
                        this.properties.value = this.properties.value.substring(0, this.properties.value.length - 1);
                        this._triggerEvent('oninput');
                    });
                    break;
                case 'caps':
                    keyElement.classList.remove('gradient-vertical');
                    keyElement.classList.add('keyboard__key--activatable', 'cyan', 'white-key');
                    keyElement.innerHTML = createHtmlIcon('up-long');
                    keyElement.addEventListener('click', () => {
                        this._toggleCapsLock();
                        keyElement.classList.toggle('keyboard__key--active', this.properties.capsLock);
                    });
                    break;
                case 'space':
                    keyElement.classList.remove('square');
                    keyElement.classList.add('qwerty_rectangle', 'space_bar');
                    keyElement.addEventListener('click', () => {
                        this.properties.value += ' ';
                        this._triggerEvent('oninput');
                    });
                    break;
                case 'done':
                    keyElement.classList.add('keyboard__key--dark');
                    keyElement.innerHTML = '<span class="check-key">'+createHtmlIcon('square-check')+'</span>';
                    if (CURRENT_KEYBOARD_FRAME == '/login/') {
                        keyElement.innerHTML += ' Aceptar';
                    } else {
                        keyElement.innerHTML += ' Conectar';
                    }
                    keyElement.addEventListener('click', () => {
                        this.close();
                        this._triggerEvent('onclose');
                        if (CURRENT_KEYBOARD_FRAME == '/login/') loginUser();
                        else document.getElementById('connect-to-network').submit();
                    });
                    break;
                default:
                    keyElement.classList.add('bold-key');
                    keyElement.textContent = key.toLowerCase();
                    keyElement.addEventListener('click', () => {
                        this.properties.value += this.properties.capsLock ? key.toUpperCase() : key.toLowerCase();
                        this._triggerEvent('oninput');
                    });
                    break;
            }
            fragment.appendChild(keyElement);
            if (insertLineBreak) {
                fragment.appendChild(document.createElement('br'));
            }
        });
        return fragment;
    },

    _triggerEvent(handlerName) {
        if (typeof this.eventHandlers[handlerName] == 'function') {
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
        this.properties.value = initialValue || '';
        this.eventHandlers.oninput = oninput;
        this.eventHandlers.onclose = onclose;
        this.elements.main.classList.remove('keyboard--hidden');
    },

    close() {
        this.properties.value = '';
        this.eventHandlers.oninput = oninput;
        this.eventHandlers.onclose = onclose;
        this.elements.main.classList.add('keyboard--hidden');
    }
};

window.addEventListener('DOMContentLoaded', function () {
    keyboard.init();
});
