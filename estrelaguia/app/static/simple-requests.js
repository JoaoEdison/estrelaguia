async function upvote(e, route, token) {
	const resp = await fetch(route, {
		method: 'POST',
		headers: {
			'X-CSRFToken': token
		},
	})
	if (resp.ok) {
		e.originalTarget.outerHTML = downButton.getElements()
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
		e.originalTarget.outerHTML = upButton.getElements()
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
		e.originalTarget.outerHTML = removeFavButton.getElements()
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
		e.originalTarget.outerHTML = favButton.getElements()
	}
}
