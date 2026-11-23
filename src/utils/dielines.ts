import type { CanvasFaceId, PackagingDimensions, PackagingModelId } from '../types/packaging';

export interface FaceRegion {
  id: CanvasFaceId;
  name: string;
  x: number;
  y: number;
  width: number;
  height: number;
}

export function getFaceRegions(modelId: PackagingModelId, width: number, height: number): FaceRegion[] {
  switch (modelId) {
    case 'mailer_box': {
      // 2048 x 2048
      const boxW = width * 0.44; // 900
      const boxD = height * 0.32; // 655
      const wallH = height * 0.14; // 286
      const cx = (width - boxW) / 2;
      const cy = height * 0.42;

      return [
        { id: 'bottom', name: 'Dasar Kotak (Bawah)', x: cx, y: cy, width: boxW, height: boxD },
        { id: 'lid', name: 'Tutup Atas (Lid Luar)', x: cx, y: cy - boxD - wallH * 0.1, width: boxW, height: boxD },
        { id: 'front', name: 'Sisi Depan', x: cx, y: cy + boxD, width: boxW, height: wallH },
        { id: 'back', name: 'Sisi Belakang', x: cx, y: cy - wallH, width: boxW, height: wallH },
        { id: 'left', name: 'Samping Kiri', x: cx - wallH, y: cy, width: wallH, height: boxD },
        { id: 'right', name: 'Samping Kanan', x: cx + boxW, y: cy, width: wallH, height: boxD },
      ];
    }

    case 'tuck_box': {
      // 4 main panels side by side
      const pW = width * 0.22;
      const pH = height * 0.48;
      const startX = width * 0.04;
      const startY = height * 0.28;

      return [
        { id: 'left', name: 'Samping Kiri', x: startX, y: startY, width: pW, height: pH },
        { id: 'front', name: 'Sisi Depan (Utama)', x: startX + pW, y: startY, width: pW, height: pH },
        { id: 'right', name: 'Samping Kanan', x: startX + pW * 2, y: startY, width: pW, height: pH },
        { id: 'back', name: 'Sisi Belakang', x: startX + pW * 3, y: startY, width: pW, height: pH },
        { id: 'top', name: 'Flap Tutup Atas', x: startX + pW, y: startY - pW * 0.9, width: pW, height: pW * 0.9 },
        { id: 'bottom', name: 'Dasar Bawah', x: startX + pW, y: startY + pH, width: pW, height: pW * 0.9 },
      ];
    }

    case 'beverage_can': {
      return [
        { id: 'full_dieline', name: 'Wrap Melingkar 360°', x: 0, y: 0, width, height },
        { id: 'front', name: 'Tampak Depan Utama', x: width * 0.25, y: height * 0.08, width: width * 0.5, height: height * 0.84 },
        { id: 'back', name: 'Informasi Nutrisi / Barcode', x: width * 0.78, y: height * 0.12, width: width * 0.2, height: height * 0.76 },
      ];
    }

    case 'dropper_bottle': {
      return [
        { id: 'full_dieline', name: 'Label Badan Botol', x: width * 0.05, y: height * 0.1, width: width * 0.9, height: height * 0.8 },
        { id: 'front', name: 'Logo Depan', x: width * 0.28, y: height * 0.12, width: width * 0.44, height: height * 0.76 },
        { id: 'back', name: 'Instruksi Belakang', x: width * 0.74, y: height * 0.15, width: width * 0.2, height: height * 0.7 },
      ];
    }

    case 'standup_pouch': {
      const pW = width * 0.44;
      const pH = height * 0.76;
      return [
        { id: 'front', name: 'Panel Depan', x: width * 0.04, y: height * 0.12, width: pW, height: pH },
        { id: 'back', name: 'Panel Belakang', x: width * 0.52, y: height * 0.12, width: pW, height: pH },
      ];
    }

    case 'paper_cup': {
      return [
        { id: 'full_dieline', name: 'Wrap Cup Kertas', x: width * 0.04, y: height * 0.08, width: width * 0.92, height: height * 0.84 },
        { id: 'front', name: 'Logo Depan', x: width * 0.32, y: height * 0.12, width: width * 0.36, height: height * 0.76 },
      ];
    }

    case 'shopping_bag': {
      const fW = width * 0.34;
      const sW = width * 0.14;
      const pH = height * 0.6;
      const sy = height * 0.2;
      return [
        { id: 'left', name: 'Lipatan Kiri', x: width * 0.02, y: sy, width: sW, height: pH },
        { id: 'front', name: 'Muka Depan', x: width * 0.02 + sW, y: sy, width: fW, height: pH },
        { id: 'right', name: 'Lipatan Kanan', x: width * 0.02 + sW + fW, y: sy, width: sW, height: pH },
        { id: 'back', name: 'Muka Belakang', x: width * 0.02 + sW * 2 + fW, y: sy, width: fW, height: pH },
      ];
    }

    case 'cosmetic_tube': {
      return [
        { id: 'front', name: 'Bagian Depan', x: width * 0.08, y: height * 0.1, width: width * 0.4, height: height * 0.8 },
        { id: 'back', name: 'Bagian Belakang', x: width * 0.52, y: height * 0.1, width: width * 0.4, height: height * 0.8 },
      ];
    }

    case 'cosmetic_jar': {
      return [
        { id: 'top', name: 'Stiker Tutup (Lid)', x: width * 0.1, y: height * 0.15, width: width * 0.35, height: width * 0.35 },
        { id: 'front', name: 'Label Samping Melingkar', x: width * 0.5, y: height * 0.25, width: width * 0.45, height: height * 0.5 },
      ];
    }

    default:
      return [{ id: 'front', name: 'Depan', x: 0, y: 0, width, height }];
  }
}

/**
 * Draws CAD dieline cut, crease, and bleed guidelines on canvas
 */
export function drawDielineOverlay(
  ctx: CanvasRenderingContext2D,
  modelId: PackagingModelId,
  width: number,
  height: number,
  dimensions: PackagingDimensions,
  showGuides: boolean
) {
  if (!showGuides) return;

  const regions = getFaceRegions(modelId, width, height);

  ctx.save();

  // Draw background grid lines (subtle blueprint grid)
  ctx.strokeStyle = 'rgba(255, 255, 255, 0.04)';
  ctx.lineWidth = 1;
  const gridSize = 64;
  for (let x = 0; x < width; x += gridSize) {
    ctx.beginPath();
    ctx.moveTo(x, 0);
    ctx.lineTo(x, height);
    ctx.stroke();
  }
  for (let y = 0; y < height; y += gridSize) {
    ctx.beginPath();
    ctx.moveTo(0, y);
    ctx.lineTo(width, y);
    ctx.stroke();
  }

  // Draw packaging face panels
  regions.forEach((region) => {
    // Fill subtle face highlight
    ctx.fillStyle = 'rgba(99, 102, 241, 0.03)';
    ctx.fillRect(region.x, region.y, region.width, region.height);

    // Crease line (dashed)
    ctx.setLineDash([8, 6]);
    ctx.strokeStyle = 'rgba(56, 189, 248, 0.6)'; // cyan dashed for crease
    ctx.lineWidth = 2;
    ctx.strokeRect(region.x, region.y, region.width, region.height);

    // Face label badge
    ctx.setLineDash([]);
    const badgeText = region.name.toUpperCase();
    ctx.font = 'bold 20px Inter, sans-serif';
    const textWidth = ctx.measureText(badgeText).width;
    const badgePadX = 14;
    const badgeH = 32;

    const badgeX = region.x + (region.width - textWidth - badgePadX * 2) / 2;
    const badgeY = region.y + 16;

    // Badge pill background
    ctx.fillStyle = 'rgba(15, 23, 42, 0.75)';
    ctx.strokeStyle = 'rgba(99, 102, 241, 0.5)';
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.roundRect(badgeX, badgeY, textWidth + badgePadX * 2, badgeH, 16);
    ctx.fill();
    ctx.stroke();

    // Badge text
    ctx.fillStyle = '#93c5fd';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(badgeText, badgeX + (textWidth + badgePadX * 2) / 2, badgeY + badgeH / 2);

    // Cross center marker
    ctx.strokeStyle = 'rgba(99, 102, 241, 0.25)';
    ctx.lineWidth = 1;
    const midX = region.x + region.width / 2;
    const midY = region.y + region.height / 2;
    ctx.beginPath();
    ctx.moveTo(midX - 16, midY);
    ctx.lineTo(midX + 16, midY);
    ctx.moveTo(midX, midY - 16);
    ctx.lineTo(midX, midY + 16);
    ctx.stroke();
  });

  // Legend at bottom left
  ctx.setLineDash([]);
  const legX = 30;
  const legY = height - 50;
  ctx.fillStyle = 'rgba(15, 23, 42, 0.85)';
  ctx.strokeStyle = 'rgba(255, 255, 255, 0.15)';
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.roundRect(legX, legY, 540, 36, 8);
  ctx.fill();
  ctx.stroke();

  ctx.font = '12px Inter, sans-serif';
  ctx.textAlign = 'left';
  ctx.textBaseline = 'middle';

  // Crease legend
  ctx.strokeStyle = '#38bdf8';
  ctx.setLineDash([4, 4]);
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(legX + 15, legY + 18);
  ctx.lineTo(legX + 45, legY + 18);
  ctx.stroke();
  ctx.setLineDash([]);
  ctx.fillStyle = '#cbd5e1';
  ctx.fillText('Garis Lipat (Crease)', legX + 52, legY + 18);

  // Cut line legend
  ctx.strokeStyle = '#ef4444';
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(legX + 190, legY + 18);
  ctx.lineTo(legX + 220, legY + 18);
  ctx.stroke();
  ctx.fillText('Garis Potong (Cut)', legX + 227, legY + 18);

  // Dimensions read-out
  ctx.fillStyle = '#a5b4fc';
  ctx.fillText(
    `Dimensi: ${dimensions.width}×${dimensions.height}×${dimensions.depth}mm`,
    legX + 355,
    legY + 18
  );

  ctx.restore();
}

/**
 * Generate Vector SVG Dieline for professional packaging cutting & printing
 */
export function generateDielineSVG(
  modelId: PackagingModelId,
  dimensions: PackagingDimensions,
  width: number = 2048,
  height: number = 2048
): string {
  const regions = getFaceRegions(modelId, width, height);

  let svgContent = `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${width} ${height}" width="${width}" height="${height}">
  <!-- Dieline Generated by Pacdora 3D Mockup Studio -->
  <!-- Dimensions: ${dimensions.width} x ${dimensions.height} x ${dimensions.depth} mm -->
  <defs>
    <style>
      .cut-line { stroke: #ef4444; stroke-width: 2.5; fill: none; }
      .crease-line { stroke: #0284c7; stroke-width: 2; stroke-dasharray: 8,6; fill: none; }
      .bleed-line { stroke: #10b981; stroke-width: 1.5; stroke-dasharray: 4,4; fill: none; }
      .label-text { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 22px; font-weight: bold; fill: #1e293b; }
      .dim-text { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 16px; fill: #475569; }
    </style>
  </defs>
  <rect width="100%" height="100%" fill="#ffffff" />
`;

  // Draw panels and creases
  regions.forEach((r) => {
    svgContent += `
    <!-- Panel: ${r.name} -->
    <rect class="crease-line" x="${r.x}" y="${r.y}" width="${r.width}" height="${r.height}" />
    <text class="label-text" x="${r.x + r.width / 2}" y="${r.y + 40}" text-anchor="middle">${r.name}</text>
    <text class="dim-text" x="${r.x + r.width / 2}" y="${r.y + r.height - 20}" text-anchor="middle">${Math.round(r.width)}px × ${Math.round(r.height)}px</text>
    `;
  });

  // Perimeter bounding cut line
  const minX = Math.min(...regions.map((r) => r.x)) - 10;
  const minY = Math.min(...regions.map((r) => r.y)) - 10;
  const maxX = Math.max(...regions.map((r) => r.x + r.width)) + 10;
  const maxY = Math.max(...regions.map((r) => r.y + r.height)) + 10;

  svgContent += `
    <!-- Outer Cut Line -->
    <rect class="cut-line" x="${Math.max(10, minX)}" y="${Math.max(10, minY)}" width="${Math.min(width - 20, maxX - minX)}" height="${Math.min(height - 20, maxY - minY)}" rx="8" />
    
    <!-- Header Info -->
    <text class="label-text" x="40" y="50" font-size="28">PACDORA 3D DIELINE SPECIFICATION</text>
    <text class="dim-text" x="40" y="85">Packaging Type: ${modelId} | Size: ${dimensions.width}mm (W) × ${dimensions.height}mm (H) × ${dimensions.depth}mm (D)</text>
    <text class="dim-text" x="40" y="110">Color Code: Red = Outer Cut Line | Blue (Dashed) = Fold / Crease Line</text>
  </svg>`;

  return svgContent;
}
