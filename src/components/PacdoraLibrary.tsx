import { useState } from 'react';
import type { FC } from 'react';
import {
  Search,
  ChevronDown,
  ChevronRight,
  RotateCw,
} from 'lucide-react';
import { MOCKUP_CATALOG } from '../utils/mockupCatalogData';
import type { MockupCardItem } from '../utils/mockupCatalogData';
import type { PackagingModelId } from '../types/packaging';

interface PacdoraLibraryProps {
  onSelectMockup: (item: MockupCardItem) => void;
  onOpenEditor: () => void;
  activeModelId?: PackagingModelId;
}

export const PacdoraLibrary: FC<PacdoraLibraryProps> = ({
  onSelectMockup,
  onOpenEditor,
}) => {
  const [selectedCategory, setSelectedCategory] = useState<string>('pouches');
  const [searchQuery, setSearchQuery] = useState('');
  const [expandedCats, setExpandedCats] = useState<Record<string, boolean>>({
    boxes: false,
    bottles: false,
    food: false,
    pouches: true, // Expanded by default like in Screenshot 177!
    cans: false,
    jars: false,
    tubes: false,
    cups: false,
    apparel: false,
  });

  const toggleCategory = (catKey: string) => {
    setExpandedCats((prev) => ({ ...prev, [catKey]: !prev[catKey] }));
    setSelectedCategory(catKey);
  };

  const categories = [
    { key: 'all', label: 'All', icon: '📦' },
    { key: 'boxes', label: 'Boxes', icon: '📦', hasSub: true },
    { key: 'bottles', label: 'Bottles', icon: '🧴', hasSub: true },
    { key: 'food', label: 'Food Packaging', icon: '🥡', hasSub: true },
    { key: 'pouches', label: 'Pouches & Sachets & Bags', icon: '👝', hasSub: true },
    { key: 'cans', label: 'Cans', icon: '🥫', hasSub: true },
    { key: 'jars', label: 'Jars', icon: '🏺', hasSub: true },
    { key: 'tubes', label: 'Tubes', icon: '🧴', hasSub: true },
    { key: 'cups', label: 'Containers & Cups & Bowls', icon: '☕', hasSub: true },
    { key: 'apparel', label: 'Apparel', icon: '👕', hasSub: true },
  ];

  const filteredMockups = MOCKUP_CATALOG.filter((item) => {
    const matchesCat =
      selectedCategory === 'all' || item.categorySlug === selectedCategory;
    const matchesSearch =
      searchQuery === '' ||
      item.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      item.category.toLowerCase().includes(searchQuery.toLowerCase()) ||
      item.dimensionsText.includes(searchQuery);
    return matchesCat && matchesSearch;
  });

  return (
    <div className="flex-1 flex overflow-hidden bg-[#f8fafc] text-slate-800 font-sans select-none">
      {/* Left Sidebar Category Tree (Identical to Screenshot 177) */}
      <aside className="w-64 border-r border-slate-200 bg-white flex flex-col h-full shrink-0 overflow-y-auto py-4 px-3">
        <div className="space-y-1">
          {categories.map((cat) => {
            const isSelected = selectedCategory === cat.key;
            const isExpanded = expandedCats[cat.key];

            return (
              <div key={cat.key}>
                <button
                  onClick={() => {
                    if (cat.hasSub) {
                      toggleCategory(cat.key);
                    } else {
                      setSelectedCategory(cat.key);
                    }
                  }}
                  className={`w-full flex items-center justify-between px-3 py-2.5 rounded-lg text-sm font-medium transition ${
                    isSelected
                      ? 'bg-slate-100 text-slate-900 font-semibold'
                      : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
                  }`}
                >
                  <div className="flex items-center space-x-3">
                    <span className="text-base">{cat.icon}</span>
                    <span>{cat.label}</span>
                  </div>
                  {cat.hasSub && (
                    <span className="text-slate-400">
                      {isExpanded ? (
                        <ChevronDown className="w-4 h-4" />
                      ) : (
                        <ChevronRight className="w-4 h-4" />
                      )}
                    </span>
                  )}
                </button>

                {/* Sub-items for Pouches (When expanded) */}
                {cat.key === 'pouches' && isExpanded && (
                  <div className="ml-8 pl-2 border-l border-slate-200 space-y-1 my-1">
                    {[
                      'Stand-up Pouch',
                      'Zipper Pouch',
                      'Coffee Bag',
                      'Tea Pouch',
                      'Snack Pouch',
                    ].map((sub) => (
                      <button
                        key={sub}
                        onClick={() => setSelectedCategory('pouches')}
                        className="w-full text-left px-2 py-1.5 text-xs text-slate-500 hover:text-indigo-600 rounded transition"
                      >
                        {sub}
                      </button>
                    ))}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </aside>

      {/* Main Content Area (Screenshot 177 Mockup Grid) */}
      <main className="flex-1 flex flex-col overflow-hidden">
        {/* Search & Header Bar */}
        <div className="h-16 px-8 border-b border-slate-200 bg-white flex items-center justify-between shrink-0">
          <div>
            <h1 className="text-xl font-bold text-slate-900">
              {categories.find((c) => c.key === selectedCategory)?.label || 'Mockups Library'}
            </h1>
            <span className="text-xs text-slate-500">
              Showing {filteredMockups.length} 3D packaging mockup templates
            </span>
          </div>

          <div className="flex items-center space-x-3">
            <div className="relative w-72">
              <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
              <input
                type="text"
                placeholder="Search mockups (e.g. pouch, can, box)..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-9 pr-3 py-2 bg-slate-100 border border-slate-200 rounded-lg text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:border-indigo-500 focus:bg-white"
              />
            </div>

            <button
              onClick={onOpenEditor}
              className="px-4 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-xs shadow-sm transition flex items-center space-x-1.5"
            >
              <span>Go to 3D Editor →</span>
            </button>
          </div>
        </div>

        {/* Mockups Card Grid (Screenshot 177) */}
        <div className="flex-1 overflow-y-auto p-8 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          {filteredMockups.map((item) => (
            <div
              key={item.id}
              onClick={() => {
                onSelectMockup(item);
                onOpenEditor();
              }}
              className="group cursor-pointer flex flex-col bg-white rounded-2xl border border-slate-200 overflow-hidden hover:shadow-xl hover:border-indigo-400/80 transition-all duration-200 transform hover:-translate-y-1"
            >
                {/* 3D Visual Preview Area */}
                <div className="relative h-60 bg-[#f1f5f9] flex items-center justify-center p-6 overflow-hidden">
                  {/* Top-Left Circular 3D Rotation Badge (Screenshot 177) */}
                  {item.is3D && (
                    <div className="absolute top-3 left-3 flex items-center justify-center w-8 h-8 rounded-full bg-white/90 shadow-sm border border-slate-200/80 text-[10px] font-bold text-slate-700">
                      <div className="flex items-center space-x-0.5">
                        <span>3D</span>
                        <RotateCw className="w-2.5 h-2.5 text-slate-400" />
                      </div>
                    </div>
                  )}

                  {/* Packaging Visual representation */}
                  <div className="text-7xl group-hover:scale-110 transition-transform duration-300 drop-shadow-lg">
                    {item.thumbnailSvg}
                  </div>

                  {/* Hover "Customize in 3D" Pill */}
                  <div className="absolute inset-0 bg-slate-900/10 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                    <span className="px-4 py-2 rounded-full bg-indigo-600 text-white font-semibold text-xs shadow-lg">
                      Open 3D Mockup ↗
                    </span>
                  </div>
                </div>

                {/* Card Meta & Material Swatches (Screenshot 177) */}
                <div className="p-4 flex flex-col space-y-2">
                  <h3 className="font-semibold text-sm text-slate-800 line-clamp-1 group-hover:text-indigo-600 transition">
                    {item.title}
                  </h3>

                  <div className="flex items-center justify-between">
                    {/* Spherical Material Swatches (Screenshot 177) */}
                    <div className="flex items-center space-x-1.5">
                      {item.colorSwatches.map((swatch, idx) => (
                        <span
                          key={idx}
                          style={{
                            background: `radial-gradient(circle at 35% 35%, #ffffff, ${swatch})`,
                          }}
                          className="w-4 h-4 rounded-full border border-slate-300 shadow-inner inline-block"
                        />
                      ))}
                    </div>

                    <span className="font-mono text-[11px] text-slate-400">
                      {item.dimensionsText}
                    </span>
                  </div>
                </div>
              </div>
            ))}
        </div>
      </main>
    </div>
  );
};
