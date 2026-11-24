// Jalankan vitest dari path kanonik. Di Windows, cwd "e:\" vs "E:\" membuat Vite memuat
// vitest dua kali ("Cannot read properties of undefined (reading 'config')").
import { spawnSync } from "node:child_process";
import { realpathSync } from "node:fs";
import { join } from "node:path";

const cwd = realpathSync.native(process.cwd());
const bin = join(cwd, "node_modules", "vitest", "vitest.mjs");
const { status } = spawnSync(process.execPath, [bin, ...process.argv.slice(2)], { cwd, stdio: "inherit" });
process.exit(status ?? 1);
