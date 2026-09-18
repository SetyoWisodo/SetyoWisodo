import { useRef, useEffect, useState, useCallback } from 'react';
import type { FC, ChangeEvent, MouseEvent } from 'react';
import {
  Type,
  Image as ImageIcon,
  Square,
  QrCode,
  Barcode,
  Award,
  ZoomIn,
  ZoomOut,
  Maximize2,
  Eye,
  EyeOff,
} from 'lucide-react';
import type { PackagingStudioState } from '../hooks/usePackagingStudio';
import { PACKAGING_MODELS } from '../utils/packagingModels';
import { drawDielineOverlay, getFaceRegions } from '../utils/dielines';
import { drawBadge, generateBarcodeDataUrl, generateQRCodeDataUrl } from '../utils/qrGenerator';
import type {
  DesignLayer,
  ShapeLayer,
  TextLayer,
  ImageLayer,
  BarcodeLayer,
  QRCodeLayer,
  BadgeLayer,
} from '../types/packaging';

interface DielineEditorProps {
  studio: PackagingStudioState;
  onCanvasRendered?: (canvas: HTMLCanvasElement) => void;
}

// Global image cache for loaded layers
const imageElementCache = new Map<string, HTMLImageElement>();

export const DielineEditor: FC<DielineEditorProps> = ({ studio, onCanvasRendered }) => {
  const {
    currentModelId,
    dimensions,
    backgroundColor,
    layers,
    selectedLayerId,
    setSelectedLayerId,
    updateLayer,
    activeFace,
    setActiveFace,
    showGuides,
    setShowGuides,
    addTextLayer,
    addImageLayer,
    addShapeLayer,
    addBarcodeLayer,
    addQRCodeLayer,
    addBadgeLayer,
  } = studio;

  const modelDef = PACKAGING_MODELS[currentModelId];
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const containerRef = useRef<HTMLDivElement | null>(null);

  // Zoom and Pan
  const [zoom, setZoom] = useState<number>(0.32);
  const [pan, setPan] = useState<{ x: number; y: number }>({ x: 20, y: 20 });
  const [isPanning, setIsPanning] = useState(false);
  const [startPan, setStartPan] = useState<{ x: number; y: number }>({ x: 0, y: 0 });

  // Dragging & Transforming layer
  const [isDraggingLayer, setIsDraggingLayer] = useState(false);
  const [dragStart, setDragStart] = useState<{ mouseX: number; mouseY: number; layerX: number; layerY: number }>({
    mouseX: 0,
    mouseY: 0,
    layerX: 0,
    layerY: 0,
  });

  // Modal / Dropdown menus
  const [showShapeMenu, setShowShapeMenu] = useState(false);
  const [showBadgeMenu, setShowBadgeMenu] = useState(false);
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  // QR & Barcode image cache
  const [generatedUrls, setGeneratedUrls] = useState<Record<string, string>>({});

  // Pre-generate QR code data URLs when layers change
  useEffect(() => {
    layers.forEach((layer) => {
      if (layer.type === 'qrcode') {
        const qrLayer = layer as QRCodeLayer;
        const key = `qr_${qrLayer.id}_${qrLayer.content}_${qrLayer.color}_${qrLayer.bgColor}`;
        if (!generatedUrls[key]) {
          generateQRCodeDataUrl(qrLayer.content, qrLayer.color, qrLayer.bgColor).then((url) => {
            if (url) {
              setGeneratedUrls((prev) => ({ ...prev, [key]: url }));
            }
          });
        }
      } else if (layer.type === 'barcode') {
        const barLayer = layer as BarcodeLayer;
        const key = `bar_${barLayer.id}_${barLayer.code}_${barLayer.color}_${barLayer.bgColor}`;
        if (!generatedUrls[key]) {
          const url = generateBarcodeDataUrl(barLayer.code, barLayer.color, barLayer.bgColor, barLayer.showText);
          setGeneratedUrls((prev) => ({ ...prev, [key]: url }));
        }
      }
    });
  }, [layers, generatedUrls]);

  // Main canvas drawing function
  const renderCanvas = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const W = modelDef.textureWidth;
    const H = modelDef.textureHeight;

    canvas.width = W;
    canvas.height = H;

    // 1. Fill base background color
    ctx.fillStyle = backgroundColor;
    ctx.fillRect(0, 0, W, H);

    // 2. Render all design layers from bottom to top
    layers.forEach((layer) => {
      if (layer.hidden) return;

      ctx.save();
      ctx.globalAlpha = layer.opacity;

      switch (layer.type) {
        case 'text': {
          const textLayer = layer as TextLayer;
          ctx.translate(textLayer.x, textLayer.y);
          if (textLayer.rotation) ctx.rotate((textLayer.rotation * Math.PI) / 180);

          ctx.font = `${textLayer.fontStyle || 'normal'} ${textLayer.fontWeight} ${textLayer.fontSize}px "${textLayer.fontFamily}", sans-serif`;
          ctx.fillStyle = textLayer.color;
          ctx.textAlign = textLayer.textAlign;
          ctx.textBaseline = 'middle';

          // Multi-line support
          const lines = textLayer.text.split('\n');
          const lineH = textLayer.fontSize * (textLayer.lineHeight || 1.2);
          const startY = -((lines.length - 1) * lineH) / 2;

          lines.forEach((line, index) => {
            const curY = startY + index * lineH;
            if (textLayer.strokeWidth && textLayer.strokeColor) {
              ctx.strokeStyle = textLayer.strokeColor;
              ctx.lineWidth = textLayer.strokeWidth;
              ctx.strokeText(line, 0, curY);
            }
            ctx.fillText(line, 0, curY);
          });
          break;
        }

        case 'shape': {
          const shapeLayer = layer as ShapeLayer;
          ctx.translate(shapeLayer.x, shapeLayer.y);
          if (shapeLayer.rotation) ctx.rotate((shapeLayer.rotation * Math.PI) / 180);

          ctx.fillStyle = shapeLayer.fill;
          ctx.strokeStyle = shapeLayer.strokeColor;
          ctx.lineWidth = shapeLayer.strokeWidth || 0;

          const w = shapeLayer.width;
          const h = shapeLayer.height;

          if (shapeLayer.shapeType === 'circle') {
            ctx.beginPath();
            ctx.arc(0, 0, w / 2, 0, Math.PI * 2);
            if (shapeLayer.fill !== 'transparent') ctx.fill();
            if (shapeLayer.strokeWidth) ctx.stroke();
          } else if (shapeLayer.shapeType === 'pill' || shapeLayer.shapeType === 'rect') {
            const r = shapeLayer.shapeType === 'pill' ? Math.min(w, h) / 2 : shapeLayer.borderRadius || 0;
            ctx.beginPath();
            ctx.roundRect(-w / 2, -h / 2, w, h, r);
            if (shapeLayer.fill !== 'transparent') ctx.fill();
            if (shapeLayer.strokeWidth) ctx.stroke();
          } else if (shapeLayer.shapeType === 'line') {
            ctx.beginPath();
            ctx.moveTo(-w / 2, 0);
            ctx.lineTo(w / 2, 0);
            ctx.stroke();
          }
          break;
        }

        case 'image': {
          const imgLayer = layer as ImageLayer;
          ctx.translate(imgLayer.x, imgLayer.y);
          if (imgLayer.rotation) ctx.rotate((imgLayer.rotation * Math.PI) / 180);

          let cachedImg = imageElementCache.get(imgLayer.src);
          if (!cachedImg) {
            cachedImg = new Image();
            cachedImg.crossOrigin = 'anonymous';
            cachedImg.src = imgLayer.src;
            cachedImg.onload = () => {
              imageElementCache.set(imgLayer.src, cachedImg!);
              renderCanvas();
            };
          } else if (cachedImg.complete) {
            ctx.drawImage(cachedImg, -imgLayer.width / 2, -imgLayer.height / 2, imgLayer.width, imgLayer.height);
          }
          break;
        }

        case 'qrcode': {
          const qrLayer = layer as QRCodeLayer;
          const key = `qr_${qrLayer.id}_${qrLayer.content}_${qrLayer.color}_${qrLayer.bgColor}`;
          const qrUrl = generatedUrls[key];
          if (qrUrl) {
            ctx.translate(qrLayer.x, qrLayer.y);
            if (qrLayer.rotation) ctx.rotate((qrLayer.rotation * Math.PI) / 180);

            let cachedImg = imageElementCache.get(qrUrl);
            if (!cachedImg) {
              cachedImg = new Image();
              cachedImg.src = qrUrl;
              cachedImg.onload = () => {
                imageElementCache.set(qrUrl, cachedImg!);
                renderCanvas();
              };
            } else if (cachedImg.complete) {
              ctx.drawImage(cachedImg, -qrLayer.size / 2, -qrLayer.size / 2, qrLayer.size, qrLayer.size);
            }
          }
          break;
        }

        case 'barcode': {
          const barLayer = layer as BarcodeLayer;
          const key = `bar_${barLayer.id}_${barLayer.code}_${barLayer.color}_${barLayer.bgColor}`;
          const barUrl = generatedUrls[key];
          if (barUrl) {
            ctx.translate(barLayer.x, barLayer.y);
            if (barLayer.rotation) ctx.rotate((barLayer.rotation * Math.PI) / 180);

            let cachedImg = imageElementCache.get(barUrl);
            if (!cachedImg) {
              cachedImg = new Image();
              cachedImg.src = barUrl;
              cachedImg.onload = () => {
                imageElementCache.set(barUrl, cachedImg!);
                renderCanvas();
              };
            } else if (cachedImg.complete) {
              ctx.drawImage(cachedImg, -barLayer.width / 2, -barLayer.height / 2, barLayer.width, barLayer.height);
            }
          }
          break;
        }

        case 'badge': {
          const badgeLayer = layer as BadgeLayer;
          drawBadge(ctx, badgeLayer.badgeType, badgeLayer.x, badgeLayer.y, badgeLayer.size, badgeLayer.color, badgeLayer.subText);
          break;
        }
      }

      ctx.restore();
    });

    // 3. Draw Dieline CAD Overlay (Creases, Cuts, Bleed, Dimensions)
    drawDielineOverlay(ctx, currentModelId, W, H, dimensions, showGuides);

    // 4. Draw Selected Layer bounding box & handles
    if (selectedLayerId) {
      const sel = layers.find((l) => l.id === selectedLayerId);
      if (sel) {
        ctx.save();
        ctx.translate(sel.x, sel.y);
        if (sel.rotation) ctx.rotate((sel.rotation * Math.PI) / 180);

        let bW = 100;
        let bH = 50;

        if (sel.type === 'shape') {
          const s = sel as ShapeLayer;
          bW = s.width;
          bH = s.height;
        } else if (sel.type === 'image') {
          const img = sel as ImageLayer;
          bW = img.width;
          bH = img.height;
        } else if (sel.type === 'qrcode') {
          const q = sel as QRCodeLayer;
          bW = q.size;
          bH = q.size;
        } else if (sel.type === 'barcode') {
          const b = sel as BarcodeLayer;
          bW = b.width;
          bH = b.height;
        } else if (sel.type === 'badge') {
          const bg = sel as BadgeLayer;
          bW = bg.size;
          bH = bg.size;
        } else if (sel.type === 'text') {
          const t = sel as TextLayer;
          ctx.font = `${t.fontWeight} ${t.fontSize}px "${t.fontFamily}", sans-serif`;
          const lines = t.text.split('\n');
          const maxLineWidth = Math.max(...lines.map((l) => ctx.measureText(l).width));
          bW = maxLineWidth + 24;
          bH = lines.length * t.fontSize * (t.lineHeight || 1.2) + 16;
        }

        // Bounding box dashed stroke
        ctx.strokeStyle = '#6366f1';
        ctx.lineWidth = 2;
        ctx.setLineDash([6, 4]);
        ctx.strokeRect(-bW / 2 - 4, -bH / 2 - 4, bW + 8, bH + 8);

        // Corner handles
        ctx.setLineDash([]);
        ctx.fillStyle = '#ffffff';
        ctx.strokeStyle = '#6366f1';
        ctx.lineWidth = 2;
        const handleSize = 8;
        const corners = [
          [-bW / 2 - 4, -bH / 2 - 4],
          [bW / 2 + 4, -bH / 2 - 4],
          [bW / 2 + 4, bH / 2 + 4],
          [-bW / 2 - 4, bH / 2 + 4],
        ];
        corners.forEach(([hx, hy]) => {
          ctx.fillRect(hx - handleSize / 2, hy - handleSize / 2, handleSize, handleSize);
          ctx.strokeRect(hx - handleSize / 2, hy - handleSize / 2, handleSize, handleSize);
        });

        ctx.restore();
      }
    }

    // Notify 3D viewport of the rendered canvas
    if (onCanvasRendered) {
      onCanvasRendered(canvas);
    }
  }, [
    backgroundColor,
    currentModelId,
    dimensions,
    generatedUrls,
    layers,
    modelDef.textureHeight,
    modelDef.textureWidth,
    onCanvasRendered,
    selectedLayerId,
    showGuides,
  ]);

  // Re-render when dependencies change
  useEffect(() => {
    renderCanvas();
  }, [renderCanvas]);

  // Handle image upload from file picker
  const handleFileUpload = (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (event) => {
      const src = event.target?.result as string;
      const img = new Image();
      img.src = src;
      img.onload = () => {
        addImageLayer(src, img.naturalWidth, img.naturalHeight);
      };
    };
    reader.readAsDataURL(file);
    e.target.value = '';
  };

  // Convert mouse screen coordinates to canvas coordinate space
  const getCanvasCoords = (clientX: number, clientY: number) => {
    if (!canvasRef.current) return { x: 0, y: 0 };
    const rect = canvasRef.current.getBoundingClientRect();
    const scaleX = modelDef.textureWidth / rect.width;
    const scaleY = modelDef.textureHeight / rect.height;
    return {
      x: (clientX - rect.left) * scaleX,
      y: (clientY - rect.top) * scaleY,
    };
  };

  // Canvas Mouse Down: Select layer or start drag
  const handleMouseDown = (e: MouseEvent) => {
    if (e.button === 1 || e.altKey) {
      // Middle click or Alt + Drag to pan
      setIsPanning(true);
      setStartPan({ x: e.clientX - pan.x, y: e.clientY - pan.y });
      return;
    }

    const { x, y } = getCanvasCoords(e.clientX, e.clientY);

    // Hit test layers from top to bottom
    let hitLayer: DesignLayer | null = null;
    for (let i = layers.length - 1; i >= 0; i--) {
      const layer = layers[i];
      if (layer.hidden) continue;

      // Approximate distance check
      const dist = Math.hypot(layer.x - x, layer.y - y);
      const hitRadius = layer.type === 'badge' ? 70 : layer.type === 'text' ? 120 : 160;

      if (dist < hitRadius) {
        hitLayer = layer;
        break;
      }
    }

    if (hitLayer) {
      setSelectedLayerId(hitLayer.id);
      setIsDraggingLayer(true);
      setDragStart({
        mouseX: x,
        mouseY: y,
        layerX: hitLayer.x,
        layerY: hitLayer.y,
      });
    } else {
      setSelectedLayerId(null);
    }
  };

  const handleMouseMove = (e: MouseEvent) => {
    if (isPanning) {
      setPan({
        x: e.clientX - startPan.x,
        y: e.clientY - startPan.y,
      });
      return;
    }

    if (isDraggingLayer && selectedLayerId) {
      const { x, y } = getCanvasCoords(e.clientX, e.clientY);
      const deltaX = x - dragStart.mouseX;
      const deltaY = y - dragStart.mouseY;
      updateLayer(selectedLayerId, {
        x: Math.round(dragStart.layerX + deltaX),
        y: Math.round(dragStart.layerY + deltaY),
      });
    }
  };

  const handleMouseUp = () => {
    setIsPanning(false);
    setIsDraggingLayer(false);
  };

  // Focus into a specific face panel
  const handleFocusFace = (faceId: string) => {
    setActiveFace(faceId as any);
    const regions = getFaceRegions(currentModelId, modelDef.textureWidth, modelDef.textureHeight);
    const region = regions.find((r) => r.id === faceId);

    if (region && containerRef.current) {
      const contW = containerRef.current.clientWidth;
      const contH = containerRef.current.clientHeight;
      const targetZoom = Math.min(contW / region.width, contH / region.height) * 0.7;
      setZoom(targetZoom);
      setPan({
        x: contW / 2 - (region.x + region.width / 2) * targetZoom,
        y: contH / 2 - (region.y + region.height / 2) * targetZoom,
      });
    } else {
      // Reset to full dieline
      setZoom(0.32);
      setPan({ x: 30, y: 30 });
    }
  };

  return (
    <div className="relative w-full h-full flex flex-col bg-[#11141d] overflow-hidden select-none">
      {/* 2D Canvas Top Toolbar */}
      <div className="h-12 border-b border-slate-800 bg-[#161a26] px-3 flex items-center justify-between text-xs z-10 shrink-0">
        <div className="flex items-center space-x-1.5 overflow-x-auto py-1">
          {/* Add Text */}
          <button
            onClick={() => addTextLayer('LOGO MERK')}
            className="flex items-center space-x-1.5 px-2.5 py-1.5 rounded-md bg-slate-800 hover:bg-slate-700 text-slate-200 hover:text-white transition shadow-sm font-medium border border-slate-700/60"
            title="Tambah Teks"
          >
            <Type className="w-3.5 h-3.5 text-indigo-400" />
            <span>Teks</span>
          </button>

          {/* Upload Image */}
          <button
            onClick={() => fileInputRef.current?.click()}
            className="flex items-center space-x-1.5 px-2.5 py-1.5 rounded-md bg-slate-800 hover:bg-slate-700 text-slate-200 hover:text-white transition shadow-sm font-medium border border-slate-700/60"
            title="Unggah Gambar / Logo"
          >
            <ImageIcon className="w-3.5 h-3.5 text-emerald-400" />
            <span>Logo / Gambar</span>
          </button>
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileUpload}
            accept="image/*"
            className="hidden"
          />

          {/* Shapes Dropdown */}
          <div className="relative">
            <button
              onClick={() => {
                setShowShapeMenu(!showShapeMenu);
                setShowBadgeMenu(false);
              }}
              className="flex items-center space-x-1.5 px-2.5 py-1.5 rounded-md bg-slate-800 hover:bg-slate-700 text-slate-200 hover:text-white transition shadow-sm font-medium border border-slate-700/60"
            >
              <Square className="w-3.5 h-3.5 text-amber-400" />
              <span>Bentuk</span>
            </button>
            {showShapeMenu && (
              <div className="absolute top-full left-0 mt-1 w-36 bg-[#1a1f2e] border border-slate-700 rounded-lg shadow-xl py-1 z-30">
                <button
                  onClick={() => {
                    addShapeLayer('rect');
                    setShowShapeMenu(false);
                  }}
                  className="w-full text-left px-3 py-1.5 hover:bg-indigo-600/20 text-slate-200 hover:text-indigo-400 transition"
                >
                  Persegi
                </button>
                <button
                  onClick={() => {
                    addShapeLayer('circle');
                    setShowShapeMenu(false);
                  }}
                  className="w-full text-left px-3 py-1.5 hover:bg-indigo-600/20 text-slate-200 hover:text-indigo-400 transition"
                >
                  Lingkaran
                </button>
                <button
                  onClick={() => {
                    addShapeLayer('pill');
                    setShowShapeMenu(false);
                  }}
                  className="w-full text-left px-3 py-1.5 hover:bg-indigo-600/20 text-slate-200 hover:text-indigo-400 transition"
                >
                  Kapsul / Pill
                </button>
                <button
                  onClick={() => {
                    addShapeLayer('line');
                    setShowShapeMenu(false);
                  }}
                  className="w-full text-left px-3 py-1.5 hover:bg-indigo-600/20 text-slate-200 hover:text-indigo-400 transition"
                >
                  Garis Pemisah
                </button>
              </div>
            )}
          </div>

          {/* Barcode */}
          <button
            onClick={() => addBarcodeLayer('899723450912')}
            className="flex items-center space-x-1.5 px-2.5 py-1.5 rounded-md bg-slate-800 hover:bg-slate-700 text-slate-200 hover:text-white transition shadow-sm font-medium border border-slate-700/60"
            title="Tambah Barcode EAN-13"
          >
            <Barcode className="w-3.5 h-3.5 text-purple-400" />
            <span>Barcode</span>
          </button>

          {/* QR Code */}
          <button
            onClick={() => addQRCodeLayer('https://pacdora.com')}
            className="flex items-center space-x-1.5 px-2.5 py-1.5 rounded-md bg-slate-800 hover:bg-slate-700 text-slate-200 hover:text-white transition shadow-sm font-medium border border-slate-700/60"
            title="Tambah QR Code"
          >
            <QrCode className="w-3.5 h-3.5 text-sky-400" />
            <span>QR Code</span>
          </button>

          {/* Packaging Badges & Seals */}
          <div className="relative">
            <button
              onClick={() => {
                setShowBadgeMenu(!showBadgeMenu);
                setShowShapeMenu(false);
              }}
              className="flex items-center space-x-1.5 px-2.5 py-1.5 rounded-md bg-slate-800 hover:bg-slate-700 text-slate-200 hover:text-white transition shadow-sm font-medium border border-slate-700/60"
            >
              <Award className="w-3.5 h-3.5 text-rose-400" />
              <span>Stempel</span>
            </button>
            {showBadgeMenu && (
              <div className="absolute top-full left-0 mt-1 w-44 bg-[#1a1f2e] border border-slate-700 rounded-lg shadow-xl py-1 z-30">
                <button
                  onClick={() => {
                    addBadgeLayer('recyclable');
                    setShowBadgeMenu(false);
                  }}
                  className="w-full text-left px-3 py-1.5 hover:bg-indigo-600/20 text-slate-200 hover:text-indigo-400 transition"
                >
                  ♻️ 100% Recyclable
                </button>
                <button
                  onClick={() => {
                    addBadgeLayer('organic');
                    setShowBadgeMenu(false);
                  }}
                  className="w-full text-left px-3 py-1.5 hover:bg-indigo-600/20 text-slate-200 hover:text-indigo-400 transition"
                >
                  🌿 Certified Organic
                </button>
                <button
                  onClick={() => {
                    addBadgeLayer('halal');
                    setShowBadgeMenu(false);
                  }}
                  className="w-full text-left px-3 py-1.5 hover:bg-indigo-600/20 text-slate-200 hover:text-indigo-400 transition"
                >
                  🕌 Halal Indonesia
                </button>
                <button
                  onClick={() => {
                    addBadgeLayer('cruelty_free');
                    setShowBadgeMenu(false);
                  }}
                  className="w-full text-left px-3 py-1.5 hover:bg-indigo-600/20 text-slate-200 hover:text-indigo-400 transition"
                >
                  🐇 Cruelty Free
                </button>
                <button
                  onClick={() => {
                    addBadgeLayer('fsc');
                    setShowBadgeMenu(false);
                  }}
                  className="w-full text-left px-3 py-1.5 hover:bg-indigo-600/20 text-slate-200 hover:text-indigo-400 transition"
                >
                  🌲 FSC Paper Mix
                </button>
                <button
                  onClick={() => {
                    addBadgeLayer('net_weight');
                    setShowBadgeMenu(false);
                  }}
                  className="w-full text-left px-3 py-1.5 hover:bg-indigo-600/20 text-slate-200 hover:text-indigo-400 transition"
                >
                  ⚖️ Netto 250g
                </button>
              </div>
            )}
          </div>
        </div>

        {/* View / CAD guides & Zoom controls */}
        <div className="flex items-center space-x-2 shrink-0">
          <button
            onClick={() => setShowGuides(!showGuides)}
            className={`flex items-center space-x-1 px-2.5 py-1.5 rounded-md transition font-medium border ${
              showGuides
                ? 'bg-indigo-600/20 border-indigo-500/50 text-indigo-400'
                : 'bg-slate-800 border-slate-700/60 text-slate-400 hover:text-white'
            }`}
            title="Tampilkan / Sembunyikan Garis CAD Dieline"
          >
            {showGuides ? <Eye className="w-3.5 h-3.5" /> : <EyeOff className="w-3.5 h-3.5" />}
            <span className="hidden sm:inline">Garis Dieline</span>
          </button>

          <div className="h-4 w-px bg-slate-700/80" />

          <button
            onClick={() => setZoom((z) => Math.max(0.1, z - 0.05))}
            className="p-1.5 rounded bg-slate-800 hover:bg-slate-700 text-slate-300"
            title="Perkecil"
          >
            <ZoomOut className="w-3.5 h-3.5" />
          </button>
          <span className="text-[11px] font-mono text-slate-400 w-9 text-center">
            {Math.round(zoom * 100)}%
          </span>
          <button
            onClick={() => setZoom((z) => Math.min(1.2, z + 0.05))}
            className="p-1.5 rounded bg-slate-800 hover:bg-slate-700 text-slate-300"
            title="Perbesar"
          >
            <ZoomIn className="w-3.5 h-3.5" />
          </button>
          <button
            onClick={() => {
              setZoom(0.32);
              setPan({ x: 20, y: 20 });
            }}
            className="p-1.5 rounded bg-slate-800 hover:bg-slate-700 text-slate-300"
            title="Reset Zoom"
          >
            <Maximize2 className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>

      {/* Face Panel Quick Selector Bar */}
      <div className="h-8 border-b border-slate-800/80 bg-[#131620] px-3 flex items-center space-x-1 overflow-x-auto text-[11px] shrink-0">
        <span className="text-slate-400 font-medium mr-1 uppercase text-[10px] tracking-wider">Fokus Sisi:</span>
        {modelDef.availableFaces.map((f) => (
          <button
            key={f.id}
            onClick={() => handleFocusFace(f.id)}
            className={`px-2.5 py-0.5 rounded transition ${
              activeFace === f.id
                ? 'bg-indigo-600 text-white font-medium shadow-sm'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'
            }`}
          >
            {f.name}
          </button>
        ))}
      </div>

      {/* Main Interactive Canvas Workspace with checkerboard background */}
      <div
        ref={containerRef}
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onMouseLeave={handleMouseUp}
        className="flex-1 relative overflow-hidden checkerboard-bg cursor-crosshair flex items-center justify-center"
      >
        <div
          style={{
            transform: `translate(${pan.x}px, ${pan.y}px) scale(${zoom})`,
            transformOrigin: '0 0',
            transition: isPanning || isDraggingLayer ? 'none' : 'transform 0.15s ease-out',
          }}
          className="relative shadow-2xl border border-slate-700/60 rounded"
        >
          <canvas
            ref={canvasRef}
            className="block"
          />
        </div>

        {/* Floating Canvas Info Tag */}
        <div className="absolute bottom-3 right-3 bg-slate-900/80 backdrop-blur-md border border-slate-800 px-3 py-1.5 rounded-lg text-[11px] text-slate-400 flex items-center space-x-3 pointer-events-none">
          <span>Resolusi: {modelDef.textureWidth} × {modelDef.textureHeight} px</span>
          <span className="w-px h-3 bg-slate-700" />
          <span>Geser mouse untuk atur posisi elemen</span>
        </div>
      </div>
    </div>
  );
};
