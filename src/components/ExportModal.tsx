import { useState } from 'react';
import type { FC, RefObject } from 'react';
import confetti from 'canvas-confetti';
import {
  Download,
  X,
  Camera,
  Film,
  Box,
  FileCode,
  Check,
  Loader2,
} from 'lucide-react';
import type { PackagingStudioState } from '../hooks/usePackagingStudio';
import { PACKAGING_MODELS } from '../utils/packagingModels';
import { generateDielineSVG } from '../utils/dielines';
import type { Viewport3DRef } from './Viewport3D';

interface ExportModalProps {
  studio: PackagingStudioState;
  viewportRef: RefObject<Viewport3DRef | null>;
  dielineCanvas: HTMLCanvasElement | null;
}

export const ExportModal: FC<ExportModalProps> = ({ studio, viewportRef, dielineCanvas }) => {
  const {
    isExportModalOpen,
    setIsExportModalOpen,
    currentModelId,
    dimensions,
  } = studio;

  const currentModel = PACKAGING_MODELS[currentModelId];

  // Active Export Tab
  const [activeTab, setActiveTab] = useState<'render' | 'dieline' | 'video' | 'gltf'>('render');

  // Render settings
  const [renderRes, setRenderRes] = useState<'1080p' | '2k' | '4k'>('2k');
  const [renderFormat, setRenderFormat] = useState<'png' | 'jpeg' | 'webp'>('png');
  const [renderTransparent, setRenderTransparent] = useState(false);
  const [previewImage, setPreviewImage] = useState<string | null>(null);
  const [isRendering, setIsRendering] = useState(false);

  // Video recording settings
  const [isRecording, setIsRecording] = useState(false);
  const [recordProgress, setRecordProgress] = useState(0);

  if (!isExportModalOpen) return null;

  const resolutionConfig = {
    '1080p': { width: 1920, height: 1080, label: 'Full HD (1920 × 1080)' },
    '2k': { width: 2048, height: 2048, label: '2K Square (2048 × 2048)' },
    '4k': { width: 3840, height: 2160, label: '4K Ultra HD (3840 × 2160)' },
  };

  // Generate snapshot preview
  const handleGeneratePreview = () => {
    if (!viewportRef.current) return;
    setIsRendering(true);
    setTimeout(() => {
      const res = resolutionConfig[renderRes];
      const dataUrl = viewportRef.current?.captureSnapshot(res.width, res.height, renderTransparent);
      if (dataUrl) setPreviewImage(dataUrl);
      setIsRendering(false);
    }, 100);
  };

  // Download high-resolution rendered image
  const handleDownloadRender = () => {
    if (!viewportRef.current) return;
    setIsRendering(true);

    setTimeout(() => {
      const res = resolutionConfig[renderRes];
      const dataUrl = viewportRef.current?.captureSnapshot(res.width, res.height, renderTransparent);
      if (dataUrl) {
        const link = document.createElement('a');
        link.download = `Pacdora_${currentModelId}_mockup_${renderRes}.${renderFormat === 'jpeg' ? 'jpg' : renderFormat}`;
        link.href = dataUrl;
        link.click();

        // Celebration Confetti
        confetti({
          particleCount: 80,
          spread: 70,
          origin: { y: 0.6 },
        });
      }
      setIsRendering(false);
    }, 150);
  };

  // Download Dieline Vector SVG
  const handleDownloadDielineSVG = () => {
    const svgString = generateDielineSVG(
      currentModelId,
      dimensions,
      currentModel.textureWidth,
      currentModel.textureHeight
    );
    const blob = new Blob([svgString], { type: 'image/svg+xml;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.download = `Pacdora_${currentModelId}_dieline_spec.svg`;
    link.href = url;
    link.click();
    URL.revokeObjectURL(url);

    confetti({ particleCount: 50, spread: 60 });
  };

  // Download Dieline High-Res PNG
  const handleDownloadDielinePNG = () => {
    if (!dielineCanvas) return;
    const url = dielineCanvas.toDataURL('image/png');
    const link = document.createElement('a');
    link.download = `Pacdora_${currentModelId}_dieline_print.png`;
    link.href = url;
    link.click();

    confetti({ particleCount: 50, spread: 60 });
  };

  // Record 360 Turntable Video
  const handleRecord360 = async () => {
    if (!viewportRef.current || isRecording) return;
    setIsRecording(true);
    setRecordProgress(0);

    try {
      const videoBlob = await viewportRef.current.record360Video(4500, (p) => {
        setRecordProgress(Math.round(p * 100));
      });

      const url = URL.createObjectURL(videoBlob);
      const link = document.createElement('a');
      link.download = `Pacdora_${currentModelId}_turntable_360.webm`;
      link.href = url;
      link.click();
      URL.revokeObjectURL(url);

      confetti({ particleCount: 80, spread: 80 });
    } catch (err) {
      console.error('Failed to record video:', err);
    } finally {
      setIsRecording(false);
    }
  };

  // Download 3D Model glTF/GLB
  const handleDownloadGLTF = async () => {
    if (!viewportRef.current) return;
    try {
      const blob = await viewportRef.current.exportGLTF();
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.download = `Pacdora_${currentModelId}_3d_model.glb`;
      link.href = url;
      link.click();
      URL.revokeObjectURL(url);

      confetti({ particleCount: 70, spread: 70 });
    } catch (err) {
      console.error('GLTF Export failed:', err);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md select-none">
      <div className="bg-[#12151f] border border-slate-800 rounded-2xl w-full max-w-3xl max-h-[90vh] flex flex-col shadow-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-150">
        {/* Modal Header */}
        <div className="px-6 py-4 border-b border-slate-800 flex items-center justify-between">
          <div className="flex items-center space-x-2.5">
            <div className="w-8 h-8 rounded-lg bg-indigo-600/20 text-indigo-400 border border-indigo-500/30 flex items-center justify-center">
              <Download className="w-4 h-4" />
            </div>
            <div>
              <h2 className="text-base font-bold text-white">Ekspor & Render Packaging</h2>
              <p className="text-xs text-slate-400 mt-0.5">
                Download mockup 3D fotorealistik resolusi tinggi, pola dieline CAD, atau model 3D glTF.
              </p>
            </div>
          </div>
          <button
            onClick={() => setIsExportModalOpen(false)}
            className="p-2 rounded-lg bg-slate-800/80 hover:bg-slate-700 text-slate-400 hover:text-white transition"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Export Navigation Tabs */}
        <div className="flex border-b border-slate-800 bg-[#0e111a] px-6 text-xs font-medium">
          <button
            onClick={() => setActiveTab('render')}
            className={`flex items-center space-x-2 py-3 border-b-2 transition ${
              activeTab === 'render'
                ? 'border-indigo-500 text-indigo-400 font-semibold'
                : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            <Camera className="w-4 h-4" />
            <span>Render Gambar 4K</span>
          </button>

          <button
            onClick={() => setActiveTab('dieline')}
            className={`flex items-center space-x-2 py-3 border-b-2 transition ml-6 ${
              activeTab === 'dieline'
                ? 'border-indigo-500 text-indigo-400 font-semibold'
                : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            <FileCode className="w-4 h-4" />
            <span>Jaring-jaring Dieline (SVG/CAD)</span>
          </button>

          <button
            onClick={() => setActiveTab('video')}
            className={`flex items-center space-x-2 py-3 border-b-2 transition ml-6 ${
              activeTab === 'video'
                ? 'border-indigo-500 text-indigo-400 font-semibold'
                : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            <Film className="w-4 h-4" />
            <span>Video 360° Turntable</span>
          </button>

          <button
            onClick={() => setActiveTab('gltf')}
            className={`flex items-center space-x-2 py-3 border-b-2 transition ml-6 ${
              activeTab === 'gltf'
                ? 'border-indigo-500 text-indigo-400 font-semibold'
                : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            <Box className="w-4 h-4" />
            <span>Model 3D (glTF/GLB)</span>
          </button>
        </div>

        {/* Tab Body */}
        <div className="flex-1 overflow-y-auto p-6">
          {/* ================= TAB 1: RENDER 4K ================= */}
          {activeTab === 'render' && (
            <div className="space-y-5">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
                {/* Options Column */}
                <div className="space-y-4">
                  {/* Resolution Selector */}
                  <div className="space-y-2">
                    <span className="text-xs font-semibold text-slate-300 uppercase tracking-wider block">
                      Resolusi Gambar
                    </span>
                    <div className="space-y-2">
                      {(['1080p', '2k', '4k'] as const).map((r) => (
                        <label
                          key={r}
                          onClick={() => setRenderRes(r)}
                          className={`p-3 rounded-xl border flex items-center justify-between cursor-pointer transition ${
                            renderRes === r
                              ? 'bg-indigo-600/15 border-indigo-500 text-white'
                              : 'bg-slate-900/60 border-slate-800 text-slate-300 hover:bg-slate-800'
                          }`}
                        >
                          <div>
                            <span className="text-xs font-semibold block uppercase">
                              {r === '1080p' ? 'Full HD 1080p' : r === '2k' ? '2K Square (Instagram)' : '4K Ultra HD (Print)'}
                            </span>
                            <span className="text-[11px] text-slate-400 font-mono">
                              {resolutionConfig[r].width} × {resolutionConfig[r].height} px
                            </span>
                          </div>
                          {renderRes === r && <Check className="w-4 h-4 text-indigo-400" />}
                        </label>
                      ))}
                    </div>
                  </div>

                  {/* Format & Transparent Toggle */}
                  <div className="grid grid-cols-2 gap-3 pt-1">
                    <div className="space-y-1">
                      <span className="text-xs font-medium text-slate-300">Format File</span>
                      <select
                        value={renderFormat}
                        onChange={(e) => setRenderFormat(e.target.value as any)}
                        className="w-full px-2.5 py-2 bg-slate-900 border border-slate-700 rounded-lg text-xs text-slate-200 focus:outline-none focus:border-indigo-500"
                      >
                        <option value="png">PNG (Lossless)</option>
                        <option value="jpeg">JPG (Standard)</option>
                        <option value="webp">WebP (Modern Web)</option>
                      </select>
                    </div>

                    <div className="space-y-1">
                      <span className="text-xs font-medium text-slate-300">Latar Transparan</span>
                      <label className="flex items-center space-x-2 h-9 px-2 bg-slate-900 border border-slate-700 rounded-lg text-xs cursor-pointer">
                        <input
                          type="checkbox"
                          checked={renderTransparent}
                          onChange={(e) => setRenderTransparent(e.target.checked)}
                          className="rounded bg-slate-800 border-slate-600 text-indigo-600 focus:ring-0 w-3.5 h-3.5"
                        />
                        <span className="text-slate-300 text-[11px]">Transparan PNG</span>
                      </label>
                    </div>
                  </div>
                </div>

                {/* Preview Box Column */}
                <div className="flex flex-col items-center justify-center border border-slate-800 rounded-xl bg-slate-950/60 p-4 min-h-[220px]">
                  {previewImage ? (
                    <div className="relative w-full h-full flex flex-col items-center justify-center">
                      <img
                        src={previewImage}
                        alt="Render Snapshot"
                        className="max-h-52 object-contain rounded-lg shadow-md border border-slate-800"
                      />
                      <span className="text-[10px] text-slate-500 mt-2 font-mono">
                        Preview ({resolutionConfig[renderRes].width}×{resolutionConfig[renderRes].height})
                      </span>
                    </div>
                  ) : (
                    <div className="text-center space-y-2 text-slate-500">
                      <Camera className="w-10 h-10 mx-auto text-slate-600" />
                      <p className="text-xs">Klik tombol di bawah untuk membuat preview render seketika</p>
                      <button
                        onClick={handleGeneratePreview}
                        disabled={isRendering}
                        className="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium transition"
                      >
                        {isRendering ? 'Memproses...' : 'Generate Preview'}
                      </button>
                    </div>
                  )}
                </div>
              </div>

              {/* Action Button */}
              <div className="pt-2 border-t border-slate-800/80 flex items-center justify-between">
                <span className="text-xs text-slate-400">
                  Kemasan: <strong className="text-slate-200">{currentModel.name}</strong> ({dimensions.width}×{dimensions.height}×{dimensions.depth}mm)
                </span>

                <button
                  onClick={handleDownloadRender}
                  disabled={isRendering}
                  className="flex items-center space-x-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-indigo-600 to-violet-600 hover:from-indigo-500 hover:to-violet-500 text-white font-semibold text-xs shadow-lg shadow-indigo-600/30 transition transform active:scale-95"
                >
                  {isRendering ? (
                    <>
                      <Loader2 className="w-4 h-4 animate-spin" />
                      <span>Merender Resolusi Tinggi...</span>
                    </>
                  ) : (
                    <>
                      <Download className="w-4 h-4" />
                      <span>Download Render {renderRes.toUpperCase()}</span>
                    </>
                  )}
                </button>
              </div>
            </div>
          )}

          {/* ================= TAB 2: DIELINE VECTOR CAD ================= */}
          {activeTab === 'dieline' && (
            <div className="space-y-4">
              <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 space-y-2">
                <h3 className="text-sm font-semibold text-slate-200">
                  Jaring-jaring Kemasan (CAD Dieline Standard)
                </h3>
                <p className="text-xs text-slate-400 leading-relaxed">
                  File ini berisikan pola cetak lembaran datar (unfolded dieline net) dengan standar industri kemasan:
                  garis potong luar (Cut - merah), garis lipat (Crease - biru putus-putus), dan area bleed untuk pisau die-cutting percetakan.
                </p>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
                {/* SVG CAD Card */}
                <div className="p-4 rounded-xl border border-slate-700/80 bg-slate-800/40 space-y-3 flex flex-col justify-between">
                  <div>
                    <div className="flex items-center justify-between mb-2">
                      <span className="font-semibold text-xs text-slate-100">Vector SVG (CAD)</span>
                      <span className="text-[10px] px-2 py-0.5 bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 rounded font-semibold">
                        Industri Percetakan
                      </span>
                    </div>
                    <p className="text-xs text-slate-400">
                      Format vektor presisi tanpa pecah, siap dibuka di Adobe Illustrator, CorelDRAW, atau software laser cutting.
                    </p>
                  </div>

                  <button
                    onClick={handleDownloadDielineSVG}
                    className="w-full flex items-center justify-center space-x-2 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white font-medium text-xs transition shadow"
                  >
                    <Download className="w-3.5 h-3.5" />
                    <span>Download SVG Dieline</span>
                  </button>
                </div>

                {/* High Res PNG Card */}
                <div className="p-4 rounded-xl border border-slate-700/80 bg-slate-800/40 space-y-3 flex flex-col justify-between">
                  <div>
                    <div className="flex items-center justify-between mb-2">
                      <span className="font-semibold text-xs text-slate-100">PNG Resolusi Tinggi</span>
                      <span className="text-[10px] px-2 py-0.5 bg-sky-500/20 text-sky-400 border border-sky-500/30 rounded font-semibold">
                        {currentModel.textureWidth} × {currentModel.textureHeight} px
                      </span>
                    </div>
                    <p className="text-xs text-slate-400">
                      Gambar jaring-jaring lengkap beserta desain grafis, logo, dan barcode yang telah Anda rancang.
                    </p>
                  </div>

                  <button
                    onClick={handleDownloadDielinePNG}
                    className="w-full flex items-center justify-center space-x-2 py-2 rounded-lg bg-slate-700 hover:bg-slate-600 text-white font-medium text-xs transition shadow"
                  >
                    <Download className="w-3.5 h-3.5" />
                    <span>Download PNG Dieline</span>
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* ================= TAB 3: 360° TURNTABLE VIDEO ================= */}
          {activeTab === 'video' && (
            <div className="space-y-4">
              <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 space-y-2">
                <h3 className="text-sm font-semibold text-slate-200">
                  Rekam Animasi Putaran 360° (Turntable)
                </h3>
                <p className="text-xs text-slate-400 leading-relaxed">
                  Menghasilkan video berputar 360 derajat kemasan Anda secara otomatis dalam format WebM berkualitas tinggi, cocok untuk showcase media sosial, website e-commerce, atau presentasi klien.
                </p>
              </div>

              {isRecording ? (
                <div className="p-6 rounded-xl bg-indigo-950/30 border border-indigo-500/50 text-center space-y-3">
                  <Loader2 className="w-8 h-8 mx-auto text-indigo-400 animate-spin" />
                  <span className="text-xs font-semibold text-slate-200 block">
                    Sedang Merekam Putaran 360° ({recordProgress}%)
                  </span>
                  <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                    <div
                      style={{ width: `${recordProgress}%` }}
                      className="bg-indigo-500 h-full transition-all duration-100"
                    />
                  </div>
                  <span className="text-[11px] text-slate-400">
                    Mohon tunggu hingga putaran selesai untuk mengunduh video...
                  </span>
                </div>
              ) : (
                <div className="p-6 rounded-xl border border-slate-800 bg-slate-900/40 text-center space-y-4">
                  <Film className="w-12 h-12 mx-auto text-indigo-400" />
                  <div className="space-y-1">
                    <span className="text-xs font-semibold text-slate-200 block">
                      Durasi Putaran Penuh: ~4.5 Detik (Looping Seamless)
                    </span>
                    <span className="text-[11px] text-slate-400 block">
                      Video direkam langsung dari kanvas 3D WebGL dengan frame rate 30 FPS.
                    </span>
                  </div>

                  <button
                    onClick={handleRecord360}
                    className="inline-flex items-center space-x-2 px-6 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-xs shadow-lg shadow-indigo-600/30 transition transform active:scale-95"
                  >
                    <Film className="w-4 h-4" />
                    <span>Mulai Rekam & Download Video 360°</span>
                  </button>
                </div>
              )}
            </div>
          )}

          {/* ================= TAB 4: 3D MODEL glTF/GLB ================= */}
          {activeTab === 'gltf' && (
            <div className="space-y-4">
              <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 space-y-2">
                <h3 className="text-sm font-semibold text-slate-200">
                  Ekspor Model 3D Universal (.GLB / glTF)
                </h3>
                <p className="text-xs text-slate-400 leading-relaxed">
                  File biner glTF (.glb) mencakup geometri parametrik 3D, koordinat UV, dan tekstur desain yang Anda buat secara terintegrasi (embedded).
                </p>
              </div>

              <div className="p-6 rounded-xl border border-slate-800 bg-slate-900/40 text-center space-y-4">
                <Box className="w-12 h-12 mx-auto text-purple-400" />
                <div className="space-y-1">
                  <span className="text-xs font-semibold text-slate-200 block">
                    Kompatibel dengan Blender, Unity, Unreal Engine, Figma, dan Apple AR QuickLook
                  </span>
                  <span className="text-[11px] text-slate-400 block">
                    Model 3D dapat dianimasikan lebih lanjut atau dimasukkan ke dalam game dan aplikasi augmented reality.
                  </span>
                </div>

                <button
                  onClick={handleDownloadGLTF}
                  className="inline-flex items-center space-x-2 px-6 py-2.5 rounded-xl bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white font-semibold text-xs shadow-lg shadow-purple-600/30 transition transform active:scale-95"
                >
                  <Download className="w-4 h-4" />
                  <span>Download File .GLB (3D Model)</span>
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
