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
  initLabels();
  MoneyList.init();
  NotesList.init();
}

function initLabels() {
  axiosGet({
    url: "/api/all-labels",
    alert: AppAlert,
    onSuccess: (resp) => {
      const labels = resp.data;
      if (labels && labels.length > 0) {
        MJBS.appendToList(LabelList, labels.map(LabelItem));
      } else {
        AppAlert.insert("info", "無預設標籤, 請新增標籤.");
        FormArea_CreateLabel.show();
        MJBS.focus(LabelNameInput);
      }
    },
  });
}
