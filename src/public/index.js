const pageTitle = m("h5").text("Local Buckets").addClass("display-5");
const pageSubtitle = m("p")
  .text("本地文件倉庫 (管理文件, 備份文件)")
  .addClass(".lead");
const pageTitleArea = m("div")
  .append(pageTitle, pageSubtitle)
  .addClass("text-center");

const AppAlert = MJBS.createAlert();

function ProjectListItem(project) {
  const self = cc("li", {
    id: `p-${project.id}`,
    classes: "list-group-item d-flex justify-cotent-between align-items-start",
    children: [
      m("div")
        .addClass("ms-2 me-auto")
        .append(
          m("div").text(project.title).addClass("fs-5 fw-bold ProjectTitle"),
          span(project.subtitle).addClass("ProjectSubtitle"),
          span(project.path).addClass("text-muted ProjectPath")
        ),
      span("in use")
        .attr({ title: "當前正在使用中" })
        .addClass("UsingProject badge bg-secondary")
        .css({ cursor: 'default' })
        .hide(),
      span("use").addClass("UseProjectBtn badge bg-primary").hide(),
    ],
  });

  self.init = () => {
    if (project.in_use) {
      self.elem().find(".UsingProject").show();
    } else {
      self.elem().find(".UseProjectBtn").show();
    }
  };
  return self;
}

const ProjectList = cc("ul", { classes: "list-group" });

const FormAlert_AddProject = MJBS.createAlert();
const ProjectPathInput = MJBS.createInput("text", "required");
const AddProjectBtn = MJBS.createButton("Add", "primary", "submit");

const Form_AddProject = cc("form", {
  attr: { autocomplete: "off" },
  children: [
    m("div")
      .addClass("input-group input-group-lg")
      .append(
        // label
        m("span").addClass("input-group-text").text("Project Path"),

        // text input
        m(ProjectPathInput).addClass("form-control"),

        // submit button
        m(AddProjectBtn).on("click", (event) => {
          event.preventDefault();
          const path = MJBS.valOf(ProjectPathInput, "trim");
          if (!path) {
            FormArea_AddProject.show();
            FormAlert_AddProject.insert("warning", "必須填寫項目地址");
            MJBS.focus(ProjectPathInput);
            return;
          }
          axiosPost({
            url: "/api/add-project",
            body: { path: path },
            alert: FormAlert_AddProject,
            onSuccess: (resp) => {
              const project = resp.data;
              FormAlert_AddProject.insert(
                "success",
                `成功添加項目 id: ${project.id}, path: ${project.path}`
              );
              ProjectPathInput.elem().val("");
            },
          });
        })
      ),
  ],
});

const FormArea_AddProject = cc("div", {
  children: [m(Form_AddProject), m(FormAlert_AddProject).addClass("my-1")],
});

$("#root").append(
  pageTitleArea.addClass("my-5"),
  m(AppAlert).addClass("my-3"),
  m(FormArea_AddProject).addClass("my-3").hide(),
  m(ProjectList).addClass("my-5")
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
        MJBS.appendToList(ProjectList, projects.map(ProjectListItem));
      } else {
        AppAlert.insert("info", "尚未註冊項目, 請添加項目.");
        MJBS.focus(ProjectPathInput);
      }
    },
  });
}
