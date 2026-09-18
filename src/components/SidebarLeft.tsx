import { useState } from 'react';
import type { FC } from 'react';
import {
  Box,
  Sliders,
  Sparkles,
  Sun,
  LayoutTemplate,
  Droplets,
  Check,
  RefreshCw,
} from 'lucide-react';
import type { PackagingStudioState } from '../hooks/usePackagingStudio';
import { PACKAGING_MODELS } from '../utils/packagingModels';
import { BRAND_PRESETS } from '../utils/presets';
import type { MaterialType, LightingPreset, PackagingCategory } from '../types/packaging';

interface SidebarLeftProps {
  studio: PackagingStudioState;
}

export const SidebarLeft: FC<SidebarLeftProps> = ({ studio }) => {
  const {
    currentModelId,
    setModel,
    dimensions,
    setDimensions,
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
    activeTab,
    setActiveTab,
    applyPreset,
  } = studio;

  const currentModel = PACKAGING_MODELS[currentModelId];
  const [categoryFilter, setCategoryFilter] = useState<'all' | PackagingCategory>('all');

  // Filtered models
  const modelList = Object.values(PACKAGING_MODELS).filter((m) =>
    categoryFilter === 'all' ? true : m.category === categoryFilter
  );

  // Calculate volume in ml / cm3
  const volumeMl = Math.round(
    currentModel.defaultDimensions.radius
      ? (Math.PI * Math.pow(dimensions.radius || dimensions.width / 2, 2) * dimensions.height) / 1000
      : (dimensions.width * dimensions.height * dimensions.depth) / 1000
  );

  // Material descriptions & colors
  const materialsConfig: { id: MaterialType; name: string; desc: string; color: string }[] = [
    { id: 'kraft_paper', name: 'Kraft Brown', desc: 'Kardus serat cokelat alami berserat kayu', color: '#c49a6c' },
    { id: 'kraft_white', name: 'Kraft White', desc: 'Kertas kraft putih bertekstur lembut', color: '#ede8df' },
    { id: 'coated_matte', name: 'Matte Coated', desc: 'Karton dupleks/ivory laminasi doff halus', color: '#475569' },
    { id: 'coated_gloss', name: 'Ultra Gloss', desc: 'Lapisan vernis UV kilap tinggi memantulkan cahaya', color: '#38bdf8' },
    { id: 'metallic_foil', name: 'Metallic Foil', desc: 'Lapisan foil metalik krom emas / aluminium', color: '#d4af37' },
    { id: 'glass_clear', name: 'Kaca Bening', desc: 'Kaca transparan dengan bias cahaya realistis', color: '#93c5fd' },
    { id: 'glass_amber', name: 'Kaca Amber', desc: 'Kaca botol kosmetik cokelat gelap filter UV', color: '#78350f' },
    { id: 'plastic_frosted', name: 'Frosted Translucent', desc: 'Plastik buram matte tembus pandang', color: '#cbd5e1' },
  ];

  // Studio lighting presets config
  const lightingPresets: { id: LightingPreset; name: string; desc: string; preview: string }[] = [
    { id: 'studio_minimal', name: 'Studio Minimal', desc: 'Dual softbox netral untuk katalog komersial', preview: 'bg-gradient-to-tr from-slate-700 to-slate-500' },
    { id: 'warm_commercial', name: 'Warm Commercial', desc: 'Sinar hangat keemasan ramah konsumen', preview: 'bg-gradient-to-tr from-amber-600 to-orange-400' },
    { id: 'dramatic_rim', name: 'Dramatic Rim', desc: 'Kontras gelap dengan cahaya tepi dramatis', preview: 'bg-gradient-to-tr from-sky-600 to-rose-600' },
    { id: 'neon_cyber', name: 'Neon Cyberpunk', desc: 'Cahaya futuristik cyan dan magenta berpendar', preview: 'bg-gradient-to-tr from-cyan-400 to-fuchsia-500' },
    { id: 'pure_catalog', name: 'Pure White Catalog', desc: 'Latar putih e-commerce bersih tanpa bayang kasar', preview: 'bg-gradient-to-tr from-slate-100 to-slate-300' },
  ];

  // Quick background swatches
  const bgSwatches = [
    '#0f1117',
    '#1e293b',
    '#3b2413',
    '#090d16',
    '#1b2f21',
    '#18181b',
    '#f8fafc',
    '#f1f5f9',
    '#fef3c7',
  ];

  return (
    <aside className="w-80 border-r border-slate-800 bg-[#12151e] flex flex-col h-full shrink-0 select-none z-10">
      {/* Top Navigation Tabs */}
      <div className="flex border-b border-slate-800 bg-[#0e111a] px-1 py-1 overflow-x-auto text-xs shrink-0">
        <button
          onClick={() => setActiveTab('templates')}
          className={`flex items-center space-x-1.5 px-3 py-2 rounded-lg font-medium transition whitespace-nowrap ${
            activeTab === 'templates'
              ? 'bg-indigo-600/20 text-indigo-400 border border-indigo-500/40 shadow-sm'
              : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
          }`}
          title="Katalog Model Kemasan"
        >
          <Box className="w-3.5 h-3.5" />
          <span>Model</span>
        </button>

        <button
          onClick={() => setActiveTab('dimensions')}
          className={`flex items-center space-x-1.5 px-3 py-2 rounded-lg font-medium transition whitespace-nowrap ${
            activeTab === 'dimensions'
              ? 'bg-indigo-600/20 text-indigo-400 border border-indigo-500/40 shadow-sm'
              : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
          }`}
          title="Dimensi Parametrik"
        >
          <Sliders className="w-3.5 h-3.5" />
          <span>Dimensi</span>
        </button>

        <button
          onClick={() => setActiveTab('materials')}
          className={`flex items-center space-x-1.5 px-3 py-2 rounded-lg font-medium transition whitespace-nowrap ${
            activeTab === 'materials'
              ? 'bg-indigo-600/20 text-indigo-400 border border-indigo-500/40 shadow-sm'
              : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
          }`}
          title="Bahan & Finishing"
        >
          <Sparkles className="w-3.5 h-3.5" />
          <span>Bahan</span>
        </button>

        <button
          onClick={() => setActiveTab('lighting')}
          className={`flex items-center space-x-1.5 px-3 py-2 rounded-lg font-medium transition whitespace-nowrap ${
            activeTab === 'lighting'
              ? 'bg-indigo-600/20 text-indigo-400 border border-indigo-500/40 shadow-sm'
              : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
          }`}
          title="Studio Cahaya"
        >
          <Sun className="w-3.5 h-3.5" />
          <span>Cahaya</span>
        </button>

        <button
          onClick={() => setActiveTab('brand_presets')}
          className={`flex items-center space-x-1.5 px-3 py-2 rounded-lg font-medium transition whitespace-nowrap ${
            activeTab === 'brand_presets'
              ? 'bg-indigo-600/20 text-indigo-400 border border-indigo-500/40 shadow-sm'
              : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
          }`}
          title="Preset Desain Siap Pakai"
        >
          <LayoutTemplate className="w-3.5 h-3.5" />
          <span>Preset</span>
        </button>
      </div>

      {/* Tab Content Panel */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {/* ================= TAB 1: PACKAGING MODELS ================= */}
        {activeTab === 'templates' && (
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold text-slate-300 uppercase tracking-wider">Kategori Model</span>
              <span className="text-[11px] text-slate-500">{modelList.length} Model</span>
            </div>

            {/* Category Filter Pills */}
            <div className="flex items-center space-x-1 overflow-x-auto pb-1 text-xs">
              {[
                { id: 'all', label: 'Semua' },
                { id: 'boxes', label: 'Kotak' },
                { id: 'bottles', label: 'Botol' },
                { id: 'pouches', label: 'Pouch' },
                { id: 'cups_tubes', label: 'Tube/Cup' },
              ].map((cat) => (
                <button
                  key={cat.id}
                  onClick={() => setCategoryFilter(cat.id as any)}
                  className={`px-2.5 py-1 rounded-md text-[11px] font-medium transition whitespace-nowrap ${
                    categoryFilter === cat.id
                      ? 'bg-indigo-600 text-white'
                      : 'bg-slate-800/80 text-slate-400 hover:text-slate-200 hover:bg-slate-700'
                  }`}
                >
                  {cat.label}
                </button>
              ))}
            </div>

            {/* Models Grid */}
            <div className="grid grid-cols-1 gap-2.5 pt-1">
              {modelList.map((m) => {
                const isSelected = m.id === currentModelId;
                return (
                  <div
                    key={m.id}
                    onClick={() => setModel(m.id)}
                    className={`p-3 rounded-xl border transition cursor-pointer flex items-center space-x-3 group ${
                      isSelected
                        ? 'bg-indigo-600/15 border-indigo-500 shadow-md shadow-indigo-500/10'
                        : 'bg-slate-800/40 border-slate-700/60 hover:bg-slate-800 hover:border-slate-600'
                    }`}
                  >
                    <div className="w-12 h-12 rounded-lg bg-slate-800/90 border border-slate-700 flex items-center justify-center text-2xl group-hover:scale-105 transition shrink-0">
                      {m.thumbnail}
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between">
                        <span className={`text-xs font-semibold truncate ${isSelected ? 'text-indigo-400' : 'text-slate-200'}`}>
                          {m.name}
                        </span>
                        {isSelected && <Check className="w-3.5 h-3.5 text-indigo-400 shrink-0 ml-1" />}
                      </div>
                      <span className="text-[11px] text-slate-400 line-clamp-1 block">
                        {m.description}
                      </span>
                      <span className="text-[10px] text-slate-500 font-mono mt-0.5 block">
                        {m.defaultDimensions.width}×{m.defaultDimensions.height}×{m.defaultDimensions.depth}mm
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* ================= TAB 2: PARAMETRIC DIMENSIONS ================= */}
        {activeTab === 'dimensions' && (
          <div className="space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800 pb-2">
              <span className="text-xs font-semibold text-slate-300 uppercase tracking-wider">
                Dimensi Parametrik (mm)
              </span>
              <button
                onClick={() => setDimensions({ ...currentModel.defaultDimensions })}
                className="text-[11px] text-indigo-400 hover:text-indigo-300 flex items-center space-x-1"
                title="Kembalikan ke ukuran standar"
              >
                <RefreshCw className="w-3 h-3" />
                <span>Reset</span>
              </button>
            </div>

            {/* Width Slider */}
            <div className="space-y-1.5">
              <div className="flex justify-between items-center text-xs">
                <span className="text-slate-300 font-medium">Lebar (Width)</span>
                <div className="flex items-center space-x-1">
                  <input
                    type="number"
                    value={dimensions.width}
                    min={currentModel.minDimensions.width}
                    max={currentModel.maxDimensions.width}
                    onChange={(e) =>
                      setDimensions((prev) => ({ ...prev, width: parseInt(e.target.value) || prev.width }))
                    }
                    className="w-16 px-1.5 py-0.5 bg-slate-900 border border-slate-700 rounded text-right font-mono text-xs text-indigo-400 focus:outline-none focus:border-indigo-500"
                  />
                  <span className="text-[11px] text-slate-500">mm</span>
                </div>
              </div>
              <input
                type="range"
                min={currentModel.minDimensions.width}
                max={currentModel.maxDimensions.width}
                value={dimensions.width}
                onChange={(e) =>
                  setDimensions((prev) => ({ ...prev, width: parseInt(e.target.value) }))
                }
                className="w-full h-1.5 bg-slate-800 rounded-lg appearance-none cursor-pointer"
              />
            </div>

            {/* Height Slider */}
            <div className="space-y-1.5">
              <div className="flex justify-between items-center text-xs">
                <span className="text-slate-300 font-medium">Tinggi (Height)</span>
                <div className="flex items-center space-x-1">
                  <input
                    type="number"
                    value={dimensions.height}
                    min={currentModel.minDimensions.height}
                    max={currentModel.maxDimensions.height}
                    onChange={(e) =>
                      setDimensions((prev) => ({ ...prev, height: parseInt(e.target.value) || prev.height }))
                    }
                    className="w-16 px-1.5 py-0.5 bg-slate-900 border border-slate-700 rounded text-right font-mono text-xs text-indigo-400 focus:outline-none focus:border-indigo-500"
                  />
                  <span className="text-[11px] text-slate-500">mm</span>
                </div>
              </div>
              <input
                type="range"
                min={currentModel.minDimensions.height}
                max={currentModel.maxDimensions.height}
                value={dimensions.height}
                onChange={(e) =>
                  setDimensions((prev) => ({ ...prev, height: parseInt(e.target.value) }))
                }
                className="w-full h-1.5 bg-slate-800 rounded-lg appearance-none cursor-pointer"
              />
            </div>

            {/* Depth Slider */}
            <div className="space-y-1.5">
              <div className="flex justify-between items-center text-xs">
                <span className="text-slate-300 font-medium">Panjang / Tebal (Depth)</span>
                <div className="flex items-center space-x-1">
                  <input
                    type="number"
                    value={dimensions.depth}
                    min={currentModel.minDimensions.depth}
                    max={currentModel.maxDimensions.depth}
                    onChange={(e) =>
                      setDimensions((prev) => ({ ...prev, depth: parseInt(e.target.value) || prev.depth }))
                    }
                    className="w-16 px-1.5 py-0.5 bg-slate-900 border border-slate-700 rounded text-right font-mono text-xs text-indigo-400 focus:outline-none focus:border-indigo-500"
                  />
                  <span className="text-[11px] text-slate-500">mm</span>
                </div>
              </div>
              <input
                type="range"
                min={currentModel.minDimensions.depth}
                max={currentModel.maxDimensions.depth}
                value={dimensions.depth}
                onChange={(e) =>
                  setDimensions((prev) => ({ ...prev, depth: parseInt(e.target.value) }))
                }
                className="w-full h-1.5 bg-slate-800 rounded-lg appearance-none cursor-pointer"
              />
            </div>

            {/* Radius slider if cylindrical */}
            {currentModel.defaultDimensions.radius !== undefined && (
              <div className="space-y-1.5">
                <div className="flex justify-between items-center text-xs">
                  <span className="text-slate-300 font-medium">Radius Tabung</span>
                  <div className="flex items-center space-x-1">
                    <span className="font-mono text-xs text-indigo-400">
                      {Math.round((dimensions.radius || dimensions.width / 2))} mm
                    </span>
                  </div>
                </div>
                <input
                  type="range"
                  min="20"
                  max="60"
                  value={dimensions.radius || dimensions.width / 2}
                  onChange={(e) => {
                    const r = parseInt(e.target.value);
                    setDimensions((prev) => ({ ...prev, radius: r, width: r * 2, depth: r * 2 }));
                  }}
                  className="w-full h-1.5 bg-slate-800 rounded-lg appearance-none cursor-pointer"
                />
              </div>
            )}

            {/* Packaging Specification Card */}
            <div className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800 space-y-2 mt-4">
              <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block">
                Spesifikasi Kemasan
              </span>
              <div className="flex justify-between text-xs">
                <span className="text-slate-400">Kapasitas Isi:</span>
                <span className="text-indigo-400 font-mono font-semibold">~{volumeMl} ml</span>
              </div>
              <div className="flex justify-between text-xs">
                <span className="text-slate-400">Ukuran Dieline:</span>
                <span className="text-slate-200 font-mono">
                  {currentModel.textureWidth} × {currentModel.textureHeight} px
                </span>
              </div>
              <div className="flex justify-between text-xs">
                <span className="text-slate-400">Tipe Konstruksi:</span>
                <span className="text-slate-200">{currentModel.nameEn}</span>
              </div>
            </div>
          </div>
        )}

        {/* ================= TAB 3: MATERIALS & FINISHES ================= */}
        {activeTab === 'materials' && (
          <div className="space-y-4">
            <span className="text-xs font-semibold text-slate-300 uppercase tracking-wider block border-b border-slate-800 pb-2">
              Bahan Permukaan (Paper & Finishes)
            </span>

            <div className="grid grid-cols-1 gap-2">
              {materialsConfig.map((mat) => {
                const isSelected = mat.id === material;
                const isAllowed = currentModel.allowedMaterials.includes(mat.id);

                return (
                  <button
                    key={mat.id}
                    disabled={!isAllowed}
                    onClick={() => setMaterial(mat.id)}
                    className={`p-3 rounded-xl border text-left flex items-center space-x-3 transition ${
                      isSelected
                        ? 'bg-indigo-600/15 border-indigo-500 shadow-sm'
                        : isAllowed
                        ? 'bg-slate-800/40 border-slate-700/60 hover:bg-slate-800 hover:border-slate-600'
                        : 'opacity-40 cursor-not-allowed bg-slate-900/40 border-slate-800'
                    }`}
                  >
                    <div
                      style={{ backgroundColor: mat.color }}
                      className="w-8 h-8 rounded-lg shadow-inner border border-white/20 shrink-0"
                    />
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between">
                        <span className={`text-xs font-semibold ${isSelected ? 'text-indigo-400' : 'text-slate-200'}`}>
                          {mat.name}
                        </span>
                        {isSelected && <Check className="w-3.5 h-3.5 text-indigo-400" />}
                      </div>
                      <span className="text-[11px] text-slate-400 line-clamp-1 block">
                        {mat.desc}
                      </span>
                    </div>
                  </button>
                );
              })}
            </div>

            {/* Special Finishes Controls */}
            <div className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800 space-y-3 mt-4">
              <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block">
                Efek & Lapisan Khusus
              </span>

              {/* Condensation Droplets */}
              <label className="flex items-center justify-between cursor-pointer text-xs">
                <div className="flex items-center space-x-2">
                  <Droplets className="w-4 h-4 text-sky-400" />
                  <span className="text-slate-200">Embun Air Dingin (Condensation)</span>
                </div>
                <input
                  type="checkbox"
                  checked={hasCondensation}
                  onChange={(e) => setHasCondensation(e.target.checked)}
                  className="rounded bg-slate-800 border-slate-700 text-indigo-600 focus:ring-0 w-4 h-4 cursor-pointer"
                />
              </label>

              {/* Wireframe Toggle */}
              <label className="flex items-center justify-between cursor-pointer text-xs pt-1 border-t border-slate-800/60">
                <div className="flex items-center space-x-2">
                  <Box className="w-4 h-4 text-purple-400" />
                  <span className="text-slate-200">Mode Poligon (Wireframe 3D)</span>
                </div>
                <input
                  type="checkbox"
                  checked={showWireframe}
                  onChange={(e) => setShowWireframe(e.target.checked)}
                  className="rounded bg-slate-800 border-slate-700 text-indigo-600 focus:ring-0 w-4 h-4 cursor-pointer"
                />
              </label>
            </div>
          </div>
        )}

        {/* ================= TAB 4: STUDIO LIGHTING & BACKDROP ================= */}
        {activeTab === 'lighting' && (
          <div className="space-y-4">
            <span className="text-xs font-semibold text-slate-300 uppercase tracking-wider block border-b border-slate-800 pb-2">
              Studio Pencahayaan
            </span>

            <div className="grid grid-cols-1 gap-2">
              {lightingPresets.map((preset) => {
                const isSelected = preset.id === lighting;
                return (
                  <button
                    key={preset.id}
                    onClick={() => setLighting(preset.id)}
                    className={`p-3 rounded-xl border text-left flex items-center space-x-3 transition ${
                      isSelected
                        ? 'bg-indigo-600/15 border-indigo-500 shadow-sm'
                        : 'bg-slate-800/40 border-slate-700/60 hover:bg-slate-800 hover:border-slate-600'
                    }`}
                  >
                    <div className={`w-8 h-8 rounded-lg ${preset.preview} shrink-0 shadow border border-white/20`} />
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between">
                        <span className={`text-xs font-semibold ${isSelected ? 'text-indigo-400' : 'text-slate-200'}`}>
                          {preset.name}
                        </span>
                        {isSelected && <Check className="w-3.5 h-3.5 text-indigo-400" />}
                      </div>
                      <span className="text-[11px] text-slate-400 line-clamp-1 block">
                        {preset.desc}
                      </span>
                    </div>
                  </button>
                );
              })}
            </div>

            {/* Studio Backdrop & Environment */}
            <div className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800 space-y-3 mt-4">
              <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block">
                Latar Belakang Studio (Backdrop)
              </span>

              {/* Transparent BG Toggle */}
              <label className="flex items-center justify-between cursor-pointer text-xs">
                <span className="text-slate-300">Latar Transparan (PNG Alpha)</span>
                <input
                  type="checkbox"
                  checked={isTransparentBg}
                  onChange={(e) => setIsTransparentBg(e.target.checked)}
                  className="rounded bg-slate-800 border-slate-700 text-indigo-600 focus:ring-0 w-4 h-4 cursor-pointer"
                />
              </label>

              {!isTransparentBg && (
                <div className="space-y-2 pt-1">
                  <div className="flex items-center justify-between text-xs">
                    <span className="text-slate-400">Warna Latar:</span>
                    <div className="flex items-center space-x-1.5">
                      <input
                        type="color"
                        value={backgroundColor}
                        onChange={(e) => setBackgroundColor(e.target.value)}
                        className="w-6 h-6 rounded cursor-pointer border-0 bg-transparent"
                      />
                      <span className="font-mono text-[11px] text-slate-300 uppercase">{backgroundColor}</span>
                    </div>
                  </div>

                  {/* Swatches */}
                  <div className="flex items-center space-x-1.5 pt-1">
                    {bgSwatches.map((color) => (
                      <button
                        key={color}
                        onClick={() => setBackgroundColor(color)}
                        style={{ backgroundColor: color }}
                        className={`w-5 h-5 rounded-md border ${
                          backgroundColor.toLowerCase() === color.toLowerCase()
                            ? 'border-indigo-400 scale-110 shadow'
                            : 'border-slate-700'
                        }`}
                      />
                    ))}
                  </div>
                </div>
              )}
            </div>

            {/* Turntable 360 Spin Controls */}
            <div className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800 space-y-2">
              <div className="flex items-center justify-between text-xs">
                <span className="text-slate-300 font-medium">Putaran Turntable 360°</span>
                <button
                  onClick={() => setAutoRotate(!autoRotate)}
                  className={`px-2 py-0.5 rounded text-[11px] font-medium transition ${
                    autoRotate ? 'bg-indigo-600 text-white' : 'bg-slate-800 text-slate-400'
                  }`}
                >
                  {autoRotate ? 'Aktif' : 'Nonaktif'}
                </button>
              </div>

              {autoRotate && (
                <div className="space-y-1 pt-1">
                  <div className="flex justify-between text-[11px] text-slate-400">
                    <span>Kecepatan Putar</span>
                    <span className="font-mono">{rotationSpeed}x</span>
                  </div>
                  <input
                    type="range"
                    min="0.2"
                    max="3"
                    step="0.1"
                    value={rotationSpeed}
                    onChange={(e) => setRotationSpeed(parseFloat(e.target.value))}
                    className="w-full h-1.5 bg-slate-800 rounded-lg appearance-none cursor-pointer"
                  />
                </div>
              )}
            </div>
          </div>
        )}

        {/* ================= TAB 5: BRAND PRESETS ================= */}
        {activeTab === 'brand_presets' && (
          <div className="space-y-3">
            <span className="text-xs font-semibold text-slate-300 uppercase tracking-wider block border-b border-slate-800 pb-2">
              Desain Kemasan Siap Pakai
            </span>

            <div className="grid grid-cols-1 gap-2.5">
              {BRAND_PRESETS.map((preset) => {
                const targetModel = PACKAGING_MODELS[preset.modelId];
                return (
                  <div
                    key={preset.id}
                    onClick={() => applyPreset(preset)}
                    className="p-3 rounded-xl border border-slate-700/60 bg-slate-800/40 hover:bg-slate-800 hover:border-indigo-500/80 transition cursor-pointer group shadow-sm"
                  >
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-xs font-semibold text-slate-100 group-hover:text-indigo-400 transition">
                        {preset.title}
                      </span>
                      <span className="text-lg">{targetModel.thumbnail}</span>
                    </div>
                    <span className="text-[11px] text-indigo-400/90 font-medium block">
                      {preset.category} • {targetModel.nameEn}
                    </span>
                    <p className="text-[11px] text-slate-400 line-clamp-2 mt-1">
                      {preset.description}
                    </p>
                    <div className="mt-2.5 pt-2 border-t border-slate-700/60 flex items-center justify-between text-[10px] text-slate-400">
                      <div className="flex items-center space-x-1.5">
                        <span
                          style={{ backgroundColor: preset.backgroundColor }}
                          className="w-3 h-3 rounded-full border border-slate-600 inline-block"
                        />
                        <span className="capitalize">{preset.material.replace('_', ' ')}</span>
                      </div>
                      <span className="text-indigo-400 font-medium group-hover:underline">Gunakan Desain →</span>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}
      </div>
    </aside>
  );
};
