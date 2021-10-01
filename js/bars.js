const navToggle = document.querySelector(".toggle")
const navToggle1 = document.querySelector(".toggle1")
const navMenu = document.querySelector(".nav_menu")

navToggle.addEventListener("click", () => {
    navMenu.classList.toggle("nav_menu_visible")
    
}) 
navToggle1.addEventListener("click", () => {
    navMenu.classList.remove("nav_menu_visible")
})