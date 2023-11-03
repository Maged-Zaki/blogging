let article_content = document.getElementById('id_content');
let preview_content = document.getElementById('article-preview');


article_content.addEventListener("input", async function() {
    const csrfToken = getCookie("csrftoken");

    const response = await fetch("/preview_article", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({"article_content": article_content.value})
    });
    
    const data = await response.json();
    preview_content.innerHTML = data["article_preview_content"]

}); 


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}