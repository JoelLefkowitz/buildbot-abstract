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
  execs = joinObjAttrs(parseYaml("routines.yml"));

  grunt.initConfig({ exec: execs });
  grunt.loadNpmTasks("grunt-exec");

  for (let name of Object.keys(execs)) {
    grunt.registerTask(name, "exec:" + name);
  }

  grunt.registerTask("lint", ["pylint", "bandit", "cspell", "mypy"]);
  grunt.registerTask("format", [
    "presort",
    "black",
    "autoflake",
    "sort",
    "prettier",
    "csscomb",
  ]);
  grunt.registerTask("unitTests", ["pytest"]);
  grunt.registerTask("prebuild", ["lint", "format", "unitTests"]);
};
