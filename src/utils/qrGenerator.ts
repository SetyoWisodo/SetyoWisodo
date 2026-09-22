import QRCode from 'qrcode';

/**
 * Generates data URL for dynamic QR code
 */
export async function generateQRCodeDataUrl(
  content: string,
  color: string = '#000000',
  bgColor: string = '#ffffff'
): Promise<string> {
  try {
    return await QRCode.toDataURL(content, {
      width: 512,
      margin: 1,
      color: {
        dark: color,
        light: bgColor,
      },
    });
  } catch (err) {
    console.error('Failed to generate QR Code:', err);
    return '';
  }
}

/**
 * Draws realistic UPC-A / EAN-13 barcode on a canvas and returns data URL
 */
export function generateBarcodeDataUrl(
  code: string = '8991234567890',
  color: string = '#000000',
  bgColor: string = '#ffffff',
  showText: boolean = true
): string {
  const canvas = document.createElement('canvas');
  canvas.width = 400;
  canvas.height = 180;
  const ctx = canvas.getContext('2d')!;

  ctx.fillStyle = bgColor;
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  ctx.fillStyle = color;

  // Pseudo realistic barcode pattern based on string hash
  const totalBars = 65;
  const startX = 30;
  const barWidth = 5;
  const barHeight = showText ? 115 : 140;

  // Quiet zones and guard patterns
  let seed = 0;
  for (let i = 0; i < code.length; i++) {
    seed += code.charCodeAt(i);
  }

  const seededRandom = (s: number) => {
    const x = Math.sin(s++) * 10000;
    return x - Math.floor(x);
  };

  let curX = startX;
  for (let i = 0; i < totalBars; i++) {
    // Guard bars at ends and center
    const isGuard = i < 3 || (i > 30 && i < 34) || i > 61;
    const h = isGuard ? barHeight + 12 : barHeight;
    const isDrawn = isGuard || seededRandom(seed + i) > 0.42;

    if (isDrawn) {
      const w = isGuard ? barWidth * 0.8 : (seededRandom(seed * 2 + i) > 0.65 ? barWidth * 1.5 : barWidth * 0.9);
      ctx.fillRect(curX, 20, w, h);
    }
    curX += barWidth + 0.3;
  }

  if (showText) {
    ctx.font = 'bold 20px "Courier New", monospace';
    ctx.textAlign = 'center';
    ctx.fillStyle = color;
    ctx.fillText(code, canvas.width / 2, 160);
  }

  return canvas.toDataURL('image/png');
}

/**
 * Draws specialized packaging icons & badges
 */
export function drawBadge(
  ctx: CanvasRenderingContext2D,
  type: string,
  x: number,
  y: number,
  size: number,
  color: string,
  subText?: string
) {
  ctx.save();
  ctx.translate(x, y);
  ctx.strokeStyle = color;
  ctx.fillStyle = color;
  ctx.lineWidth = Math.max(2, size * 0.04);
  ctx.lineCap = 'round';
  ctx.lineJoin = 'round';

  const r = size / 2;

  switch (type) {
    case 'recyclable': {
      // 3 chasing arrows (Möbius loop)
      ctx.beginPath();
      ctx.arc(0, 0, r * 0.8, 0, Math.PI * 2);
      ctx.stroke();

      ctx.font = `bold ${Math.round(size * 0.28)}px sans-serif`;
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText('♳', 0, -size * 0.05);

      ctx.font = `bold ${Math.round(size * 0.12)}px sans-serif`;
      ctx.fillText('100% RECYCLED', 0, size * 0.25);
      break;
    }

    case 'organic': {
      // Organic leaf seal
      ctx.beginPath();
      ctx.arc(0, 0, r * 0.85, 0, Math.PI * 2);
      ctx.stroke();

      // Leaf icon
      ctx.beginPath();
      ctx.moveTo(-r * 0.3, r * 0.2);
      ctx.quadraticCurveTo(-r * 0.4, -r * 0.4, r * 0.2, -r * 0.4);
      ctx.quadraticCurveTo(r * 0.4, 0, -r * 0.3, r * 0.2);
      ctx.stroke();

      ctx.font = `bold ${Math.round(size * 0.13)}px sans-serif`;
      ctx.textAlign = 'center';
      ctx.fillText('CERTIFIED', 0, -r * 0.55);
      ctx.fillText('ORGANIC', 0, r * 0.55);
      break;
    }

    case 'halal': {
      // Halal seal
      ctx.beginPath();
      ctx.arc(0, 0, r * 0.85, 0, Math.PI * 2);
      ctx.stroke();

      ctx.font = `bold ${Math.round(size * 0.28)}px sans-serif`;
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText('حلال', 0, -size * 0.04);

      ctx.font = `bold ${Math.round(size * 0.12)}px sans-serif`;
      ctx.fillText('HALAL INDONESIA', 0, size * 0.28);
      break;
    }

    case 'cruelty_free': {
      // Cruelty free bunny icon
      ctx.beginPath();
      ctx.arc(0, 0, r * 0.85, 0, Math.PI * 2);
      ctx.stroke();

      ctx.font = `bold ${Math.round(size * 0.26)}px sans-serif`;
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText('🐇', 0, -size * 0.05);

      ctx.font = `bold ${Math.round(size * 0.12)}px sans-serif`;
      ctx.fillText('CRUELTY FREE', 0, size * 0.25);
      break;
    }

    case 'fsc': {
      // FSC certified paper
      ctx.strokeRect(-r * 0.75, -r * 0.75, r * 1.5, r * 1.5);
      ctx.font = `bold ${Math.round(size * 0.24)}px sans-serif`;
      ctx.textAlign = 'center';
      ctx.fillText('🌲 FSC', 0, 0);
      ctx.font = `${Math.round(size * 0.1)}px sans-serif`;
      ctx.fillText('MIX PAPER', 0, r * 0.4);
      break;
    }

    case 'net_weight': {
      ctx.font = `bold ${Math.round(size * 0.2)}px sans-serif`;
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(`NETTO: ${subText || '250g / 8.8oz'}`, 0, 0);
      ctx.strokeRect(-r * 0.85, -r * 0.35, r * 1.7, r * 0.7);
      break;
    }

    default: {
      // Star badge
      ctx.beginPath();
      ctx.arc(0, 0, r * 0.8, 0, Math.PI * 2);
      ctx.stroke();
      ctx.font = `bold ${Math.round(size * 0.16)}px sans-serif`;
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText('★ 100% ★', 0, -r * 0.1);
      ctx.fillText('PREMIUM', 0, r * 0.25);
      break;
    }
  }

  ctx.restore();
}
