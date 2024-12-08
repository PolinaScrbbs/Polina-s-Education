document.addEventListener("DOMContentLoaded", () => {
    const button = document.querySelector("#selected-option");
    const list = document.querySelector(".filters__list");
    const items = document.querySelectorAll(".filters__list li");

    button.addEventListener("click", (event) => {
        event.stopPropagation();
        list.classList.toggle("filters__list--visible");
    });

    document.addEventListener("click", () => {
        list.classList.remove("filters__list--visible");
    });

    items.forEach((item) => {
        item.addEventListener("click", (event) => {
            button.textContent = event.target.textContent;

            items.forEach((el) => el.classList.remove("active"));

            item.classList.add("active");

            list.classList.remove("filters__list--visible");
        });
    });
});        


document.addEventListener("DOMContentLoaded", () => {
    const modal = document.getElementById("modal");
    const closeModalButton = modal.querySelector(".modal__close");
    const yesButton = modal.querySelector(".modal__yes");
    const noButton = modal.querySelector(".modal__no");
    const groupItems = document.querySelectorAll(".groups__item");

    groupItems.forEach(item => {
        item.addEventListener("click", () => {
            modal.style.display = "flex"; 
        });
    });

    closeModalButton.addEventListener("click", () => {
        modal.style.display = "none"; 
    });

    noButton.addEventListener("click", () => {
        modal.style.display = "none"; 
    });

    yesButton.addEventListener("click", () => {
        alert("Вы вступили в группу!"); 
        modal.style.display = "none"; 
    });

    modal.addEventListener("click", (event) => {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    });
});