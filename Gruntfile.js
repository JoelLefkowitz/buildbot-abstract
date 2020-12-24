fs = require("fs");
YAML = require("yaml");

function joinListEntries(x) {
  return [x[0], x[1].join(" ")];
}

function joinObjAttrs(x) {
  return Object.fromEntries(Object.entries(x).map(joinListEntries));
}

function parseYaml(x) {
  return YAML.parse(fs.readFileSync(x, "utf8"));
}

module.exports = function (grunt) {
  const execs = joinObjAttrs(parseYaml("routines.yml"));

  grunt.initConfig({
    exec: execs,
    clean: { packages: ["dist", "build", "*.egg-info"] },
  });

  grunt.loadNpmTasks("grunt-exec");
  grunt.loadNpmTasks("grunt-force-task");
  grunt.loadNpmTasks("grunt-contrib-clean");

  for (let name of Object.keys(execs)) {
    ["prettier"].includes(name)
      ? grunt.registerTask(name, "force:exec:" + name)
      : grunt.registerTask(name, "exec:" + name);
  }

  grunt.registerTask("lint", ["cspell", "pylint", "bandit"]);
  grunt.registerTask("format", [
    "presort",
    "black",
    "autoflake",
    "isort",
    "prettier",
    "csscomb",
  ]);
  grunt.registerTask("unitTests", ["pytest"]);
  grunt.registerTask("prebuild", ["lint", "format", "unitTests"]);
  grunt.registerTask("publish", ["clean:packages", "buildPackage", "twine"]);
};
