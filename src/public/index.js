const pageTitle = m("h5").text("Local Buckets").addClass("display-5");
const pageSubtitle = m("p").text("本地文件倉庫 (管理文件, 備份文件)").addClass(".lead");
const pageTitleArea = m("div")
  .append(pageTitle, pageSubtitle)
  .addClass("text-center");

const AppAlert = MJBS.createAlert();

const FormAlert_AddProject = MJBS.createAlert();
const ProjectPathInput = MJBS.createInput("text", "required");
const AddProjectBtn = MJBS.createButton("Add", "primary", 'submit');

const Form_AddProject = cc('form', {
  attr: {autocomplete: 'off'},
  children: [
    m('div')
      .addClass('input-group input-group-lg')
      .append(
        // label
        m('span').addClass('input-group-text').text('Project Path'),

        // text input
        m(ProjectPathInput).addClass('form-control'),

        // submit button
        m(AddProjectBtn).on('click', event => {
          event.preventDefault();
          const path = MJBS.valOf(ProjectPathInput, 'trim');
          if (!path) {
            FormAlert_AddProject.insert("warning", "必須填寫項目地址");
            MJBS.focus(ProjectPathInput);
            return;
          }
          axiosPost({
            url: '/api/add-project',
            body: {path: path},
            alert: FormAlert_AddProject,
            onSuccess: (resp) => {
              const project = resp.data;
              FormAlert_AddProject.insert(
                'success',
                `成功添加項目 id: ${project.id}, path: ${project.path}`
              );
              ProjectPathInput.elem().val('');
            }
          });
        })
      )
  ]
});

const FormArea_AddProject = cc('div', {
  children: [
    m(Form_AddProject),
    m(FormAlert_AddProject).addClass('my-1')
  ]
});

$("#root").append(
  pageTitleArea.addClass("my-5"),
  m(AppAlert).addClass("my-3"),
  m(FormArea_AddProject).addClass('my-3')
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
        MJBS.focus(ProjectPathInput);
      }
    },
  });
}
