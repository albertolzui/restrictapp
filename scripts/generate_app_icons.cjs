// Build-time helper only; Sharp is not needed by the deployed Python service.
// npm install --no-save sharp, or set RESTRICTAPP_SHARP_MODULE to its installed path.
const fs = require('node:fs/promises');
const path = require('node:path');
const sharp = require(process.env.RESTRICTAPP_SHARP_MODULE || 'sharp');
(async () => {
  const directory = path.join(__dirname, '../api/static/images');
  // Fill the square so iOS/Android can apply their own home-screen mask.
  // The glyph remains inside the central maskable safe zone.
  const svg = (await fs.readFile(path.join(directory, 'restrictapp-mark.svg'), 'utf8')).replace('rx="19"', 'rx="0"');
  for (const size of [180, 192, 512]) {
    await sharp(Buffer.from(svg), {density: 384}).resize(size,size).png({palette:true, colours:64, effort:10}).toFile(path.join(directory, `app-icon-${size}.png`));
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
