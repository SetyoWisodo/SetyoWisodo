import { useState, useRef, useEffect } from 'react';
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
  MoreHorizontal,
  Info,
  ExternalLink,
  Share2,
  Download,
  Menu,
  Pipette,
  Film,
  Image as ImageIcon,
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
    setBackgroundColor,
  } = studio;

  const currentModel = PACKAGING_MODELS[currentModelId];
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  // Left Ribbon Active Tab: 'edit' | 'models' | 'layout' | 'background' | 'video' | 'more' | 'ai_design'
  const [activeRibbon, setActiveRibbon] = useState<'edit' | 'models' | 'layout' | 'background' | 'video' | 'more' | 'ai_design'>('edit');

  // Popups / Drawers
  const [showMaterialModal, setShowMaterialModal] = useState(false);
  const [showSizeModal, setShowSizeModal] = useState(false);

  // Display mode inside editor: 3D vs 2D Dieline Net
  const [displayMode, setDisplayMode] = useState<'3d' | 'net'>('3d');

  // Active cursor tool
  const [activeTool, setActiveTool] = useState<'select' | 'pan' | 'comment'>('select');

  // Track if user has uploaded a custom image (if not, show Pacdora placeholder)
  const [, setHasUploadedCustomImage] = useState(false);

  // Set studio background to clean light studio gray matching Screenshot 179
  useEffect(() => {
    setBackgroundColor('#cbd5e1');
  }, [setBackgroundColor]);

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
        setHasUploadedCustomImage(true);
      };
    };
    reader.readAsDataURL(file);
    e.target.value = '';
  };

  const materialDisplayNames: Record<MaterialType, string> = {
    coated_matte: 'Metal matt',
    kraft_paper: 'Kraft paper',
    coated_gloss: 'Ultra gloss',
    metallic_foil: 'Metallic foil',
    glass_clear: 'Clear glass',
    glass_amber: 'Amber glass',
    plastic_frosted: 'Frosted plastic',
    kraft_white: 'White kraft',
  };

  return (
    <div className="flex-1 flex flex-col h-full overflow-hidden bg-[#e2e8f0] font-sans select-none relative">
      {/* ================= TOP NAVBAR (Screenshot 179) ================= */}
      <header className="h-14 border-b border-slate-200 bg-white px-5 flex items-center justify-between z-30 select-none shadow-xs">
        {/* Left: Pacdora Logo 'd' + Mockup Generator + Menu Icons */}
        <div className="flex items-center space-x-3.5">
          {/* Brand Circle 'd' */}
          <div
            onClick={onOpenLibrary}
            className="w-7 h-7 rounded-full bg-slate-950 flex items-center justify-center text-white font-black text-sm cursor-pointer shadow-sm"
            title="Pacdora Home"
          >
            d
          </div>

          <span className="text-sm font-bold text-slate-900 tracking-tight">
            Mockup Generator
          </span>

          <button
            onClick={onOpenLibrary}
            className="p-1.5 rounded-lg hover:bg-slate-100 text-slate-700 transition"
            title="Browse All Mockups"
          >
            <Menu className="w-4 h-4" />
          </button>

          <button
            onClick={() => setShowMaterialModal(true)}
            className="p-1.5 rounded-lg hover:bg-slate-100 text-slate-700 transition"
            title="Material & Color Inspector"
          >
            <Pipette className="w-4 h-4" />
          </button>
        </div>

        {/* Right: 3D Design, Share, Super Export */}
        <div className="flex items-center space-x-3 text-xs font-semibold">
          {/* 3D Design ↗ button (Screenshot 179) */}
          <button
            onClick={() => setDisplayMode(displayMode === '3d' ? 'net' : '3d')}
            className="flex items-center space-x-1.5 px-3.5 py-1.5 rounded-lg border border-slate-300 text-slate-800 hover:bg-slate-50 transition shadow-2xs"
          >
            <span>{displayMode === '3d' ? '3D Design' : '3D View'}</span>
            <ExternalLink className="w-3.5 h-3.5 text-slate-500" />
          </button>

          {/* Share Button (Screenshot 179) */}
          <button
            onClick={() => {
              if (navigator.clipboard) {
                navigator.clipboard.writeText(window.location.href);
                alert('Tautan mockup berhasil disalin!');
              }
            }}
            className="p-2 rounded-lg border border-slate-200 text-slate-600 hover:bg-slate-50 transition"
            title="Share Mockup"
          >
            <Share2 className="w-4 h-4" />
          </button>

          {/* Super Export Button (Screenshot 179 - Bold Purple Pill!) */}
          <button
            onClick={() => setIsExportModalOpen(true)}
            className="px-5 py-2 rounded-lg bg-[#7c3aed] hover:bg-[#6d28d9] text-white font-bold text-xs shadow-md shadow-purple-600/25 transition transform active:scale-95 flex items-center space-x-1.5 cursor-pointer"
          >
            <Download className="w-3.5 h-3.5" />
            <span>Super export</span>
          </button>
        </div>
      </header>

      {/* ================= WORKSPACE BODY (Screenshot 179) ================= */}
      <div className="flex-1 flex overflow-hidden relative">
        {/* --- 1. LEFT SLIM RIBBON BAR (Screenshot 179) --- */}
        <aside className="w-16 bg-white border-r border-slate-200/90 flex flex-col items-center py-3.5 space-y-4 shrink-0 z-20 shadow-xs">
          {/* Edit Button (Purple active indicator) */}
          <button
            onClick={() => {
              setActiveRibbon('edit');
              setDisplayMode('3d');
            }}
            className={`flex flex-col items-center space-y-1 transition ${
              activeRibbon === 'edit'
                ? 'text-[#7c3aed] font-semibold'
                : 'text-slate-400 hover:text-slate-700'
            }`}
          >
            <div
              className={`w-9 h-9 rounded-xl flex items-center justify-center transition ${
                activeRibbon === 'edit'
                  ? 'bg-purple-100/70 text-[#7c3aed]'
                  : 'hover:bg-slate-100'
              }`}
            >
              <Sparkles className="w-4 h-4" />
            </div>
            <span className="text-[10px]">Edit</span>
          </button>

          {/* Models Button (Switches back to Mockups Library!) */}
          <button
            onClick={() => {
              setActiveRibbon('models');
              onOpenLibrary();
            }}
            className="flex flex-col items-center space-y-1 text-slate-400 hover:text-slate-700 transition"
          >
            <div className="w-9 h-9 rounded-xl hover:bg-slate-100 flex items-center justify-center">
              <Box className="w-4 h-4" />
            </div>
            <span className="text-[10px]">Models</span>
          </button>

          {/* Layout Button (Toggles 2D Dieline Net) */}
          <button
            onClick={() => {
              setActiveRibbon('layout');
              setDisplayMode(displayMode === 'net' ? '3d' : 'net');
            }}
            className={`flex flex-col items-center space-y-1 transition ${
              displayMode === 'net'
                ? 'text-[#7c3aed] font-semibold'
                : 'text-slate-400 hover:text-slate-700'
            }`}
          >
            <div
              className={`w-9 h-9 rounded-xl flex items-center justify-center transition ${
                displayMode === 'net' ? 'bg-purple-100/70 text-[#7c3aed]' : 'hover:bg-slate-100'
              }`}
            >
              <Layers className="w-4 h-4" />
            </div>
            <span className="text-[10px]">Layout</span>
          </button>

          {/* AI Background Button */}
          <button
            onClick={() => {
              setActiveRibbon('background');
              setShowMaterialModal(true);
            }}
            className="flex flex-col items-center space-y-1 text-slate-400 hover:text-slate-700 transition"
          >
            <div className="w-9 h-9 rounded-xl hover:bg-slate-100 flex items-center justify-center">
              <ImageIcon className="w-4 h-4" />
            </div>
            <span className="text-[9px] text-center leading-tight">AI Background</span>
          </button>

          {/* Video Button */}
          <button
            onClick={() => {
              setActiveRibbon('video');
              setIsExportModalOpen(true);
            }}
            className="flex flex-col items-center space-y-1 text-slate-400 hover:text-slate-700 transition"
          >
            <div className="w-9 h-9 rounded-xl hover:bg-slate-100 flex items-center justify-center">
              <Film className="w-4 h-4" />
            </div>
            <span className="text-[10px]">Video</span>
          </button>

          {/* More Button */}
          <button
            onClick={() => setActiveRibbon('more')}
            className="flex flex-col items-center space-y-1 text-slate-400 hover:text-slate-700 transition"
          >
            <div className="w-9 h-9 rounded-xl hover:bg-slate-100 flex items-center justify-center">
              <MoreHorizontal className="w-4 h-4" />
            </div>
            <span className="text-[10px]">More</span>
          </button>

          {/* Bottom AI Design Button (Screenshot 179) */}
          <div className="mt-auto pt-4 flex flex-col items-center space-y-1 text-slate-400 hover:text-purple-600 transition cursor-pointer">
            <div className="w-9 h-9 rounded-xl bg-purple-50 text-purple-600 flex items-center justify-center">
              <Sparkles className="w-4 h-4" />
            </div>
            <span className="text-[9px] font-medium text-center">AI Design</span>
          </div>
        </aside>

        {/* --- 2. LEFT TOOL DRAWER (Screenshot 179 Floating White Card) --- */}
        <aside className="w-76 m-3 mr-0 bg-white border border-slate-200/90 rounded-2xl flex flex-col h-[calc(100%-24px)] shrink-0 p-5 overflow-y-auto space-y-4.5 z-10 shadow-sm">
          <h2 className="text-sm font-bold text-slate-900 tracking-tight">Upload images</h2>

          {/* Big Purple Dashed Upload Box (Screenshot 179) */}
          <div className="border-2 border-dashed border-[#c084fc] rounded-2xl bg-[#faf5ff] p-5 flex flex-col items-center justify-center text-center space-y-3">
            {/* Image placeholder landscape icon */}
            <div className="w-12 h-10 rounded-lg flex items-center justify-center text-[#7c3aed]">
              <svg width="40" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75">
                <rect width="18" height="18" x="3" y="3" rx="2" ry="2"/>
                <circle cx="9" cy="9" r="2"/>
                <path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/>
              </svg>
            </div>

            {/* Purple Upload Button */}
            <button
              onClick={handleUploadClick}
              className="px-6 py-2 rounded-xl bg-[#7c3aed] hover:bg-[#6d28d9] text-white font-bold text-xs shadow-md shadow-purple-600/30 transition transform active:scale-95 flex items-center space-x-1.5 cursor-pointer"
            >
              <Upload className="w-3.5 h-3.5" />
              <span>Upload</span>
            </button>
            <input
              type="file"
              ref={fileInputRef}
              onChange={handleFileChange}
              accept="image/*"
              className="hidden"
            />

            <span className="text-[11px] text-slate-400 font-mono">
              491 x 733 px
            </span>
          </div>

          {/* Custom Material Row (Screenshot 179) */}
          <div
            onClick={() => setShowMaterialModal(true)}
            className="p-3 rounded-xl border border-slate-200/90 hover:border-purple-300 bg-white hover:bg-purple-50/20 cursor-pointer flex items-center justify-between transition group shadow-2xs"
          >
            <div>
              <span className="text-[10px] text-slate-400 block font-medium">Custom material</span>
              <span className="text-xs font-semibold text-slate-800 group-hover:text-purple-600 transition capitalize">
                {materialDisplayNames[material] || 'Metal matt'}
              </span>
            </div>
            <ChevronRight className="w-4 h-4 text-slate-400 group-hover:text-purple-600 transition" />
          </div>

          {/* Custom Size Row (Screenshot 179) */}
          <div
            onClick={() => setShowSizeModal(true)}
            className="p-3 rounded-xl border border-slate-200/90 hover:border-purple-300 bg-white hover:bg-purple-50/20 cursor-pointer flex items-center justify-between transition group shadow-2xs"
          >
            <div>
              <span className="text-[10px] text-slate-400 block font-medium">Custom size</span>
              <span className="text-xs font-semibold text-slate-800 group-hover:text-purple-600 transition font-mono">
                {dimensions.depth || 75} x {dimensions.width || 130} x {dimensions.height || 225} mm
              </span>
            </div>
            <ChevronRight className="w-4 h-4 text-slate-400 group-hover:text-purple-600 transition" />
          </div>

          {/* Find Similar with AI Row (Screenshot 179) */}
          <div
            onClick={onOpenLibrary}
            className="p-3 rounded-xl border border-slate-200/90 hover:border-purple-300 bg-white hover:bg-purple-50/20 cursor-pointer flex items-center justify-between transition group shadow-2xs"
          >
            <span className="text-xs font-semibold text-slate-800 group-hover:text-purple-600 transition">
              Find similar with AI
            </span>
            <ChevronRight className="w-4 h-4 text-slate-400 group-hover:text-purple-600 transition" />
          </div>

          {/* Open/Close Lid Slider (for Boxes & Bottles) */}
          {currentModel.hasOpenAnimation && (
            <div className="p-3 rounded-xl border border-slate-200 bg-slate-50/60 space-y-1.5 shadow-2xs">
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

          {/* Model ID Tag (Screenshot 179) */}
          <div className="mt-auto pt-3 flex items-center space-x-1.5 text-[10px] text-slate-400 font-mono">
            <Info className="w-3 h-3 text-slate-400 shrink-0" />
            <span>Model ID: 604050</span>
          </div>
        </aside>

        {/* --- 3. CENTER 3D VIEWPORT (Screenshot 179) --- */}
        <main className="flex-1 relative overflow-hidden bg-[#d1d5db] flex items-center justify-center">
          {displayMode === '3d' ? (
            <div className="w-full h-full relative">
              <Viewport3D
                ref={viewportRef}
                studio={studio}
                dielineCanvas={dielineCanvas}
              />

              {/* Bottom Floating Control Bar (Screenshot 179) */}
              <div className="absolute bottom-5 left-1/2 -translate-x-1/2 flex items-center space-x-3 pointer-events-auto z-10 select-none">
                {/* Zoom & View Toggles */}
                <div className="bg-white/95 backdrop-blur-md shadow-lg border border-slate-200/80 rounded-xl px-2.5 py-1 flex items-center space-x-2 text-slate-700">
                  <button
                    onClick={() => {}}
                    className="p-1 hover:bg-slate-100 rounded-lg text-slate-600 font-bold text-sm w-6 h-6 flex items-center justify-center cursor-pointer"
                    title="Zoom Out"
                  >
                    −
                  </button>
                  <div className="h-3.5 w-px bg-slate-200" />
                  <button
                    onClick={() => {}}
                    className="p-1 hover:bg-slate-100 rounded-lg text-slate-600 font-bold text-sm w-6 h-6 flex items-center justify-center cursor-pointer"
                    title="Zoom In"
                  >
                    +
                  </button>
                  <div className="h-3.5 w-px bg-slate-200" />

                  {/* 3D Box view icon */}
                  <button
                    onClick={() => setDisplayMode('3d')}
                    className="p-1 rounded-lg bg-slate-100 text-slate-800 transition cursor-pointer"
                    title="3D View"
                  >
                    <Box className="w-3.5 h-3.5" />
                  </button>

                  {/* 2D Net Dieline icon */}
                  <button
                    onClick={() => setDisplayMode('net')}
                    className="p-1 rounded-lg hover:bg-slate-100 text-slate-600 transition cursor-pointer"
                    title="2D Dieline Net View"
                  >
                    <Layers className="w-3.5 h-3.5" />
                  </button>
                </div>

                {/* Watermark Free Gold Crown Badge (Screenshot 179) */}
                <div className="bg-white/95 backdrop-blur-md shadow-lg border border-slate-200/80 rounded-xl px-3.5 py-1.5 flex items-center space-x-1.5 text-xs font-semibold text-slate-800">
                  <span className="text-amber-500 text-sm">👑</span>
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
                className="absolute top-4 right-4 px-4 py-2 rounded-xl bg-purple-600 hover:bg-purple-700 text-white font-semibold text-xs shadow-lg transition cursor-pointer"
              >
                ← Back to 3D View
              </button>
            </div>
          )}
        </main>

        {/* --- 4. RIGHT FLOATING TOOLBAR (Screenshot 179) --- */}
        <div className="absolute right-4 top-5 flex flex-col space-y-1.5 bg-white/95 backdrop-blur-md shadow-lg border border-slate-200/80 rounded-2xl p-1 z-20 text-slate-600">
          <button
            onClick={() => setActiveTool('select')}
            className={`p-2 rounded-xl transition cursor-pointer ${
              activeTool === 'select' ? 'bg-purple-50 text-purple-600 font-bold' : 'hover:bg-slate-100'
            }`}
            title="Select tool"
          >
            <MousePointer className="w-4 h-4" />
          </button>

          <button
            onClick={() => setActiveTool('pan')}
            className={`p-2 rounded-xl transition cursor-pointer ${
              activeTool === 'pan' ? 'bg-purple-50 text-purple-600 font-bold' : 'hover:bg-slate-100'
            }`}
            title="Pan hand tool"
          >
            <Hand className="w-4 h-4" />
          </button>

          <button
            onClick={() => setActiveTool('comment')}
            className={`p-2 rounded-xl transition cursor-pointer ${
              activeTool === 'comment' ? 'bg-purple-50 text-purple-600 font-bold' : 'hover:bg-slate-100'
            }`}
            title="Comment"
          >
            <MessageSquare className="w-4 h-4" />
          </button>

          <div className="w-full h-px bg-slate-200" />

          <button
            onClick={undo}
            disabled={!canUndo}
            className={`p-2 rounded-xl transition cursor-pointer ${
              canUndo ? 'hover:bg-slate-100 text-slate-700' : 'text-slate-300 cursor-not-allowed'
            }`}
            title="Undo"
          >
            <RotateCcw className="w-4 h-4" />
          </button>

          <button
            onClick={redo}
            disabled={!canRedo}
            className={`p-2 rounded-xl transition cursor-pointer ${
              canRedo ? 'hover:bg-slate-100 text-slate-700' : 'text-slate-300 cursor-not-allowed'
            }`}
            title="Redo"
          >
            <RotateCw className="w-4 h-4" />
          </button>
        </div>

        {/* --- 5. FLOATING BLACK CIRCLE SUPPORT BUTTON (Screenshot 179) --- */}
        <div className="absolute right-4 bottom-5 w-10 h-10 rounded-full bg-slate-950 text-white shadow-xl flex items-center justify-center cursor-pointer hover:scale-105 transition z-20">
          <MessageSquare className="w-4 h-4" />
        </div>
      </div>

      {/* ================= POPUP MODALS: MATERIAL & SIZE ================= */}
      {showMaterialModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
          <div className="bg-white rounded-2xl w-full max-w-md p-6 shadow-2xl space-y-4">
            <div className="flex justify-between items-center border-b pb-3">
              <h3 className="font-bold text-sm text-slate-900">Custom Material Finish</h3>
              <button
                onClick={() => setShowMaterialModal(false)}
                className="text-slate-400 hover:text-slate-700 font-bold cursor-pointer"
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
                  className={`w-full text-left p-3 rounded-xl border transition cursor-pointer ${
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
                className="text-slate-400 hover:text-slate-700 font-bold cursor-pointer"
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
                className="w-full py-2.5 rounded-xl bg-purple-600 hover:bg-purple-700 text-white font-bold text-xs transition cursor-pointer"
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
