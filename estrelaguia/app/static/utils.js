function setPositionTextarea(pos, e) {
	e.target.value = pos
}

function createCustomFields(text_name, e) {
	const height = 400
	const width = 400
	var components = "";
	div = document.getElementById('files_form')		
	for (let i = 0; i < e.target.files.length; i++) {
		file = e.target.files[i]
		components += "\
			<p>"+file.name+"</p>\
			<input type=\"number\" onClick=\"setPositionTextarea(button.getLastPos(),event)\"\
			 name=\""+file.name+"[]\" required/>\
			<input type=\"number\" name=\""+file.name+"[]\" value=\""+height+"\" required/>\
			<input type=\"number\" name=\""+file.name+"[]\" value=\""+width+"\"required/>\
			<label><input type=\"radio\" value=\"L\" name=\""+file.name+"[]\" checked/>Esquerda</label>\
			<label><input type=\"radio\" value=\"C\" name=\""+file.name+"[]\"/>Centro</label>\
			<label><input type=\"radio\" value=\"R\" name=\""+file.name+"[]\"/>Direita</label>"
	}
	div.innerHTML = components;
}

class Button {
	#prev
	#state
	#div
	#label
	#name
	#text_name
	#last_pos
	constructor(element, div, label, name) {
		this.#prev = element
		this.#state = 0
		this.#div = div
		this.#label = label
		this.#name = name
		this.#text_name = "text_"+this.#name
	}
	record(e) {
		this.#last_pos = e.target.selectionStart
	}
	getLastPos() {
		return this.#last_pos
	}
	swap(e) {
		if (this.#state) {
			this.#state = 0
			document.getElementById(this.#div).outerHTML = this.#prev.outerHTML
		} else {
			this.#state = 1
			e.target.outerHTML = "<div id=\""+this.#div+"\">\
			<input type=\"submit\" value=\""+this.#label+"\" />\
			<button type=\"button\" onClick=\"button.swap(event)\">Cancelar</button>\
			<textarea id=\""+this.#text_name+"\" name=\""+this.#name+"\" maxlength=\"1000\"\
			 autocomplete=\"on\" autocorrect=\"on\" autofocus required onBlur=\"button.record(event)\"></textarea>\
			<br>\
			<input id=\"input_files\" type=\"file\" name=\"files\" accept=\"image/*\" onChange=\"createCustomFields("+this.#text_name+",event)\" multiple />\
			<div id=\"files_form\"></div>\
			</div>"
		}
	}
}
