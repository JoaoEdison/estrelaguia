function setPositionTextarea(pos, e) {
	e.target.value = pos
}

class FileInputs {
	#text_area_field
	#name
	
	constructor(name,text_area_field) {
		this.#name = name
		this.#text_area_field = text_area_field
	}
	createCustomFields(e) {
		const height = 400
		const width = 400
		var components = "";
		for (let i = 0; i < e.target.files.length; i++) {
			let file = e.target.files[i]
			components += "\
				<p>"+file.name+"</p>\
				<input type=\"number\" onClick=\"setPositionTextarea("+this.#text_area_field+".getLastPos(),event)\"\
				 name=\""+file.name+"[]\" required/>\
				<input type=\"number\" name=\""+file.name+"[]\" value=\""+height+"\" required/>\
				<input type=\"number\" name=\""+file.name+"[]\" value=\""+width+"\"required/>\
				<label><input type=\"radio\" value=\"L\" name=\""+file.name+"[]\" checked/>Esquerda</label>\
				<label><input type=\"radio\" value=\"C\" name=\""+file.name+"[]\"/>Centro</label>\
				<label><input type=\"radio\" value=\"R\" name=\""+file.name+"[]\"/>Direita</label>"
		}
		document.getElementById('files_form').innerHTML = components;
	}
}

class FormElement {
	constructor() {}
	getElements() {
		return ""
	}
}

class RequestButton extends FormElement {
	#button_description
	#function_name
	constructor(description, function_name) {
		super()
		this.#button_description = description
		this.#function_name = function_name
	}
	getElements() {
		return "<button type=\"button\" onClick=\""+this.#function_name+"\">"+this.#button_description+"</button>"
	}
}

class SubmitButton extends FormElement {
	#submit_description
	constructor(description) {
		super()
		this.#submit_description = description
	}
	getElements() {
		return "<input type=\"submit\" value=\""+this.#submit_description+"\" />"
	}
}

class TextAreaForm extends FormElement {
	#id
	#name
	text
	#last_pos
	#maxlength
	constructor(id, name, text="", maxlength=1000) {
		super()
		this.#id = id
		this.#name = name
		this.text = text
		this.#maxlength = maxlength
	}
	record(e) {
		this.#last_pos = e.target.selectionStart
	}
	getLastPos() {
		return this.#last_pos
	}
	#getCols() {
		return parseInt(Math.sqrt(this.#maxlength))
	}
	#getRows() {
		return parseInt(this.#getCols() / 4)
	}
	getElements() {
		return "<textarea id=\""+this.#id+"\" name=\""+this.#id+"\" maxlength=\""+this.#maxlength+"\"\
		         rows=\""+this.#getRows()+"\" cols=\""+this.#getCols()+"\"\
			 autocomplete=\"on\" autocorrect=\"on\" autofocus required onBlur=\""+this.#name+".record(event)\">"
			+this.text+"</textarea><br>"
	}
}

class TextField extends FormElement {
	#id
	#label
	#text
	#max_len
	#size
	#required
	constructor(id, label, required=false, max_len=100, size=0, text="") {
		super()
		this.#id = id
		this.#label = label
		this.#required = required
		this.#max_len = max_len
		this.#text = text
		this.#size = size
	}
	#getRequiredAttr() {
		if (this.#required)
			return "required"
		return ""
	}
	#getSizeAttr() {
		if (this.#text.length)
			return this.#text.length
		if (this.#size)
			return this.#size
		return this.#max_len
	}
	getElements() {
		return "<label>"+this.#label+"<input id=\""+this.#id+"\"\
			name=\""+this.#id+"\" type=\"text\"\
			maxlength=\""+this.#max_len+"\"\
			value=\""+this.#text+"\" \
			size="+this.#getSizeAttr()+" "+this.#getRequiredAttr()+"/></label><br>"
	}
}

class Button {
	#name
	#prev
	#state
	#div
	#last_pos
	#other_elements
	#files
	constructor(name, element, div, files, others) {
		this.#name = name
		this.#state = 0
		this.#prev = element
		this.#div = div
		this.#files = files
		this.#other_elements = others
	}
	setPrev(element) {
		this.#prev = element
	}
	swap(e) {
		if (this.#state) {
			this.#state = 0
			document.getElementById(this.#div).outerHTML = this.#prev.outerHTML
		} else {
			this.#state = 1
			var outerHtml = "<div id=\""+this.#div+"\">"
			if (this.#other_elements)
				for (let i=0; i < this.#other_elements.length; i++)
					outerHtml += this.#other_elements[i].getElements()
			outerHtml += "<button type=\"button\" onClick=\""+this.#name+".swap(event)\">Cancelar</button><br>"
			if (this.#files) {
				outerHtml += "<input id=\"input_files\" type=\"file\" name=\"files\" accept=\"image/*\" onChange=\""+this.#files+".createCustomFields(event)\" multiple />\
			                     <div id=\"files_form\"></div>\
			                     </div>"
			}
			e.target.outerHTML = outerHtml
		}
	}
}
