function getCookie(name) {
	const value = `; ${document.cookie}`;
	const parts = value.split(`; ${name}=`);
	if (parts.length === 2) return parts.pop().split(";").shift();
}

function submitHandler(id) {
    const textareaValue = document.getElementById(`textarea_${id}`).value;
    const text = document.getElementById(`text_${id}`);
    const modal = document.getElementById(`modal_edit_post_${id}`);

    fetch(`/edit/${id}`, {
        method: "POST",
        headers: {
            "Content-type": "application/json",
            "X-CSRFToken": getCookie("csrf_token"),
        },
        body: JSON.stringify({
            text: textareaValue,
        }),
    })
        .then((response) => response.json())
        .then((result) => {
            text.innerHTML = result.data;

            modal.classList.remove('show');
            modal.setAttribute('aria-hidden', 'true');
            modal.setAttribute('style', 'display: none');

            const modalsBackdrops = document.getElementsByClassName('modal-backdrop');

            for (let i = 0; i < modalsBackdrops.length; i++) {
                document.body.removeChild(modalsBackdrops[i]);
            }
        });
    window.location.reload();
}


function likeHandler(id, whoYouLiked) {
    const btn = document.querySelector(`#like_btn_${id}`);

    btn.classList.remove("red")
    btn.classList.remove("text-muted")

    if (whoYouLiked.indexOf(id) >= 0) {
        var liked = true;
    } else {
        var liked = false;
    }

    if (liked === true) {
        fetch(`/unlike/${id}`)
		.then(response => response.json)
        .then(result => {
            btn.classList.add("red");
            location.reload();
		});
    } else {
        fetch(`/like/${id}`)
        .then(response => response.json)
        .then(result => {
            btn.classList.add("text-muted");
            location.reload();
        });
    }
}
