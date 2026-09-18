import { useState, useRef } from 'react';
import type { FC, RefObject } from 'react';
import {
  Upload,
  Sparkles,
  Layers,
  ChevronRight,
  Box,
  MousePointer,
  Hand,
  MessageSquare,
  RotateCcw,
  RotateCw,
  Palette,
  Camera,
} from 'lucide-react';
import type { PackagingStudioState } from '../hooks/usePackagingStudio';
import { PACKAGING_MODELS } from '../utils/packagingModels';
import { Viewport3D } from './Viewport3D';
import type { Viewport3DRef } from './Viewport3D';
import { DielineEditor } from './DielineEditor';
import type { MaterialType } from '../types/packaging';

interface PacdoraEditorProps {
  studio: PackagingStudioState;
  viewportRef: RefObject<Viewport3DRef | null>;
  dielineCanvas: HTMLCanvasElement | null;
  onCanvasRendered: (canvas: HTMLCanvasElement) => void;
  onOpenLibrary: () => void;
}

export const PacdoraEditor: FC<PacdoraEditorProps> = ({
  studio,
  viewportRef,
  dielineCanvas,
  onCanvasRendered,
  onOpenLibrary,
}) => {
  const {
    currentModelId,
    dimensions,
    setDimensions,
    material,
    setMaterial,
    openFactor,
    setOpenFactor,
    undo,
    redo,
    canUndo,
    canRedo,
    setIsExportModalOpen,
    addImageLayer,
  } = studio;

  const currentModel = PACKAGING_MODELS[currentModelId];
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  // Left Ribbon Active Tab
  const [activeRibbon, setActiveRibbon] = useState<'edit' | 'models' | 'layout' | 'background' | 'video' | 'more'>('edit');

  // Popups / Drawers
  const [showMaterialModal, setShowMaterialModal] = useState(false);
  const [showSizeModal, setShowSizeModal] = useState(false);

  // View mode inside editor (3D vs 2D Dieline Net)
  const [displayMode, setDisplayMode] = useState<'3d' | 'net'>('3d');

  // Active cursor tool
  const [activeTool, setActiveTool] = useState<'select' | 'pan'>('select');

  // Handle direct image upload
  const handleUploadClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
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

  const materialNames: Record<MaterialType, string> = {
    kraft_paper: 'Kraft Brown Paper',
    kraft_white: 'Kraft White Paper',
    coated_matte: 'Metal matt / Coated matte',
    coated_gloss: 'Ultra Gloss Laminate',
    metallic_foil: 'Metallic Gold / Chrome',
    glass_clear: 'Clear Glass',
    glass_amber: 'Amber Glass',
    plastic_frosted: 'Frosted Translucent',
  };

  return (
    <div className="flex-1 flex overflow-hidden bg-[#cbd5e1] text-slate-800 font-sans select-none relative">
      {/* ================= 1. LEFT SLIM RIBBON (Screenshot 176) ================= */}
      <aside className="w-18 border-r border-slate-200 bg-white flex flex-col items-center py-4 space-y-5 shrink-0 z-20 shadow-sm">
        {/* Edit Tab (Active purple indicator) */}
        <button
          onClick={() => setActiveRibbon('edit')}
          className={`flex flex-col items-center space-y-1.5 transition ${
            activeRibbon === 'edit'
              ? 'text-purple-600 font-semibold'
              : 'text-slate-400 hover:text-slate-700'
          }`}
        >
          <div
            className={`w-10 h-10 rounded-xl flex items-center justify-center transition ${
              activeRibbon === 'edit'
                ? 'bg-purple-50 text-purple-600 shadow-sm'
                : 'hover:bg-slate-100'
            }`}
          >
            <Sparkles className="w-5 h-5" />
          </div>
          <span className="text-[11px]">Edit</span>
        </button>

        {/* Models Tab (Opens Mockups Library!) */}
        <button
          onClick={() => {
            setActiveRibbon('models');
            onOpenLibrary();
          }}
          className="flex flex-col items-center space-y-1.5 text-slate-400 hover:text-slate-700 transition"
        >
          <div className="w-10 h-10 rounded-xl hover:bg-slate-100 flex items-center justify-center">
            <Box className="w-5 h-5" />
          </div>
          <span className="text-[11px]">Models</span>
        </button>

        {/* Layout Tab (Opens 2D Dieline Graphic Editor) */}
        <button
          onClick={() => {
            setActiveRibbon('layout');
            setDisplayMode(displayMode === 'net' ? '3d' : 'net');
          }}
          className={`flex flex-col items-center space-y-1.5 transition ${
            displayMode === 'net'
              ? 'text-purple-600 font-semibold'
              : 'text-slate-400 hover:text-slate-700'
          }`}
        >
          <div
            className={`w-10 h-10 rounded-xl flex items-center justify-center transition ${
              displayMode === 'net' ? 'bg-purple-50 text-purple-600' : 'hover:bg-slate-100'
            }`}
          >
            <Layers className="w-5 h-5" />
          </div>
          <span className="text-[11px]">Layout</span>
        </button>

        {/* AI Background / Studio Tab */}
        <button
          onClick={() => {
            setActiveRibbon('background');
            setShowMaterialModal(true);
          }}
          className="flex flex-col items-center space-y-1.5 text-slate-400 hover:text-slate-700 transition"
        >
          <div className="w-10 h-10 rounded-xl hover:bg-slate-100 flex items-center justify-center">
            <Palette className="w-5 h-5" />
          </div>
          <span className="text-[11px] text-center leading-tight">AI Backgr...</span>
        </button>

        {/* Video / 360 Turntable Tab */}
        <button
          onClick={() => {
            setActiveRibbon('video');
            setIsExportModalOpen(true);
          }}
          className="flex flex-col items-center space-y-1.5 text-slate-400 hover:text-slate-700 transition"
        >
          <div className="w-10 h-10 rounded-xl hover:bg-slate-100 flex items-center justify-center">
            <Camera className="w-5 h-5" />
          </div>
          <span className="text-[11px]">Video</span>
        </button>
      </aside>

      {/* ================= 2. LEFT TOOL DRAWER (Screenshot 176) ================= */}
      <aside className="w-80 bg-white border-r border-slate-200 flex flex-col h-full shrink-0 p-5 overflow-y-auto space-y-5 z-10 shadow-sm">
        <h2 className="text-base font-bold text-slate-900">Upload images</h2>

        {/* Big Purple Dashed Upload Box (Screenshot 176) */}
        <div className="border-2 border-dashed border-purple-300 rounded-2xl bg-purple-50/40 p-6 flex flex-col items-center justify-center text-center space-y-3 hover:bg-purple-50/70 transition">
          <div className="w-14 h-14 rounded-2xl bg-white shadow-md border border-purple-100 flex items-center justify-center text-purple-600">
            <Upload className="w-7 h-7" />
          </div>

          <button
            onClick={handleUploadClick}
            className="px-6 py-2.5 rounded-xl bg-purple-600 hover:bg-purple-700 text-white font-bold text-xs shadow-md shadow-purple-600/30 transition transform active:scale-95 flex items-center space-x-2"
          >
            <Upload className="w-4 h-4" />
            <span>Upload</span>
          </button>
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileChange}
            accept="image/*"
            className="hidden"
          />

          <span className="text-xs text-slate-400 font-mono">
            {currentModel.textureWidth} × {currentModel.textureHeight} px
          </span>
        </div>

        {/* Custom Material Row (Screenshot 176) */}
        <div
          onClick={() => setShowMaterialModal(true)}
          className="p-3.5 rounded-xl border border-slate-200 hover:border-purple-300 bg-slate-50/50 hover:bg-purple-50/30 cursor-pointer flex items-center justify-between transition group"
        >
          <div>
            <span className="text-[11px] text-slate-400 block">Custom material</span>
            <span className="text-xs font-semibold text-slate-800 group-hover:text-purple-600 transition capitalize">
              {materialNames[material] || material}
            </span>
          </div>
          <ChevronRight className="w-4 h-4 text-slate-400 group-hover:text-purple-600 transition" />
        </div>

        {/* Custom Size Row (Screenshot 176) */}
        <div
          onClick={() => setShowSizeModal(true)}
          className="p-3.5 rounded-xl border border-slate-200 hover:border-purple-300 bg-slate-50/50 hover:bg-purple-50/30 cursor-pointer flex items-center justify-between transition group"
        >
          <div>
            <span className="text-[11px] text-slate-400 block">Custom size</span>
            <span className="text-xs font-semibold text-slate-800 group-hover:text-purple-600 transition font-mono">
              {dimensions.depth || 75} × {dimensions.width || 130} × {dimensions.height || 225} mm
            </span>
          </div>
          <ChevronRight className="w-4 h-4 text-slate-400 group-hover:text-purple-600 transition" />
        </div>

        {/* Find Similar with AI Row (Screenshot 176) */}
        <div
          onClick={onOpenLibrary}
          className="p-3.5 rounded-xl border border-slate-200 hover:border-purple-300 bg-slate-50/50 hover:bg-purple-50/30 cursor-pointer flex items-center justify-between transition group"
        >
          <span className="text-xs font-semibold text-slate-800 group-hover:text-purple-600 transition">
            Find similar with AI
          </span>
          <ChevronRight className="w-4 h-4 text-slate-400 group-hover:text-purple-600 transition" />
        </div>

        {/* Open/Close Lid Slider (for Boxes & Bottles) */}
        {currentModel.hasOpenAnimation && (
          <div className="p-3.5 rounded-xl border border-slate-200 bg-slate-50/50 space-y-2">
            <div className="flex justify-between items-center text-xs">
              <span className="font-semibold text-slate-800">Buka / Tutup Lid</span>
              <span className="font-mono text-purple-600 font-bold">{Math.round(openFactor * 100)}%</span>
            </div>
            <input
              type="range"
              min="0"
              max="1"
              step="0.01"
              value={openFactor}
              onChange={(e) => setOpenFactor(parseFloat(e.target.value))}
              className="w-full h-1.5 bg-slate-200 rounded appearance-none cursor-pointer"
            />
          </div>
        )}

        {/* Model ID Tag (Screenshot 176) */}
        <div className="pt-2">
          <span className="text-[11px] text-slate-400 font-mono">
            Model ID: 604050 • {currentModel.nameEn}
          </span>
        </div>
      </aside>

      {/* ================= 3. CENTRAL 3D VIEWPORT / 2D NET ================= */}
      <main className="flex-1 relative overflow-hidden bg-[#e2e8f0] flex items-center justify-center">
        {displayMode === '3d' ? (
          <div className="w-full h-full relative">
            <Viewport3D
              ref={viewportRef}
              studio={studio}
              dielineCanvas={dielineCanvas}
            />

            {/* Bottom Floating Control Bar (Screenshot 176) */}
            <div className="absolute bottom-5 left-1/2 -translate-x-1/2 flex items-center space-x-3 pointer-events-auto z-10">
              {/* Zoom & View Toggles */}
              <div className="bg-white/95 backdrop-blur shadow-xl border border-slate-200/80 rounded-2xl px-3 py-1.5 flex items-center space-x-3 text-slate-700">
                <button
                  onClick={() => {}}
                  className="p-1.5 hover:bg-slate-100 rounded-lg text-slate-600 font-bold text-sm"
                  title="Zoom Out"
                >
                  −
                </button>
                <div className="h-4 w-px bg-slate-200" />
                <button
                  onClick={() => {}}
                  className="p-1.5 hover:bg-slate-100 rounded-lg text-slate-600 font-bold text-sm"
                  title="Zoom In"
                >
                  +
                </button>
                <div className="h-4 w-px bg-slate-200" />

                {/* 3D Box view icon */}
                <button
                  onClick={() => setDisplayMode('3d')}
                  className={`p-1.5 rounded-lg transition ${
                    displayMode === '3d' ? 'bg-purple-100 text-purple-600 font-bold' : 'hover:bg-slate-100'
                  }`}
                  title="3D View"
                >
                  <Box className="w-4 h-4" />
                </button>

                {/* 2D Net Dieline icon */}
                <button
                  onClick={() => setDisplayMode('net')}
                  className="p-1.5 rounded-lg hover:bg-slate-100 transition"
                  title="2D Dieline Net View"
                >
                  <Layers className="w-4 h-4" />
                </button>
              </div>

              {/* Watermark Free Gold Crown Badge (Screenshot 176) */}
              <div className="bg-white/95 backdrop-blur shadow-xl border border-slate-200/80 rounded-2xl px-3.5 py-2 flex items-center space-x-1.5 text-xs font-semibold text-slate-800">
                <span className="text-amber-500">👑</span>
                <span>Watermark free</span>
              </div>
            </div>
          </div>
        ) : (
          /* 2D Flat Dieline Editor */
          <div className="w-full h-full relative">
            <DielineEditor
              studio={studio}
              onCanvasRendered={onCanvasRendered}
            />

            {/* Back to 3D Button */}
            <button
              onClick={() => setDisplayMode('3d')}
              className="absolute top-4 right-4 px-4 py-2 rounded-xl bg-purple-600 text-white font-semibold text-xs shadow-lg transition"
            >
              ← Back to 3D View
            </button>
          </div>
        )}
      </main>

      {/* ================= 4. RIGHT FLOATING TOOLBAR (Screenshot 176) ================= */}
      <div className="absolute right-4 top-20 flex flex-col space-y-2 bg-white/95 backdrop-blur shadow-xl border border-slate-200/80 rounded-2xl p-1.5 z-20 text-slate-600">
        <button
          onClick={() => setActiveTool('select')}
          className={`p-2 rounded-xl transition ${
            activeTool === 'select' ? 'bg-purple-50 text-purple-600 font-bold' : 'hover:bg-slate-100'
          }`}
          title="Select tool"
        >
          <MousePointer className="w-4 h-4" />
        </button>

        <button
          onClick={() => setActiveTool('pan')}
          className={`p-2 rounded-xl transition ${
            activeTool === 'pan' ? 'bg-purple-50 text-purple-600 font-bold' : 'hover:bg-slate-100'
          }`}
          title="Pan hand tool"
        >
          <Hand className="w-4 h-4" />
        </button>

        <button
          onClick={() => {}}
          className="p-2 rounded-xl hover:bg-slate-100 transition"
          title="Comment"
        >
          <MessageSquare className="w-4 h-4" />
        </button>

        <div className="w-full h-px bg-slate-200" />

        <button
          onClick={undo}
          disabled={!canUndo}
          className={`p-2 rounded-xl transition ${
            canUndo ? 'hover:bg-slate-100 text-slate-700' : 'text-slate-300 cursor-not-allowed'
          }`}
          title="Undo"
        >
          <RotateCcw className="w-4 h-4" />
        </button>

        <button
          onClick={redo}
          disabled={!canRedo}
          className={`p-2 rounded-xl transition ${
            canRedo ? 'hover:bg-slate-100 text-slate-700' : 'text-slate-300 cursor-not-allowed'
          }`}
          title="Redo"
        >
          <RotateCw className="w-4 h-4" />
        </button>
      </div>

      {/* ================= 5. POPUP MODALS: MATERIAL & SIZE ================= */}
      {showMaterialModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
          <div className="bg-white rounded-2xl w-full max-w-md p-6 shadow-2xl space-y-4">
            <div className="flex justify-between items-center border-b pb-3">
              <h3 className="font-bold text-sm text-slate-900">Custom Material Finish</h3>
              <button
                onClick={() => setShowMaterialModal(false)}
                className="text-slate-400 hover:text-slate-700 font-bold"
              >
                ✕
              </button>
            </div>

            <div className="space-y-2">
              {[
                { id: 'coated_matte', label: 'Metal matt / Coated Matte', desc: 'Doff anti-glare finish' },
                { id: 'kraft_paper', label: 'Kraft Brown Paper', desc: 'Natural corrugated fiber' },
                { id: 'coated_gloss', label: 'Ultra Gloss UV', desc: 'High reflection gloss' },
                { id: 'metallic_foil', label: 'Metallic Gold / Chrome', desc: 'Foil metallic sheen' },
                { id: 'glass_amber', label: 'Amber Glass', desc: 'Brown apothecary serum bottle' },
                { id: 'plastic_frosted', label: 'Frosted Translucent', desc: 'Matte frosted plastic' },
              ].map((m) => (
                <button
                  key={m.id}
                  onClick={() => {
                    setMaterial(m.id as any);
                    setShowMaterialModal(false);
                  }}
                  className={`w-full text-left p-3 rounded-xl border transition ${
                    material === m.id
                      ? 'border-purple-500 bg-purple-50/60 font-semibold text-purple-700'
                      : 'border-slate-200 hover:bg-slate-50 text-slate-700'
                  }`}
                >
                  <div className="text-xs font-semibold">{m.label}</div>
                  <div className="text-[11px] text-slate-400">{m.desc}</div>
                </button>
              ))}
            </div>
          </div>
        </div>
      )}

      {showSizeModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
          <div className="bg-white rounded-2xl w-full max-w-md p-6 shadow-2xl space-y-4">
            <div className="flex justify-between items-center border-b pb-3">
              <h3 className="font-bold text-sm text-slate-900">Custom Packaging Size (mm)</h3>
              <button
                onClick={() => setShowSizeModal(false)}
                className="text-slate-400 hover:text-slate-700 font-bold"
              >
                ✕
              </button>
            </div>

            <div className="space-y-4">
              <div className="space-y-1">
                <div className="flex justify-between text-xs font-medium">
                  <span>Width (Lebar)</span>
                  <span className="font-mono text-purple-600">{dimensions.width} mm</span>
                </div>
                <input
                  type="range"
                  min="50"
                  max="300"
                  value={dimensions.width}
                  onChange={(e) =>
                    setDimensions((prev) => ({ ...prev, width: parseInt(e.target.value) }))
                  }
                  className="w-full h-1.5 bg-slate-200 rounded appearance-none cursor-pointer"
                />
              </div>

              <div className="space-y-1">
                <div className="flex justify-between text-xs font-medium">
                  <span>Height (Tinggi)</span>
                  <span className="font-mono text-purple-600">{dimensions.height} mm</span>
                </div>
                <input
                  type="range"
                  min="60"
                  max="350"
                  value={dimensions.height}
                  onChange={(e) =>
                    setDimensions((prev) => ({ ...prev, height: parseInt(e.target.value) }))
                  }
                  className="w-full h-1.5 bg-slate-200 rounded appearance-none cursor-pointer"
                />
              </div>

              <div className="space-y-1">
                <div className="flex justify-between text-xs font-medium">
                  <span>Depth (Tebal)</span>
                  <span className="font-mono text-purple-600">{dimensions.depth} mm</span>
                </div>
                <input
                  type="range"
                  min="30"
                  max="200"
                  value={dimensions.depth}
                  onChange={(e) =>
                    setDimensions((prev) => ({ ...prev, depth: parseInt(e.target.value) }))
                  }
                  className="w-full h-1.5 bg-slate-200 rounded appearance-none cursor-pointer"
                />
              </div>

              <button
                onClick={() => setShowSizeModal(false)}
                className="w-full py-2.5 rounded-xl bg-purple-600 hover:bg-purple-700 text-white font-bold text-xs transition"
              >
                Apply Dimensions
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
