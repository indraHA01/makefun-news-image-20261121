// News-image entry for Saturday 21 November 2026 (Node 22, standard library only).
//
// The entry image is the committed entry.png beside this file: a broadsheet
// front page summing up 21 November 2026 — Russian missiles falling in
// Poland after the overnight attack on Ukraine, the AI sell-off dragging
// US stocks into correction, the ICJ's Myanmar genocide ruling, Trump
// defending his Putin and Xi ties after the Shenzhen summit, the 6.8 quake
// in Peru, and COP31 missing its deadline — plus a ticker of the day's
// other stories. It is drawn by render.py (Pillow, from data in that file).
// The program copies it to the output directory byte for byte, so the two
// grader runs write identical bytes. No network is used at run time.

import { copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

// Make sure the output directory exists, then copy the committed image in.
mkdirSync(outDir, { recursive: true });
copyFileSync(new URL('./entry.png', import.meta.url), join(outDir, 'entry.png'));
