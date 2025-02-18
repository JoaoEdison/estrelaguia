/*
   Copyright 2025 João E. R. Manica

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
*/

async function upvote(e, route, token) {
	const resp = await fetch(route, {
		method: 'POST',
		headers: {
			'X-CSRFToken': token
		},
	})
	if (resp.ok) {
		e.target.outerHTML = downButton.getElements()
		likes.innerHTML = likes.innerHTML.replace(/(^\d+)(.+$)/i, (match, p1, p2, offset, string) => {
			return parseInt(p1)+1+p2
		})
	}
}
async function remove_up(e, route, token) {
	const resp = await fetch(route, {
		method: 'DELETE',
		headers: {
			'X-CSRFToken': token
		},
	})
	if (resp.ok) {
		e.target.outerHTML = upButton.getElements()
		likes.innerHTML = likes.innerHTML.replace(/(^\d+)(.+$)/i, (match, p1, p2, offset, string) => {
			return parseInt(p1)-1+p2
		})
	}
}

async function favorite(e, route, token) {
	const resp = await fetch(route, {
		method: 'POST',
		headers: {
			'X-CSRFToken': token
		},
	})
	if (resp.ok) {
		e.target.outerHTML = removeFavButton.getElements()
	}
}
async function remove_favorite(e, route, token) {
	const resp = await fetch(route, {
		method: 'DELETE',
		headers: {
			'X-CSRFToken': token
		},
	})
	if (resp.ok) {
		e.target.outerHTML = favButton.getElements()
	}
}
