document.addEventListener("DOMContentLoaded", function () {
  const modalEl = document.getElementById("messageModal");
  if (modalEl) {
    const myModal = new bootstrap.Modal(modalEl);
    myModal.show();
  }
});
