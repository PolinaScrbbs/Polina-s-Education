document.addEventListener("DOMContentLoaded", () => {
    const buttons = document.querySelectorAll(".details__btn");
    const taskContents = document.querySelectorAll(".task-content");

    buttons.forEach((button) => {
        button.addEventListener("click", () => {
            const taskId = button.getAttribute("data-task");

            // Скрываем весь контент
            taskContents.forEach((content) => {
                content.style.display = "none";
            });

            // Показываем контент для нажатой кнопки
            const taskContent = document.getElementById(taskId);
            if (taskContent) {
                taskContent.style.display = "block";
            }
        });
    });
});

document.getElementById('images').addEventListener('change', function(event) {
    const fileNames = event.target.files;
    const fileNamesList = document.getElementById('file-names');
    
    fileNamesList.innerHTML = ''; // Очистить список, если файлы были изменены
    
    // Пройтись по всем выбранным файлам и добавить их имена в блок
    for (let i = 0; i < fileNames.length; i++) {
      const fileName = fileNames[i].name;
      const fileItem = document.createElement('div');
      fileItem.textContent = fileName;
      fileNamesList.appendChild(fileItem);
    }
  });