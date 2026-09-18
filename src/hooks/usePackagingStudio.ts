import { useState, useCallback, useRef } from 'react';
import type {
  CanvasFaceId,
  DesignLayer,
  LightingPreset,
  MaterialType,
  PackagingDimensions,
  PackagingModelId,
  TextLayer,
  ImageLayer,
  ShapeLayer,
  BarcodeLayer,
  QRCodeLayer,
  BadgeLayer,
  BrandPreset,
} from '../types/packaging';
import { PACKAGING_MODELS } from '../utils/packagingModels';
import { BRAND_PRESETS } from '../utils/presets';

export function usePackagingStudio() {
  const initialModel = PACKAGING_MODELS.tuck_box;
  const initialPreset = BRAND_PRESETS[0];

  const [currentModelId, setCurrentModelId] = useState<PackagingModelId>('tuck_box');
  const [dimensions, setDimensions] = useState<PackagingDimensions>({
    ...initialModel.defaultDimensions,
  });
  const [openFactor, setOpenFactor] = useState<number>(0);
  const [material, setMaterial] = useState<MaterialType>(initialPreset.material);
  const [lighting, setLighting] = useState<LightingPreset>(initialPreset.lighting);
  const [hasCondensation, setHasCondensation] = useState<boolean>(false);
  const [showWireframe, setShowWireframe] = useState<boolean>(false);
  const [autoRotate, setAutoRotate] = useState<boolean>(false);
  const [rotationSpeed, setRotationSpeed] = useState<number>(1);
  const [backgroundColor, setBackgroundColor] = useState<string>(initialPreset.backgroundColor);
  const [isTransparentBg, setIsTransparentBg] = useState<boolean>(false);

  // Layers on the 2D dieline canvas
  const [layers, setLayers] = useState<DesignLayer[]>(initialPreset.layers);
  const [selectedLayerId, setSelectedLayerId] = useState<string | null>(initialPreset.layers[1]?.id || null);
  const [activeFace, setActiveFace] = useState<CanvasFaceId>('full_dieline');
  const [showGuides, setShowGuides] = useState<boolean>(true);
  const [viewMode, setViewMode] = useState<'split' | '3d' | '2d'>('split');
  const [activeTab, setActiveTab] = useState<'templates' | 'dimensions' | 'materials' | 'lighting' | 'brand_presets'>('templates');

  // Modals state
  const [isTemplateModalOpen, setIsTemplateModalOpen] = useState(false);
  const [isExportModalOpen, setIsExportModalOpen] = useState(false);

  // Undo / Redo history
  const undoStackRef = useRef<DesignLayer[][]>([]);
  const redoStackRef = useRef<DesignLayer[][]>([]);

  const saveHistory = useCallback((currentLayers: DesignLayer[]) => {
    undoStackRef.current.push(JSON.parse(JSON.stringify(currentLayers)));
    if (undoStackRef.current.length > 25) {
      undoStackRef.current.shift();
    }
    redoStackRef.current = [];
  }, []);

  const undo = useCallback(() => {
    if (undoStackRef.current.length === 0) return;
    const previous = undoStackRef.current.pop()!;
    redoStackRef.current.push(JSON.parse(JSON.stringify(layers)));
    setLayers(previous);
  }, [layers]);

  const redo = useCallback(() => {
    if (redoStackRef.current.length === 0) return;
    const next = redoStackRef.current.pop()!;
    undoStackRef.current.push(JSON.parse(JSON.stringify(layers)));
    setLayers(next);
  }, [layers]);

  // Model change handler
  const setModel = useCallback((modelId: PackagingModelId) => {
    const modelDef = PACKAGING_MODELS[modelId];
    if (!modelDef) return;

    setCurrentModelId(modelId);
    setDimensions({ ...modelDef.defaultDimensions });
    setOpenFactor(0);
    setMaterial(modelDef.defaultMaterial);
    setActiveFace('full_dieline');

    // Find if there is a matching preset for this model
    const preset = BRAND_PRESETS.find((p) => p.modelId === modelId);
    if (preset) {
      setLayers(JSON.parse(JSON.stringify(preset.layers)));
      setBackgroundColor(preset.backgroundColor);
      setMaterial(preset.material);
      setLighting(preset.lighting);
      setSelectedLayerId(preset.layers[0]?.id || null);
    } else {
      // Create minimal default layer
      const defaultText: TextLayer = {
        id: `text_${Date.now()}`,
        name: 'Logo Merk',
        type: 'text',
        text: modelDef.nameEn.toUpperCase(),
        fontFamily: 'Montserrat',
        fontSize: 36,
        fontWeight: '700',
        color: '#ffffff',
        textAlign: 'center',
        letterSpacing: 4,
        lineHeight: 1.2,
        x: modelDef.textureWidth / 2,
        y: modelDef.textureHeight / 2,
        rotation: 0,
        opacity: 1,
      };
      setLayers([defaultText]);
      setSelectedLayerId(defaultText.id);
      setBackgroundColor('#1e293b');
    }
  }, []);

  // Apply Brand Preset
  const applyPreset = useCallback((preset: BrandPreset) => {
    saveHistory(layers);
    setCurrentModelId(preset.modelId);
    if (preset.dimensions) {
      setDimensions(preset.dimensions);
    } else {
      setDimensions({ ...PACKAGING_MODELS[preset.modelId].defaultDimensions });
    }
    setMaterial(preset.material);
    setBackgroundColor(preset.backgroundColor);
    setLighting(preset.lighting);
    setLayers(JSON.parse(JSON.stringify(preset.layers)));
    setSelectedLayerId(preset.layers[0]?.id || null);
    setOpenFactor(0);
  }, [layers, saveHistory]);

  // Layer manipulation methods
  const addTextLayer = useCallback((initialText: string = 'BRAND NAME') => {
    saveHistory(layers);
    const model = PACKAGING_MODELS[currentModelId];
    const newLayer: TextLayer = {
      id: `text_${Date.now()}`,
      name: `Teks ${layers.filter((l) => l.type === 'text').length + 1}`,
      type: 'text',
      text: initialText,
      fontFamily: 'Montserrat',
      fontSize: 36,
      fontWeight: '700',
      color: '#ffffff',
      textAlign: 'center',
      letterSpacing: 2,
      lineHeight: 1.2,
      x: model.textureWidth / 2,
      y: model.textureHeight / 2,
      rotation: 0,
      opacity: 1,
    };
    setLayers((prev) => [...prev, newLayer]);
    setSelectedLayerId(newLayer.id);
  }, [currentModelId, layers, saveHistory]);

  const addImageLayer = useCallback((imageSrc: string, naturalW: number = 300, naturalH: number = 300) => {
    saveHistory(layers);
    const model = PACKAGING_MODELS[currentModelId];
    const maxDim = 400;
    const ratio = naturalW / (naturalH || 1);
    const w = ratio >= 1 ? maxDim : maxDim * ratio;
    const h = ratio >= 1 ? maxDim / ratio : maxDim;

    const newLayer: ImageLayer = {
      id: `image_${Date.now()}`,
      name: `Gambar ${layers.filter((l) => l.type === 'image').length + 1}`,
      type: 'image',
      src: imageSrc,
      width: Math.round(w),
      height: Math.round(h),
      maintainAspectRatio: true,
      x: model.textureWidth / 2,
      y: model.textureHeight / 2,
      rotation: 0,
      opacity: 1,
    };
    setLayers((prev) => [...prev, newLayer]);
    setSelectedLayerId(newLayer.id);
  }, [currentModelId, layers, saveHistory]);

  const addShapeLayer = useCallback((shapeType: ShapeLayer['shapeType'] = 'rect') => {
    saveHistory(layers);
    const model = PACKAGING_MODELS[currentModelId];
    const newLayer: ShapeLayer = {
      id: `shape_${Date.now()}`,
      name: `Bentuk (${shapeType})`,
      type: 'shape',
      shapeType,
      width: shapeType === 'circle' ? 240 : 360,
      height: shapeType === 'circle' ? 240 : 120,
      fill: '#6366f1',
      strokeColor: '#ffffff',
      strokeWidth: 0,
      borderRadius: shapeType === 'pill' ? 60 : 8,
      x: model.textureWidth / 2,
      y: model.textureHeight / 2,
      rotation: 0,
      opacity: 1,
    };
    setLayers((prev) => [...prev, newLayer]);
    setSelectedLayerId(newLayer.id);
  }, [currentModelId, layers, saveHistory]);

  const addBarcodeLayer = useCallback((code: string = '8991234567890') => {
    saveHistory(layers);
    const model = PACKAGING_MODELS[currentModelId];
    const newLayer: BarcodeLayer = {
      id: `barcode_${Date.now()}`,
      name: 'Barcode EAN-13',
      type: 'barcode',
      code,
      width: 260,
      height: 110,
      color: '#0f172a',
      bgColor: '#ffffff',
      showText: true,
      x: model.textureWidth / 2,
      y: model.textureHeight / 2,
      rotation: 0,
      opacity: 1,
    };
    setLayers((prev) => [...prev, newLayer]);
    setSelectedLayerId(newLayer.id);
  }, [currentModelId, layers, saveHistory]);

  const addQRCodeLayer = useCallback(async (content: string = 'https://pacdora.com') => {
    saveHistory(layers);
    const model = PACKAGING_MODELS[currentModelId];
    const newLayer: QRCodeLayer = {
      id: `qr_${Date.now()}`,
      name: 'QR Code',
      type: 'qrcode',
      content,
      size: 140,
      color: '#000000',
      bgColor: '#ffffff',
      x: model.textureWidth / 2,
      y: model.textureHeight / 2,
      rotation: 0,
      opacity: 1,
    };
    setLayers((prev) => [...prev, newLayer]);
    setSelectedLayerId(newLayer.id);
  }, [currentModelId, layers, saveHistory]);

  const addBadgeLayer = useCallback((badgeType: BadgeLayer['badgeType'] = 'recyclable') => {
    saveHistory(layers);
    const model = PACKAGING_MODELS[currentModelId];
    const newLayer: BadgeLayer = {
      id: `badge_${Date.now()}`,
      name: `Stempel ${badgeType.toUpperCase()}`,
      type: 'badge',
      badgeType,
      size: 110,
      color: '#ffffff',
      x: model.textureWidth / 2,
      y: model.textureHeight / 2,
      rotation: 0,
      opacity: 1,
    };
    setLayers((prev) => [...prev, newLayer]);
    setSelectedLayerId(newLayer.id);
  }, [currentModelId, layers, saveHistory]);

  const updateLayer = useCallback((id: string, partial: Partial<DesignLayer>) => {
    setLayers((prev) =>
      prev.map((layer) => {
        if (layer.id === id) {
          return { ...layer, ...partial } as DesignLayer;
        }
        return layer;
      })
    );
  }, []);

  const removeLayer = useCallback((id: string) => {
    saveHistory(layers);
    setLayers((prev) => prev.filter((l) => l.id !== id));
    setSelectedLayerId((prev) => (prev === id ? null : prev));
  }, [layers, saveHistory]);

  const duplicateLayer = useCallback((id: string) => {
    const target = layers.find((l) => l.id === id);
    if (!target) return;
    saveHistory(layers);
    const cloned: DesignLayer = JSON.parse(JSON.stringify(target));
    cloned.id = `${cloned.type}_${Date.now()}`;
    cloned.name = `${cloned.name} (Salinan)`;
    cloned.x += 30;
    cloned.y += 30;
    setLayers((prev) => [...prev, cloned]);
    setSelectedLayerId(cloned.id);
  }, [layers, saveHistory]);

  const reorderLayer = useCallback((id: string, direction: 'up' | 'down' | 'top' | 'bottom') => {
    saveHistory(layers);
    setLayers((prev) => {
      const idx = prev.findIndex((l) => l.id === id);
      if (idx === -1) return prev;
      const copy = [...prev];
      const item = copy.splice(idx, 1)[0];
      if (direction === 'up') {
        const newIdx = Math.min(copy.length, idx + 1);
        copy.splice(newIdx, 0, item);
      } else if (direction === 'down') {
        const newIdx = Math.max(0, idx - 1);
        copy.splice(newIdx, 0, item);
      } else if (direction === 'top') {
        copy.push(item);
      } else if (direction === 'bottom') {
        copy.unshift(item);
      }
      return copy;
    });
  }, [layers, saveHistory]);

  const selectedLayer = layers.find((l) => l.id === selectedLayerId) || null;

  return {
    currentModelId,
    setModel,
    dimensions,
    setDimensions,
    openFactor,
    setOpenFactor,
    material,
    setMaterial,
    lighting,
    setLighting,
    hasCondensation,
    setHasCondensation,
    showWireframe,
    setShowWireframe,
    autoRotate,
    setAutoRotate,
    rotationSpeed,
    setRotationSpeed,
    backgroundColor,
    setBackgroundColor,
    isTransparentBg,
    setIsTransparentBg,
    layers,
    setLayers,
    selectedLayerId,
    setSelectedLayerId,
    selectedLayer,
    activeFace,
    setActiveFace,
    showGuides,
    setShowGuides,
    viewMode,
    setViewMode,
    activeTab,
    setActiveTab,
    isTemplateModalOpen,
    setIsTemplateModalOpen,
    isExportModalOpen,
    setIsExportModalOpen,
    addTextLayer,
    addImageLayer,
    addShapeLayer,
    addBarcodeLayer,
    addQRCodeLayer,
    addBadgeLayer,
    updateLayer,
    removeLayer,
    duplicateLayer,
    reorderLayer,
    applyPreset,
    undo,
    redo,
    canUndo: undoStackRef.current.length > 0,
    canRedo: redoStackRef.current.length > 0,
  };
}

export type PackagingStudioState = ReturnType<typeof usePackagingStudio>;
