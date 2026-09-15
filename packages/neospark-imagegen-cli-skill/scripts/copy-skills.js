#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");

const packageRoot = path.resolve(__dirname, "..");
const repoRoot = path.resolve(packageRoot, "../..");
const outRoot = path.join(packageRoot, "skills");

const skillName = "neospark-imagegen-cli";

const sources = [
  { agent: "claude", source: path.join(repoRoot, ".claude", "skills", skillName) },
  { agent: "codex", source: path.join(repoRoot, ".codex", "skills", skillName) },
  { agent: "openclaw", source: path.join(repoRoot, "skills", skillName) },
];

function copySkill(mapping) {
  const target = path.join(outRoot, mapping.agent, skillName);
  if (!fs.existsSync(mapping.source)) {
    console.warn(`Source not found: ${mapping.source}`);
    return;
  }
  fs.rmSync(target, { recursive: true, force: true });
  fs.cpSync(mapping.source, target, { recursive: true, dereference: true });
  console.log(`Copied ${mapping.agent}: ${target}`);
}

fs.rmSync(outRoot, { recursive: true, force: true });
for (const mapping of sources) {
  copySkill(mapping);
}
console.log("Skill files ready for packaging.");
