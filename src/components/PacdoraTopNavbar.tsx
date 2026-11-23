import type { FC } from 'react';
import {
  Menu,
  Pipette,
  Share2,
  ExternalLink,
  Globe,
  Download,
  ArrowLeft,
} from 'lucide-react';
import type { PackagingStudioState } from '../hooks/usePackagingStudio';

interface PacdoraTopNavbarProps {
  studio: PackagingStudioState;
  activeView: 'library' | 'editor';
  onNavigate: (view: 'library' | 'editor') => void;
  lang: string;
  onToggleLang: () => void;
}

export const PacdoraTopNavbar: FC<PacdoraTopNavbarProps> = ({
  studio,
  activeView,
  onNavigate,
  lang,
  onToggleLang,
}) => {
  const { setIsExportModalOpen } = studio;

  if (activeView === 'library') {
    // ================= NAVBAR FOR LIBRARY (Screenshot 177) =================
    return (
      <header className="h-16 border-b border-slate-200 bg-white px-6 flex items-center justify-between z-30 select-none">
        {/* Left: Pacdora Logo (Screenshot 177) */}
        <div className="flex items-center space-x-8">
          <div
            onClick={() => onNavigate('library')}
            className="flex items-center space-x-2 cursor-pointer group"
          >
            {/* Pacdora Circular Logo 'd' */}
            <div className="w-8 h-8 rounded-full bg-slate-900 flex items-center justify-center text-white font-black text-lg tracking-tighter">
              d
            </div>
            <span className="text-xl font-bold tracking-tight text-slate-900 font-sans">
              pacdora
            </span>
          </div>

          {/* Navigation Links (Screenshot 177) */}
          <nav className="hidden md:flex items-center space-x-7 text-sm font-medium text-slate-600">
            <button
              onClick={() => onNavigate('library')}
              className="py-5 border-b-2 border-slate-900 text-slate-900 font-semibold"
            >
              Mockups
            </button>
            <button
              onClick={() => onNavigate('editor')}
              className="py-5 hover:text-slate-900 transition"
            >
              Dieline Templates
            </button>
            <button className="py-5 hover:text-slate-900 transition">
              AI Creation
            </button>
            <button className="py-5 hover:text-slate-900 transition">
              Tools
            </button>
            <button className="py-5 hover:text-slate-900 transition">
              Business
            </button>
            <button className="py-5 hover:text-slate-900 transition">
              Pricing
            </button>
          </nav>
        </div>

        {/* Right: Language & Log in (Screenshot 177) */}
        <div className="flex items-center space-x-4 text-xs font-semibold">
          <button
            onClick={onToggleLang}
            className="flex items-center space-x-1.5 text-slate-700 hover:text-slate-950 transition"
          >
            <Globe className="w-4 h-4 text-slate-400" />
            <span className="uppercase">{lang === 'id' ? 'Indonesia' : 'English'} ▾</span>
          </button>

          <span className="text-slate-300">|</span>

          <button
            onClick={() => onNavigate('editor')}
            className="px-5 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-white font-bold transition shadow-sm"
          >
            Open 3D Studio
          </button>
        </div>
      </header>
    );
  }

  // ================= NAVBAR FOR DETAIL EDITOR (Screenshot 176) =================
  return (
    <header className="h-14 border-b border-slate-200 bg-white px-4 flex items-center justify-between z-30 select-none shadow-sm">
      {/* Left: Pacdora Logo 'd' + Mockup Generator + Menu Icons (Screenshot 176) */}
      <div className="flex items-center space-x-4">
        {/* Back to Library */}
        <button
          onClick={() => onNavigate('library')}
          className="p-1.5 rounded-lg hover:bg-slate-100 text-slate-600 transition"
          title="Back to Mockups Catalog"
        >
          <ArrowLeft className="w-4 h-4" />
        </button>

        {/* Brand Circle 'd' */}
        <div
          onClick={() => onNavigate('library')}
          className="w-7 h-7 rounded-full bg-slate-900 flex items-center justify-center text-white font-black text-sm cursor-pointer"
        >
          d
        </div>

        <span className="text-sm font-bold text-slate-900 tracking-tight">
          Mockup Generator
        </span>

        <button className="p-1.5 rounded-lg hover:bg-slate-100 text-slate-600 transition">
          <Menu className="w-4 h-4" />
        </button>

        <button className="p-1.5 rounded-lg hover:bg-slate-100 text-slate-600 transition">
          <Pipette className="w-4 h-4" />
        </button>
      </div>

      {/* Right: 3D Design, Share, Super Export (Screenshot 176) */}
      <div className="flex items-center space-x-3 text-xs font-semibold">
        {/* 3D Design ↗ button (Screenshot 176) */}
        <button
          onClick={() => {
            studio.setViewMode('2d');
          }}
          className="hidden sm:flex items-center space-x-1.5 px-3.5 py-1.5 rounded-xl border border-slate-300 text-slate-800 hover:bg-slate-50 transition"
        >
          <span>3D Design</span>
          <ExternalLink className="w-3.5 h-3.5 text-slate-500" />
        </button>

        {/* Share Button (Screenshot 176) */}
        <button className="p-2 rounded-xl border border-slate-200 text-slate-600 hover:bg-slate-50 transition">
          <Share2 className="w-4 h-4" />
        </button>

        {/* Super Export Button (Screenshot 176 - Bold Purple Pill!) */}
        <button
          onClick={() => setIsExportModalOpen(true)}
          className="px-5 py-2 rounded-xl bg-purple-600 hover:bg-purple-700 text-white font-bold text-xs shadow-md shadow-purple-600/30 transition transform active:scale-95 flex items-center space-x-1.5"
        >
          <Download className="w-3.5 h-3.5" />
          <span>Super export</span>
        </button>
      </div>
    </header>
  );
};
