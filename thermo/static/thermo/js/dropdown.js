document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".delete-btn").forEach(button => {
        button.addEventListener("click", function (event) {
            event.preventDefault();
            if (confirm("Удалить?")) {
                const postId = this.getAttribute("data-home-id");
                const deleteUrl = this.getAttribute("data-delete-url").replace("0", postId);
                const csrfToken = this.getAttribute("data-csrf-token");

                const form = document.createElement("form");
                form.method = "POST";
                form.action = deleteUrl;
                form.style.display = "none";

                const csrfInput = document.createElement("input");
                csrfInput.type = "hidden";
                csrfInput.name = "csrfmiddlewaretoken";
                csrfInput.value = csrfToken;
                form.appendChild(csrfInput);

                document.body.appendChild(form);
                form.submit();
            }
        });
    });
});