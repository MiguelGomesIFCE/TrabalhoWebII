document.addEventListener("input", e => {
    if (e.target.id === "busca") {
        const termo = e.target.value.toLowerCase();
        document.querySelectorAll(".lista li").forEach(li => {
            li.style.display = li.innerText.toLowerCase().includes(termo)
                ? "flex" : "none";
        });
    }
});