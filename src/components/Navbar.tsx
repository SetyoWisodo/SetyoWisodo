import type { FC } from 'react';
import {
  Box,
  Layers,
  Download,
  RotateCcw,
  RotateCw,
  Columns,
  Sliders,
  Globe,
  Grid,
} from 'lucide-react';
import type { PackagingStudioState } from '../hooks/usePackagingStudio';
import { PACKAGING_MODELS } from '../utils/packagingModels';
import type { Language } from '../hooks/useTranslations';

interface NavbarProps {
  studio: PackagingStudioState;
  lang: Language;
  onToggleLang: () => void;
}

export const Navbar: FC<NavbarProps> = ({ studio, lang, onToggleLang }) => {
  const {
    currentModelId,
    dimensions,
    viewMode,
    setViewMode,
    undo,
    redo,
    canUndo,
    canRedo,
    setIsTemplateModalOpen,
    setIsExportModalOpen,
    setActiveTab,
  } = studio;

  const currentModel = PACKAGING_MODELS[currentModelId];

  return (
    <header className="h-14 border-b border-slate-800 bg-[#0e111a] px-4 flex items-center justify-between z-20 select-none">
      {/* Brand & Packaging Title */}
      <div className="flex items-center space-x-3">
        <div className="flex items-center space-x-2">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-indigo-600 to-violet-500 flex items-center justify-center shadow-lg shadow-indigo-500/25">
            <Box className="w-5 h-5 text-white" />
          </div>
          <div className="flex flex-col">
            <div className="flex items-center space-x-1.5">
              <span className="font-bold text-sm tracking-tight text-white font-sans">PACDORA 3D</span>
              <span className="text-[10px] font-semibold bg-indigo-500/20 text-indigo-400 px-1.5 py-0.5 rounded border border-indigo-500/30">
                STUDIO V2
              </span>
            </div>
            <span className="text-[10px] text-slate-400 hidden sm:inline">
              Online 3D Packaging Mockup & Dieline Generator
            </span>
          </div>
        </div>

        <div className="h-5 w-px bg-slate-800 hidden md:block" />

        {/* Current Packaging Model Selector Button */}
        <button
          onClick={() => setIsTemplateModalOpen(true)}
          className="flex items-center space-x-2 px-3 py-1.5 rounded-lg bg-slate-800/80 hover:bg-slate-700/80 border border-slate-700/80 text-xs text-slate-200 transition group shadow-sm"
          title="Ganti Model Kemasan"
        >
          <span className="text-base">{currentModel.thumbnail}</span>
          <span className="font-medium text-slate-100 group-hover:text-indigo-400 transition">
            {lang === 'id' ? currentModel.name : currentModel.nameEn}
          </span>
          <span className="text-[11px] text-slate-400">▾</span>
        </button>

        {/* Dimension Badge with Quick Slider Link */}
        <button
          onClick={() => setActiveTab('dimensions')}
          className="hidden lg:flex items-center space-x-1.5 px-2.5 py-1 rounded-md bg-slate-900 border border-slate-800 text-[11px] text-slate-400 hover:text-slate-200 hover:border-slate-700 transition"
          title="Ubah Dimensi Kemasan"
        >
          <Sliders className="w-3 h-3 text-indigo-400" />
          <span className="font-mono">
            {dimensions.width} × {dimensions.height} × {dimensions.depth} mm
          </span>
        </button>
      </div>

      {/* Middle View Mode Switcher */}
      <div className="hidden md:flex items-center bg-slate-900/90 border border-slate-800 rounded-lg p-0.5 text-xs">
        <button
          onClick={() => setViewMode('split')}
          className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-md font-medium transition ${
            viewMode === 'split'
              ? 'bg-indigo-600 text-white shadow-sm'
              : 'text-slate-400 hover:text-slate-200'
          }`}
          title="Split View: 3D Viewport & 2D Dieline"
        >
          <Columns className="w-3.5 h-3.5" />
          <span>Split View</span>
        </button>
        <button
          onClick={() => setViewMode('3d')}
          className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-md font-medium transition ${
            viewMode === '3d'
              ? 'bg-indigo-600 text-white shadow-sm'
              : 'text-slate-400 hover:text-slate-200'
          }`}
          title="Hanya Tampilan 3D"
        >
          <Box className="w-3.5 h-3.5" />
          <span>Hanya 3D</span>
        </button>
        <button
          onClick={() => setViewMode('2d')}
          className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-md font-medium transition ${
            viewMode === '2d'
              ? 'bg-indigo-600 text-white shadow-sm'
              : 'text-slate-400 hover:text-slate-200'
          }`}
          title="Hanya Tampilan Editor Dieline 2D"
        >
          <Layers className="w-3.5 h-3.5" />
          <span>Hanya 2D Dieline</span>
        </button>
      </div>

      {/* Right Actions: Undo/Redo, Language, Catalog, Export */}
      <div className="flex items-center space-x-2">
        {/* Undo / Redo */}
        <div className="hidden sm:flex items-center space-x-1 bg-slate-900 border border-slate-800 rounded-lg p-0.5">
          <button
            onClick={undo}
            disabled={!canUndo}
            className={`p-1.5 rounded-md transition ${
              canUndo
                ? 'text-slate-300 hover:text-white hover:bg-slate-800'
                : 'text-slate-600 cursor-not-allowed'
            }`}
            title="Undo (Ctrl+Z)"
          >
            <RotateCcw className="w-3.5 h-3.5" />
          </button>
          <button
            onClick={redo}
            disabled={!canRedo}
            className={`p-1.5 rounded-md transition ${
              canRedo
                ? 'text-slate-300 hover:text-white hover:bg-slate-800'
                : 'text-slate-600 cursor-not-allowed'
            }`}
            title="Redo (Ctrl+Y)"
          >
            <RotateCw className="w-3.5 h-3.5" />
          </button>
        </div>

        {/* Language Switcher */}
        <button
          onClick={onToggleLang}
          className="flex items-center space-x-1 px-2.5 py-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-800 text-xs text-slate-300 transition"
          title="Ganti Bahasa / Switch Language"
        >
          <Globe className="w-3.5 h-3.5 text-slate-400" />
          <span className="font-semibold uppercase text-[11px]">{lang}</span>
        </button>

        {/* Catalog Button */}
        <button
          onClick={() => setIsTemplateModalOpen(true)}
          className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 hover:text-white border border-slate-700/80 text-xs font-medium transition shadow-sm"
        >
          <Grid className="w-3.5 h-3.5 text-indigo-400" />
          <span className="hidden sm:inline">{lang === 'id' ? 'Template Galeri' : 'Templates'}</span>
        </button>

        {/* Export & Render Button (Primary Call to Action) */}
        <button
          onClick={() => setIsExportModalOpen(true)}
          className="flex items-center space-x-1.5 px-3.5 py-1.5 rounded-lg bg-gradient-to-r from-indigo-600 via-indigo-500 to-violet-600 hover:from-indigo-500 hover:to-violet-500 text-white text-xs font-semibold shadow-lg shadow-indigo-600/30 border border-indigo-400/30 transition transform active:scale-95"
        >
          <Download className="w-3.5 h-3.5" />
          <span>{lang === 'id' ? 'Ekspor & Render 4K' : 'Export & Render 4K'}</span>
        </button>
      </div>
    </header>
  );
};
