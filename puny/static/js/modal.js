const closeModal = document.getElementById("close-modal");
const openModal = document.getElementById("open-modal");
const modalBody = document.getElementById("modal");

closeModal.addEventListener("click", () => {
  modalBody.classList.add("hidden");
});

openModal.addEventListener("click", () => {
  modalBody.classList.remove("hidden");
});
