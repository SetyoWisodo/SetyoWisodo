import * as THREE from 'three';
import type { MaterialType } from '../types/packaging';

// Cache generated procedural textures to avoid recalculation
const textureCache: Record<string, THREE.CanvasTexture> = {};

/**
 * Creates procedural kraft paper texture with fibers and noise
 */
export function createKraftTexture(isWhite: boolean = false): THREE.CanvasTexture {
  const cacheKey = isWhite ? 'kraft_white' : 'kraft_brown';
  if (textureCache[cacheKey]) return textureCache[cacheKey];

  const canvas = document.createElement('canvas');
  canvas.width = 512;
  canvas.height = 512;
  const ctx = canvas.getContext('2d')!;

  // Base paper color
  ctx.fillStyle = isWhite ? '#f8f6f0' : '#d8b688';
  ctx.fillRect(0, 0, 512, 512);

  // Subtle noise
  const imgData = ctx.getImageData(0, 0, 512, 512);
  const data = imgData.data;
  for (let i = 0; i < data.length; i += 4) {
    const noise = (Math.random() - 0.5) * (isWhite ? 12 : 25);
    data[i] = Math.min(255, Math.max(0, data[i] + noise));
    data[i + 1] = Math.min(255, Math.max(0, data[i + 1] + noise * 0.9));
    data[i + 2] = Math.min(255, Math.max(0, data[i + 2] + noise * 0.7));
  }
  ctx.putImageData(imgData, 0, 0);

  // Paper fibers
  ctx.strokeStyle = isWhite ? 'rgba(180, 175, 160, 0.15)' : 'rgba(120, 85, 45, 0.18)';
  ctx.lineWidth = 1;
  for (let i = 0; i < 400; i++) {
    const x = Math.random() * 512;
    const y = Math.random() * 512;
    const len = 3 + Math.random() * 10;
    const angle = Math.random() * Math.PI * 2;
    ctx.beginPath();
    ctx.moveTo(x, y);
    ctx.lineTo(x + Math.cos(angle) * len, y + Math.sin(angle) * len);
    ctx.stroke();
  }

  const texture = new THREE.CanvasTexture(canvas);
  texture.wrapS = THREE.RepeatWrapping;
  texture.wrapT = THREE.RepeatWrapping;
  texture.repeat.set(4, 4);
  textureCache[cacheKey] = texture;
  return texture;
}

/**
 * Creates condensation droplets bump map for cold cans and bottles
 */
export function createCondensationBumpTexture(): THREE.CanvasTexture {
  if (textureCache['condensation']) return textureCache['condensation'];

  const canvas = document.createElement('canvas');
  canvas.width = 512;
  canvas.height = 512;
  const ctx = canvas.getContext('2d')!;

  ctx.fillStyle = '#808080'; // 50% neutral bump height
  ctx.fillRect(0, 0, 512, 512);

  // Draw random droplets
  for (let i = 0; i < 280; i++) {
    const x = Math.random() * 512;
    const y = Math.random() * 512;
    const r = 2 + Math.random() * 8;

    const grad = ctx.createRadialGradient(x - r * 0.3, y - r * 0.3, 1, x, y, r);
    grad.addColorStop(0, '#ffffff');
    grad.addColorStop(0.7, '#cccccc');
    grad.addColorStop(1, '#808080');

    ctx.fillStyle = grad;
    ctx.beginPath();
    ctx.arc(x, y, r, 0, Math.PI * 2);
    ctx.fill();
  }

  const texture = new THREE.CanvasTexture(canvas);
  texture.wrapS = THREE.RepeatWrapping;
  texture.wrapT = THREE.RepeatWrapping;
  texture.repeat.set(3, 3);
  textureCache['condensation'] = texture;
  return texture;
}

/**
 * Configures MeshPhysicalMaterial properties based on packaging material type
 */
export function applyMaterialProperties(
  material: THREE.MeshPhysicalMaterial,
  type: MaterialType,
  hasCondensation: boolean = false
) {
  // Default reset
  material.metalness = 0.0;
  material.roughness = 0.3;
  material.clearcoat = 0.0;
  material.clearcoatRoughness = 0.0;
  material.transmission = 0.0;
  material.ior = 1.5;
  material.transparent = false;
  material.opacity = 1.0;
  material.bumpMap = null;
  material.bumpScale = 0.05;

  switch (type) {
    case 'kraft_paper':
      material.roughness = 0.88;
      material.metalness = 0.0;
      material.clearcoat = 0.0;
      material.bumpMap = createKraftTexture(false);
      material.bumpScale = 0.02;
      break;

    case 'kraft_white':
      material.roughness = 0.82;
      material.metalness = 0.0;
      material.clearcoat = 0.0;
      material.bumpMap = createKraftTexture(true);
      material.bumpScale = 0.015;
      break;

    case 'coated_matte':
      material.roughness = 0.42;
      material.metalness = 0.02;
      material.clearcoat = 0.15;
      material.clearcoatRoughness = 0.2;
      break;

    case 'coated_gloss':
      material.roughness = 0.12;
      material.metalness = 0.05;
      material.clearcoat = 0.9;
      material.clearcoatRoughness = 0.05;
      break;

    case 'metallic_foil':
      material.roughness = 0.22;
      material.metalness = 0.85;
      material.clearcoat = 0.4;
      material.clearcoatRoughness = 0.1;
      break;

    case 'glass_clear':
      material.roughness = 0.05;
      material.metalness = 0.0;
      material.transmission = 0.92;
      material.ior = 1.52;
      material.transparent = true;
      material.opacity = 0.85;
      break;

    case 'glass_amber':
      material.roughness = 0.08;
      material.metalness = 0.0;
      material.transmission = 0.82;
      material.ior = 1.54;
      material.color = new THREE.Color('#582c0c');
      material.transparent = true;
      material.opacity = 0.88;
      break;

    case 'plastic_frosted':
      material.roughness = 0.45;
      material.metalness = 0.0;
      material.transmission = 0.65;
      material.ior = 1.45;
      material.transparent = true;
      material.opacity = 0.8;
      break;
  }

  if (hasCondensation) {
    material.bumpMap = createCondensationBumpTexture();
    material.bumpScale = 0.08;
  }

  material.needsUpdate = true;
}
