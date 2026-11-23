export type PackagingModelId = 
  | 'mailer_box'
  | 'tuck_box'
  | 'beverage_can'
  | 'dropper_bottle'
  | 'standup_pouch'
  | 'paper_cup'
  | 'shopping_bag'
  | 'cosmetic_tube'
  | 'cosmetic_jar';

export type PackagingCategory = 'boxes' | 'bottles' | 'pouches' | 'cups_tubes';

export type MaterialType = 
  | 'kraft_paper'
  | 'kraft_white'
  | 'coated_matte'
  | 'coated_gloss'
  | 'metallic_foil'
  | 'glass_clear'
  | 'glass_amber'
  | 'plastic_frosted';

export type LightingPreset = 
  | 'studio_minimal'
  | 'warm_commercial'
  | 'dramatic_rim'
  | 'neon_cyber'
  | 'pure_catalog';

export type CanvasFaceId = 
  | 'full_dieline'
  | 'front'
  | 'back'
  | 'top'
  | 'bottom'
  | 'left'
  | 'right'
  | 'lid'
  | 'label';

export interface PackagingDimensions {
  width: number;  // mm
  height: number; // mm
  depth: number;  // mm
  radius?: number; // for cylindrical objects
}

export interface PackagingModelDef {
  id: PackagingModelId;
  name: string;
  nameEn: string;
  category: PackagingCategory;
  categoryName: string;
  description: string;
  thumbnail: string;
  defaultDimensions: PackagingDimensions;
  minDimensions: PackagingDimensions;
  maxDimensions: PackagingDimensions;
  availableFaces: { id: CanvasFaceId; name: string; nameEn: string }[];
  textureWidth: number;
  textureHeight: number;
  hasOpenAnimation: boolean;
  openLabel?: string;
  defaultMaterial: MaterialType;
  allowedMaterials: MaterialType[];
}

export interface LayerBase {
  id: string;
  type: 'text' | 'image' | 'shape' | 'barcode' | 'qrcode' | 'badge';
  name: string;
  x: number; // percentage (0-100) or pixels on dieline
  y: number; // percentage (0-100) or pixels on dieline
  rotation: number; // degrees
  opacity: number; // 0 to 1
  locked?: boolean;
  hidden?: boolean;
  faceTarget?: CanvasFaceId;
}

export interface TextLayer extends LayerBase {
  type: 'text';
  text: string;
  fontFamily: string;
  fontSize: number; // px on 2048 canvas
  fontWeight: '300' | '400' | '500' | '600' | '700' | '800';
  fontStyle?: 'normal' | 'italic';
  color: string;
  textAlign: 'left' | 'center' | 'right';
  letterSpacing: number; // px
  lineHeight: number; // multiple
  strokeColor?: string;
  strokeWidth?: number;
  shadowColor?: string;
  shadowBlur?: number;
}

export interface ImageLayer extends LayerBase {
  type: 'image';
  src: string;
  width: number;
  height: number;
  maintainAspectRatio: boolean;
  blendMode?: 'normal' | 'multiply' | 'screen' | 'overlay';
}

export interface ShapeLayer extends LayerBase {
  type: 'shape';
  shapeType: 'rect' | 'circle' | 'pill' | 'badge_ribbon' | 'line' | 'star' | 'frame';
  width: number;
  height: number;
  fill: string;
  strokeColor: string;
  strokeWidth: number;
  borderRadius?: number;
}

export interface BarcodeLayer extends LayerBase {
  type: 'barcode';
  code: string;
  width: number;
  height: number;
  color: string;
  bgColor: string;
  showText: boolean;
}

export interface QRCodeLayer extends LayerBase {
  type: 'qrcode';
  content: string;
  size: number;
  color: string;
  bgColor: string;
}

export interface BadgeLayer extends LayerBase {
  type: 'badge';
  badgeType: 'recyclable' | 'organic' | 'halal' | 'cruelty_free' | 'fsc' | 'premium' | 'net_weight' | 'barcode_box';
  size: number;
  color: string;
  subText?: string;
}

export type DesignLayer = TextLayer | ImageLayer | ShapeLayer | BarcodeLayer | QRCodeLayer | BadgeLayer;

export interface BrandPreset {
  id: string;
  title: string;
  modelId: PackagingModelId;
  category: string;
  material: MaterialType;
  backgroundColor: string;
  accentColor: string;
  lighting: LightingPreset;
  layers: DesignLayer[];
  dimensions?: PackagingDimensions;
  description: string;
}
