document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('input[type=file]').forEach(input => {
    input.onchange = () => {
      if (input.files.length > 0) {
        if (input.files[0].size > 99999999) {
          alert("Your video file is too large. Please keep your upload smaller than 100MB. (Try compressing your video file? Most 1-2 minute videos are less than 30MB.)");
          return false;
        }
        input.parentNode.parentNode.classList.add("has-name");
        input.parentNode.parentNode.classList.add("file");
        input.parentNode.parentNode.classList.add("is-block");
        input.parentNode.querySelectorAll(".file-name").forEach(node => {
          node.parentNode.removeChild(node);
        });
        let node = document.createElement("span");
        node.classList.add("file-name");
        node.textContent = input.files[0].name;
        input.parentNode.appendChild(node);
      }
    }
  });
  document.querySelectorAll("form").forEach(form => {
    form.addEventListener('submit', () => {
      form.querySelectorAll("button[type=submit]").forEach(button => {
        button.classList.add("is-loading");
      });
    });
  });
  // Get all "navbar-burger" elements
  const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);

  // Check if there are any navbar burgers
  if ($navbarBurgers.length > 0) {

    // Add a click event on each of them
    $navbarBurgers.forEach(el => {
      el.addEventListener('click', () => {

        // Get the target from the "data-target" attribute
        const target = el.dataset.target;
        const $target = document.getElementById(target);

        // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
        el.classList.toggle('is-active');
        $target.classList.toggle('is-active');

      });
    });
  }
});