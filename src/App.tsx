import { useState, useRef, useEffect } from 'react';
import { usePackagingStudio } from './hooks/usePackagingStudio';
import { useTranslations } from './hooks/useTranslations';
import { PacdoraTopNavbar } from './components/PacdoraTopNavbar';
import { PacdoraLibrary } from './components/PacdoraLibrary';
import { PacdoraEditor } from './components/PacdoraEditor';
import { ExportModal } from './components/ExportModal';
import type { Viewport3DRef } from './components/Viewport3D';
import type { MockupCardItem } from './utils/mockupCatalogData';

export function App() {
  const studio = usePackagingStudio();
  const { lang, toggleLanguage } = useTranslations();
  const viewportRef = useRef<Viewport3DRef | null>(null);

  // Synchronized Dieline Canvas state
  const [dielineCanvas, setDielineCanvas] = useState<HTMLCanvasElement | null>(null);

  // Active top-level view: 'library' (Screenshot 177) vs 'editor' (Screenshot 176)
  // Default to 'editor' so the user immediately sees the active 3D Mockup Generator!
  const [currentView, setCurrentView] = useState<'library' | 'editor'>('editor');

  // When a mockup is chosen from the Library (Screenshot 177)
  const handleSelectMockup = (item: MockupCardItem) => {
    studio.setModel(item.modelId);
    studio.setDimensions({
      width: item.dims.width,
      height: item.dims.height,
      depth: item.dims.depth,
      radius: item.modelId === 'beverage_can' || item.modelId === 'dropper_bottle' ? item.dims.width / 2 : undefined,
    });
    studio.setMaterial(item.defaultMaterial);
    setCurrentView('editor');
  };

  // Keyboard Shortcuts (Undo, Redo, Delete)
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      const activeEl = document.activeElement;
      const isInput =
        activeEl?.tagName === 'INPUT' ||
        activeEl?.tagName === 'TEXTAREA' ||
        activeEl?.tagName === 'SELECT';

      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'z') {
        if (e.shiftKey) {
          e.preventDefault();
          studio.redo();
        } else {
          e.preventDefault();
          studio.undo();
        }
      } else if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'y') {
        e.preventDefault();
        studio.redo();
      }

      if ((e.key === 'Delete' || e.key === 'Backspace') && !isInput && studio.selectedLayerId) {
        e.preventDefault();
        studio.removeLayer(studio.selectedLayerId);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [studio]);

  return (
    <div className="w-screen h-screen flex flex-col bg-[#f1f5f9] text-slate-900 overflow-hidden font-sans">
      {/* Top Navbar matching Screenshot 177 & 176 */}
      <PacdoraTopNavbar
        studio={studio}
        activeView={currentView}
        onNavigate={(v) => setCurrentView(v)}
        lang={lang}
        onToggleLang={toggleLanguage}
      />

      {/* Main View Area */}
      <div className="flex-1 flex overflow-hidden relative">
        {currentView === 'library' ? (
          /* ================= SCREENSHOT 177: MOCKUPS LIBRARY ================= */
          <PacdoraLibrary
            onSelectMockup={handleSelectMockup}
            onOpenEditor={() => setCurrentView('editor')}
            activeModelId={studio.currentModelId}
          />
        ) : (
          /* ================= SCREENSHOT 176: MOCKUP DETAIL EDITOR ================= */
          <PacdoraEditor
            studio={studio}
            viewportRef={viewportRef}
            dielineCanvas={dielineCanvas}
            onCanvasRendered={(canvas) => setDielineCanvas(canvas)}
            onOpenLibrary={() => setCurrentView('library')}
          />
        )}
      </div>

      {/* Super Export Modal (Triggered by Purple "Super export" button) */}
      <ExportModal
        studio={studio}
        viewportRef={viewportRef}
        dielineCanvas={dielineCanvas}
      />
    </div>
  );
}

export default App;
