#!/usr/bin/env node
"use strict";

const fs = require("fs");
const os = require("os");
const path = require("path");

const skillName = "neospark-imagegen-cli";
const home = os.homedir();

const bundledSkills = path.join(__dirname, "skills");

const agents = {
  claude: {
    label: "Claude Code",
    bundled: path.join(bundledSkills, "claude", skillName),
    target: path.join(home, ".claude", "skills", skillName),
  },
  codex: {
    label: "Codex",
    bundled: path.join(bundledSkills, "codex", skillName),
    target: path.join(home, ".codex", "skills", skillName),
  },
  openclaw: {
    label: "OpenClaw",
    bundled: path.join(bundledSkills, "openclaw", skillName),
    target: path.join(home, ".openclaw", "skills", skillName),
  },
};

function printHelp() {
  console.log(`Usage: npx neospark-imagegen-cli-skill [install|uninstall] [options]

Commands:
  install      Install or update the skill for all agents (default)
  uninstall    Remove the skill from all agents

Options:
  --agent, -a  Target one agent: claude | codex | openclaw (default: all)
  --help, -h   Show this help message
`);
}

function parseArgs(argv) {
  const args = { command: "install", agent: null };
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === "--help" || arg === "-h") {
      printHelp();
      process.exit(0);
    }
    if (arg === "--agent" || arg === "-a") {
      args.agent = argv[++i] || null;
      continue;
    }
    if (["install", "uninstall"].includes(arg)) {
      args.command = arg;
      continue;
    }
    if (!arg.startsWith("-")) {
      console.error(`Unknown command: ${arg}`);
      process.exit(1);
    }
  }
  return args;
}

function copyDirectory(source, target) {
  fs.rmSync(target, { recursive: true, force: true });
  fs.cpSync(source, target, { recursive: true, dereference: true });
}

function install(agentKey) {
  const agent = agents[agentKey];
  if (!fs.existsSync(agent.bundled)) {
    console.warn(`[${agent.label}] Bundled skill not found: ${agent.bundled}`);
    return;
  }
  fs.mkdirSync(path.dirname(agent.target), { recursive: true });
  copyDirectory(agent.bundled, agent.target);
  console.log(`[${agent.label}] Installed: ${agent.target}`);
}

function uninstall(agentKey) {
  const agent = agents[agentKey];
  if (!fs.existsSync(agent.target)) {
    console.log(`[${agent.label}] Not installed.`);
    return;
  }
  fs.rmSync(agent.target, { recursive: true, force: true });
  console.log(`[${agent.label}] Removed: ${agent.target}`);
}

function main() {
  const args = parseArgs(process.argv.slice(2));

  if (args.agent && !agents[args.agent]) {
    console.error(`Unknown agent: ${args.agent}. Choose: claude, codex, openclaw.`);
    process.exit(1);
  }

  const selected = args.agent ? [args.agent] : Object.keys(agents);

  for (const key of selected) {
    if (args.command === "install") {
      install(key);
    } else {
      uninstall(key);
    }
  }

  console.log("\nDone. Restart your agent or reload skills for changes to take effect.");
}

main();
