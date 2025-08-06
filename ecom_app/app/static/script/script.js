document.addEventListener("DOMContentLoaded", () => {
    const search = document.getElementById("search");
    const searchBtn = document.getElementById("search-btn");

    if (search && searchBtn) {
        searchBtn.addEventListener("click", () => {
            const searchValue = search.value;
            alert("Searching for: " + searchValue);
        });
    } else {
        console.error("Search input or button not found!");
    }
});


document.getElementById('options').addEventListener('change', () =>{
    let selectedvalue = this.value;
    if(selectedvalue){
        window.location.href = selectedvalue;
    }
})

document.getElementById("addToCartButton").addEventListener("click", function() {
    console.log("Button Clicked!");
});

document.getElementById("addToCartForm").addEventListener("submit", function(event) {
    console.log("Form Submitted!");
});

document.querySelector("form").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent page reload

    fetch(this.action, {
        method: "POST",
        body: new FormData(this),
        headers: {
            "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert("✅ " + data.message);
        } else if (data.error) {
            alert("❌ " + data.error);
        }
    })
    .catch(error => console.log("❌ Fetch Error:", error));
});




