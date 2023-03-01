const pageTitle = m("h5").text("Local Buckets").addClass("display-5");
const pageSubtitle = m("p").text("本地文件倉庫 (管理文件, 備份文件)").addClass(".lead");
const pageTitleArea = m("div")
  .append(pageTitle, pageSubtitle)
  .addClass("text-center");

const AppSubmitBtn = MJBS.createButton("submit", "primary");
const AppAlert = MJBS.createAlert();

$("#root").append(
  pageTitleArea.addClass("my-5"),
  m(AppAlert).addClass("my-3"),
);

init();

function init() {
  initProjects();
}

function initProjects() {
  axiosGet({
    url: "/api/all-projects",
    alert: AppAlert,
    onSuccess: (resp) => {
      const projects = resp.data;
      if (projects && projects.length > 0) {
        console.log(projects);
        // MJBS.appendToList(LabelList, labels.map(LabelItem));
      } else {
        AppAlert.insert("info", "尚未註冊項目, 請添加項目.");
        // MJBS.focus(LabelNameInput);
      }
    },
  });
}
