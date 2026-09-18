import { useState } from 'react';
import type { FC } from 'react';
import { Search, X, Check, ArrowRight } from 'lucide-react';
import type { PackagingStudioState } from '../hooks/usePackagingStudio';
import { PACKAGING_MODELS } from '../utils/packagingModels';
import type { PackagingCategory } from '../types/packaging';

interface TemplateModalProps {
  studio: PackagingStudioState;
}

export const TemplateModal: FC<TemplateModalProps> = ({ studio }) => {
  const {
    isTemplateModalOpen,
    setIsTemplateModalOpen,
    currentModelId,
    setModel,
  } = studio;

  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<'all' | PackagingCategory>('all');

  if (!isTemplateModalOpen) return null;

  const allModels = Object.values(PACKAGING_MODELS);

  const filtered = allModels.filter((m) => {
    const matchesCategory = selectedCategory === 'all' || m.category === selectedCategory;
    const matchesSearch =
      m.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      m.nameEn.toLowerCase().includes(searchQuery.toLowerCase()) ||
      m.description.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesCategory && matchesSearch;
  });

  const categories: { id: 'all' | PackagingCategory; label: string }[] = [
    { id: 'all', label: 'Semua Kategori' },
    { id: 'boxes', label: 'Kotak & Kardus' },
    { id: 'bottles', label: 'Botol & Kaleng' },
    { id: 'pouches', label: 'Pouch & Tas' },
    { id: 'cups_tubes', label: 'Gelas & Tube' },
  ];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/75 backdrop-blur-sm select-none">
      <div className="bg-[#12151f] border border-slate-800 rounded-2xl w-full max-w-4xl max-h-[85vh] flex flex-col shadow-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-150">
        {/* Header */}
        <div className="px-6 py-4 border-b border-slate-800 flex items-center justify-between">
          <div>
            <h2 className="text-base font-bold text-white flex items-center space-x-2">
              <span>Katalog Model Kemasan 3D</span>
              <span className="text-xs px-2 py-0.5 rounded-full bg-indigo-500/20 text-indigo-400 border border-indigo-500/30">
                Pacdora Library
              </span>
            </h2>
            <p className="text-xs text-slate-400 mt-0.5">
              Pilih template kemasan 3D parametrik untuk membuat mockup dan jaring-jaring dieline.
            </p>
          </div>
          <button
            onClick={() => setIsTemplateModalOpen(false)}
            className="p-2 rounded-lg bg-slate-800/80 hover:bg-slate-700 text-slate-400 hover:text-white transition"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Filter Bar & Search */}
        <div className="px-6 py-3 border-b border-slate-800 bg-[#0e111a] flex flex-col sm:flex-row items-center justify-between gap-3">
          {/* Search Input */}
          <div className="relative w-full sm:w-72">
            <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
            <input
              type="text"
              placeholder="Cari kemasan (contoh: mailer, kaleng, cup)..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-9 pr-3 py-1.5 bg-slate-900 border border-slate-700/80 rounded-lg text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-indigo-500"
            />
          </div>

          {/* Category Tabs */}
          <div className="flex items-center space-x-1 overflow-x-auto w-full sm:w-auto">
            {categories.map((c) => (
              <button
                key={c.id}
                onClick={() => setSelectedCategory(c.id)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition whitespace-nowrap ${
                  selectedCategory === c.id
                    ? 'bg-indigo-600 text-white shadow-sm'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'
                }`}
              >
                {c.label}
              </button>
            ))}
          </div>
        </div>

        {/* Grid of Mockup Cards */}
        <div className="flex-1 overflow-y-auto p-6 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filtered.map((model) => {
            const isCurrent = model.id === currentModelId;
            return (
              <div
                key={model.id}
                onClick={() => {
                  setModel(model.id);
                  setIsTemplateModalOpen(false);
                }}
                className={`p-4 rounded-xl border flex flex-col justify-between transition cursor-pointer group relative ${
                  isCurrent
                    ? 'bg-indigo-950/30 border-indigo-500 ring-1 ring-indigo-500'
                    : 'bg-slate-900/60 border-slate-800 hover:border-indigo-500/80 hover:bg-slate-800/60'
                }`}
              >
                <div>
                  <div className="flex items-center justify-between mb-3">
                    <span className="text-3xl p-2.5 rounded-xl bg-slate-800/80 border border-slate-700/60 inline-block group-hover:scale-110 transition">
                      {model.thumbnail}
                    </span>
                    {isCurrent ? (
                      <span className="flex items-center space-x-1 px-2 py-0.5 rounded-full bg-indigo-500/20 text-indigo-400 border border-indigo-500/30 text-[10px] font-semibold">
                        <Check className="w-3 h-3" />
                        <span>Aktif</span>
                      </span>
                    ) : (
                      <span className="text-[10px] text-slate-500 bg-slate-800/60 px-2 py-0.5 rounded">
                        {model.categoryName}
                      </span>
                    )}
                  </div>

                  <h3 className="font-semibold text-sm text-slate-100 group-hover:text-indigo-400 transition">
                    {model.name}
                  </h3>
                  <span className="text-[11px] text-slate-500 font-mono block mb-2">
                    {model.nameEn}
                  </span>

                  <p className="text-xs text-slate-400 line-clamp-2 leading-relaxed">
                    {model.description}
                  </p>
                </div>

                <div className="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs">
                  <span className="text-slate-400 font-mono text-[11px]">
                    {model.defaultDimensions.width}×{model.defaultDimensions.height}×{model.defaultDimensions.depth}mm
                  </span>
                  <span className="text-indigo-400 font-medium flex items-center space-x-1 group-hover:translate-x-0.5 transition">
                    <span>Gunakan</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
