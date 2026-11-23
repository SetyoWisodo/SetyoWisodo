import { useState } from 'react';
import type { FC } from 'react';
import {
  Layers,
  Type,
  Square,
  Image as ImageIcon,
  QrCode,
  Barcode,
  Award,
  Copy,
  Trash2,
  ChevronUp,
  ChevronDown,
  Eye,
  EyeOff,
  AlignLeft,
  AlignCenter,
  AlignRight,
  Palette,
  Sliders,
} from 'lucide-react';
import type { PackagingStudioState } from '../hooks/usePackagingStudio';
import type {
  TextLayer,
  ShapeLayer,
  BarcodeLayer,
  QRCodeLayer,
  BadgeLayer,
} from '../types/packaging';

interface SidebarRightProps {
  studio: PackagingStudioState;
}

export const SidebarRight: FC<SidebarRightProps> = ({ studio }) => {
  const {
    layers,
    selectedLayerId,
    setSelectedLayerId,
    selectedLayer,
    updateLayer,
    removeLayer,
    duplicateLayer,
    reorderLayer,
    backgroundColor,
    setBackgroundColor,
    addTextLayer,
    addBarcodeLayer,
    addQRCodeLayer,
    addBadgeLayer,
  } = studio;

  const [activeRightTab, setActiveRightTab] = useState<'inspector' | 'layers'>('inspector');

  const fontFamilies = [
    'Montserrat',
    'Inter',
    'Poppins',
    'Playfair Display',
    'Bebas Neue',
    'Space Grotesk',
  ];

  return (
    <aside className="w-80 border-l border-slate-800 bg-[#12151e] flex flex-col h-full shrink-0 select-none z-10">
      {/* Top Header Switcher: Properti (Inspector) vs Lapisan (Layers) */}
      <div className="flex border-b border-slate-800 bg-[#0e111a] px-2 py-1 text-xs shrink-0">
        <button
          onClick={() => setActiveRightTab('inspector')}
          className={`flex-1 flex items-center justify-center space-x-1.5 py-2 rounded-lg font-medium transition ${
            activeRightTab === 'inspector'
              ? 'bg-indigo-600/20 text-indigo-400 border border-indigo-500/40 shadow-sm'
              : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          <Sliders className="w-3.5 h-3.5" />
          <span>Properti Elemen</span>
        </button>

        <button
          onClick={() => setActiveRightTab('layers')}
          className={`flex-1 flex items-center justify-center space-x-1.5 py-2 rounded-lg font-medium transition ${
            activeRightTab === 'layers'
              ? 'bg-indigo-600/20 text-indigo-400 border border-indigo-500/40 shadow-sm'
              : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          <Layers className="w-3.5 h-3.5" />
          <span>Lapisan ({layers.length})</span>
        </button>
      </div>

      {/* Main Right Panel Body */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {activeRightTab === 'inspector' && (
          <>
            {selectedLayer ? (
              <div className="space-y-4">
                {/* Selected Layer Header */}
                <div className="flex items-center justify-between border-b border-slate-800 pb-2.5">
                  <div className="flex items-center space-x-2">
                    <div className="p-1 rounded bg-indigo-600/20 text-indigo-400">
                      {selectedLayer.type === 'text' && <Type className="w-3.5 h-3.5" />}
                      {selectedLayer.type === 'shape' && <Square className="w-3.5 h-3.5" />}
                      {selectedLayer.type === 'image' && <ImageIcon className="w-3.5 h-3.5" />}
                      {selectedLayer.type === 'barcode' && <Barcode className="w-3.5 h-3.5" />}
                      {selectedLayer.type === 'qrcode' && <QrCode className="w-3.5 h-3.5" />}
                      {selectedLayer.type === 'badge' && <Award className="w-3.5 h-3.5" />}
                    </div>
                    <span className="text-xs font-semibold text-slate-200 truncate max-w-[140px]">
                      {selectedLayer.name}
                    </span>
                  </div>

                  {/* Actions: Duplicate, Delete */}
                  <div className="flex items-center space-x-1">
                    <button
                      onClick={() => duplicateLayer(selectedLayer.id)}
                      className="p-1.5 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white transition"
                      title="Duplikat Elemen"
                    >
                      <Copy className="w-3.5 h-3.5" />
                    </button>
                    <button
                      onClick={() => removeLayer(selectedLayer.id)}
                      className="p-1.5 rounded bg-slate-800 hover:bg-rose-900/40 text-slate-300 hover:text-rose-400 transition"
                      title="Hapus Elemen"
                    >
                      <Trash2 className="w-3.5 h-3.5" />
                    </button>
                  </div>
                </div>

                {/* ============= TYPE SPECIFIC CONTROLS ============= */}

                {/* TEXT LAYER CONTROLS */}
                {selectedLayer.type === 'text' && (
                  <div className="space-y-3">
                    <div className="space-y-1">
                      <span className="text-[11px] font-medium text-slate-400">Isi Teks</span>
                      <textarea
                        rows={2}
                        value={(selectedLayer as TextLayer).text}
                        onChange={(e) => updateLayer(selectedLayer.id, { text: e.target.value })}
                        className="w-full px-2.5 py-1.5 bg-slate-900 border border-slate-700 rounded-lg text-xs text-slate-100 focus:outline-none focus:border-indigo-500 font-sans"
                      />
                    </div>

                    {/* Font Family & Size */}
                    <div className="grid grid-cols-2 gap-2">
                      <div className="space-y-1">
                        <span className="text-[11px] font-medium text-slate-400">Font</span>
                        <select
                          value={(selectedLayer as TextLayer).fontFamily}
                          onChange={(e) => updateLayer(selectedLayer.id, { fontFamily: e.target.value })}
                          className="w-full px-2 py-1.5 bg-slate-900 border border-slate-700 rounded-lg text-xs text-slate-200 focus:outline-none focus:border-indigo-500"
                        >
                          {fontFamilies.map((f) => (
                            <option key={f} value={f}>
                              {f}
                            </option>
                          ))}
                        </select>
                      </div>

                      <div className="space-y-1">
                        <div className="flex justify-between items-center">
                          <span className="text-[11px] font-medium text-slate-400">Ukuran</span>
                          <span className="font-mono text-[10px] text-indigo-400">
                            {(selectedLayer as TextLayer).fontSize}px
                          </span>
                        </div>
                        <input
                          type="range"
                          min="12"
                          max="160"
                          value={(selectedLayer as TextLayer).fontSize}
                          onChange={(e) =>
                            updateLayer(selectedLayer.id, { fontSize: parseInt(e.target.value) })
                          }
                          className="w-full h-1.5 bg-slate-800 rounded appearance-none cursor-pointer mt-2"
                        />
                      </div>
                    </div>

                    {/* Font Weight & Alignment */}
                    <div className="grid grid-cols-2 gap-2 pt-1">
                      <div className="space-y-1">
                        <span className="text-[11px] font-medium text-slate-400">Ketebalan</span>
                        <select
                          value={(selectedLayer as TextLayer).fontWeight}
                          onChange={(e) =>
                            updateLayer(selectedLayer.id, {
                              fontWeight: e.target.value as any,
                            })
                          }
                          className="w-full px-2 py-1.5 bg-slate-900 border border-slate-700 rounded-lg text-xs text-slate-200 focus:outline-none focus:border-indigo-500"
                        >
                          <option value="300">Light (300)</option>
                          <option value="400">Regular (400)</option>
                          <option value="600">Semi Bold (600)</option>
                          <option value="700">Bold (700)</option>
                          <option value="800">Black (800)</option>
                        </select>
                      </div>

                      <div className="space-y-1">
                        <span className="text-[11px] font-medium text-slate-400">Perataan</span>
                        <div className="flex items-center space-x-1 bg-slate-900 border border-slate-700 rounded-lg p-0.5">
                          {(['left', 'center', 'right'] as const).map((align) => (
                            <button
                              key={align}
                              onClick={() => updateLayer(selectedLayer.id, { textAlign: align })}
                              className={`flex-1 py-1 rounded flex items-center justify-center transition ${
                                (selectedLayer as TextLayer).textAlign === align
                                  ? 'bg-indigo-600 text-white'
                                  : 'text-slate-400 hover:text-white'
                              }`}
                            >
                              {align === 'left' && <AlignLeft className="w-3.5 h-3.5" />}
                              {align === 'center' && <AlignCenter className="w-3.5 h-3.5" />}
                              {align === 'right' && <AlignRight className="w-3.5 h-3.5" />}
                            </button>
                          ))}
                        </div>
                      </div>
                    </div>

                    {/* Text Color & Letter Spacing */}
                    <div className="grid grid-cols-2 gap-2 pt-1">
                      <div className="space-y-1">
                        <span className="text-[11px] font-medium text-slate-400">Warna Teks</span>
                        <div className="flex items-center space-x-2 bg-slate-900 border border-slate-700 rounded-lg p-1">
                          <input
                            type="color"
                            value={(selectedLayer as TextLayer).color}
                            onChange={(e) => updateLayer(selectedLayer.id, { color: e.target.value })}
                            className="w-6 h-6 rounded cursor-pointer border-0 bg-transparent"
                          />
                          <span className="font-mono text-xs text-slate-200 uppercase">
                            {(selectedLayer as TextLayer).color}
                          </span>
                        </div>
                      </div>

                      <div className="space-y-1">
                        <div className="flex justify-between items-center">
                          <span className="text-[11px] font-medium text-slate-400">Spasi Huruf</span>
                          <span className="font-mono text-[10px] text-indigo-400">
                            {(selectedLayer as TextLayer).letterSpacing}px
                          </span>
                        </div>
                        <input
                          type="range"
                          min="0"
                          max="20"
                          value={(selectedLayer as TextLayer).letterSpacing}
                          onChange={(e) =>
                            updateLayer(selectedLayer.id, { letterSpacing: parseInt(e.target.value) })
                          }
                          className="w-full h-1.5 bg-slate-800 rounded appearance-none cursor-pointer mt-2"
                        />
                      </div>
                    </div>
                  </div>
                )}

                {/* SHAPE LAYER CONTROLS */}
                {selectedLayer.type === 'shape' && (
                  <div className="space-y-3">
                    <div className="grid grid-cols-2 gap-2">
                      <div className="space-y-1">
                        <span className="text-[11px] font-medium text-slate-400">Warna Isi (Fill)</span>
                        <div className="flex items-center space-x-2 bg-slate-900 border border-slate-700 rounded-lg p-1">
                          <input
                            type="color"
                            value={(selectedLayer as ShapeLayer).fill}
                            onChange={(e) => updateLayer(selectedLayer.id, { fill: e.target.value })}
                            className="w-6 h-6 rounded cursor-pointer border-0 bg-transparent"
                          />
                          <span className="font-mono text-xs text-slate-200 uppercase">
                            {(selectedLayer as ShapeLayer).fill}
                          </span>
                        </div>
                      </div>

                      <div className="space-y-1">
                        <span className="text-[11px] font-medium text-slate-400">Garis Tepi (Stroke)</span>
                        <div className="flex items-center space-x-2 bg-slate-900 border border-slate-700 rounded-lg p-1">
                          <input
                            type="color"
                            value={(selectedLayer as ShapeLayer).strokeColor}
                            onChange={(e) => updateLayer(selectedLayer.id, { strokeColor: e.target.value })}
                            className="w-6 h-6 rounded cursor-pointer border-0 bg-transparent"
                          />
                          <span className="font-mono text-xs text-slate-200 uppercase">
                            {(selectedLayer as ShapeLayer).strokeColor}
                          </span>
                        </div>
                      </div>
                    </div>

                    <div className="space-y-1">
                      <div className="flex justify-between items-center">
                        <span className="text-[11px] font-medium text-slate-400">Tebal Garis</span>
                        <span className="font-mono text-[10px] text-indigo-400">
                          {(selectedLayer as ShapeLayer).strokeWidth}px
                        </span>
                      </div>
                      <input
                        type="range"
                        min="0"
                        max="20"
                        value={(selectedLayer as ShapeLayer).strokeWidth}
                        onChange={(e) =>
                          updateLayer(selectedLayer.id, { strokeWidth: parseInt(e.target.value) })
                        }
                        className="w-full h-1.5 bg-slate-800 rounded appearance-none cursor-pointer"
                      />
                    </div>

                    <div className="grid grid-cols-2 gap-2 pt-1">
                      <div className="space-y-1">
                        <div className="flex justify-between items-center">
                          <span className="text-[11px] font-medium text-slate-400">Lebar</span>
                          <span className="font-mono text-[10px] text-indigo-400">
                            {(selectedLayer as ShapeLayer).width}px
                          </span>
                        </div>
                        <input
                          type="range"
                          min="20"
                          max="800"
                          value={(selectedLayer as ShapeLayer).width}
                          onChange={(e) =>
                            updateLayer(selectedLayer.id, { width: parseInt(e.target.value) })
                          }
                          className="w-full h-1.5 bg-slate-800 rounded appearance-none cursor-pointer"
                        />
                      </div>

                      <div className="space-y-1">
                        <div className="flex justify-between items-center">
                          <span className="text-[11px] font-medium text-slate-400">Tinggi</span>
                          <span className="font-mono text-[10px] text-indigo-400">
                            {(selectedLayer as ShapeLayer).height}px
                          </span>
                        </div>
                        <input
                          type="range"
                          min="4"
                          max="800"
                          value={(selectedLayer as ShapeLayer).height}
                          onChange={(e) =>
                            updateLayer(selectedLayer.id, { height: parseInt(e.target.value) })
                          }
                          className="w-full h-1.5 bg-slate-800 rounded appearance-none cursor-pointer"
                        />
                      </div>
                    </div>
                  </div>
                )}

                {/* BARCODE CONTROLS */}
                {selectedLayer.type === 'barcode' && (
                  <div className="space-y-3">
                    <div className="space-y-1">
                      <span className="text-[11px] font-medium text-slate-400">Nomor Barcode (EAN-13)</span>
                      <input
                        type="text"
                        value={(selectedLayer as BarcodeLayer).code}
                        onChange={(e) => updateLayer(selectedLayer.id, { code: e.target.value })}
                        className="w-full px-2.5 py-1.5 bg-slate-900 border border-slate-700 rounded-lg text-xs font-mono text-slate-100 focus:outline-none focus:border-indigo-500"
                      />
                    </div>

                    <div className="grid grid-cols-2 gap-2">
                      <div className="space-y-1">
                        <span className="text-[11px] font-medium text-slate-400">Warna Garis</span>
                        <input
                          type="color"
                          value={(selectedLayer as BarcodeLayer).color}
                          onChange={(e) => updateLayer(selectedLayer.id, { color: e.target.value })}
                          className="w-full h-8 rounded bg-slate-900 border border-slate-700 cursor-pointer"
                        />
                      </div>

                      <div className="space-y-1">
                        <span className="text-[11px] font-medium text-slate-400">Warna Dasar</span>
                        <input
                          type="color"
                          value={(selectedLayer as BarcodeLayer).bgColor}
                          onChange={(e) => updateLayer(selectedLayer.id, { bgColor: e.target.value })}
                          className="w-full h-8 rounded bg-slate-900 border border-slate-700 cursor-pointer"
                        />
                      </div>
                    </div>
                  </div>
                )}

                {/* QR CODE CONTROLS */}
                {selectedLayer.type === 'qrcode' && (
                  <div className="space-y-3">
                    <div className="space-y-1">
                      <span className="text-[11px] font-medium text-slate-400">Tautan URL / Isi Teks</span>
                      <input
                        type="text"
                        value={(selectedLayer as QRCodeLayer).content}
                        onChange={(e) => updateLayer(selectedLayer.id, { content: e.target.value })}
                        className="w-full px-2.5 py-1.5 bg-slate-900 border border-slate-700 rounded-lg text-xs text-slate-100 focus:outline-none focus:border-indigo-500 font-mono"
                      />
                    </div>

                    <div className="space-y-1">
                      <div className="flex justify-between items-center">
                        <span className="text-[11px] font-medium text-slate-400">Ukuran QR</span>
                        <span className="font-mono text-[10px] text-indigo-400">
                          {(selectedLayer as QRCodeLayer).size}px
                        </span>
                      </div>
                      <input
                        type="range"
                        min="60"
                        max="300"
                        value={(selectedLayer as QRCodeLayer).size}
                        onChange={(e) =>
                          updateLayer(selectedLayer.id, { size: parseInt(e.target.value) })
                        }
                        className="w-full h-1.5 bg-slate-800 rounded appearance-none cursor-pointer"
                      />
                    </div>
                  </div>
                )}

                {/* BADGE CONTROLS */}
                {selectedLayer.type === 'badge' && (
                  <div className="space-y-3">
                    <div className="space-y-1">
                      <span className="text-[11px] font-medium text-slate-400">Tipe Stempel Sertifikasi</span>
                      <select
                        value={(selectedLayer as BadgeLayer).badgeType}
                        onChange={(e) => updateLayer(selectedLayer.id, { badgeType: e.target.value as any })}
                        className="w-full px-2 py-1.5 bg-slate-900 border border-slate-700 rounded-lg text-xs text-slate-200 focus:outline-none focus:border-indigo-500"
                      >
                        <option value="recyclable">♻️ 100% Recyclable</option>
                        <option value="organic">🌿 Certified Organic</option>
                        <option value="halal">🕌 Halal Indonesia</option>
                        <option value="cruelty_free">🐇 Cruelty Free</option>
                        <option value="fsc">🌲 FSC Paper</option>
                        <option value="net_weight">⚖️ Netto 250g</option>
                      </select>
                    </div>

                    <div className="grid grid-cols-2 gap-2">
                      <div className="space-y-1">
                        <span className="text-[11px] font-medium text-slate-400">Warna Stempel</span>
                        <input
                          type="color"
                          value={(selectedLayer as BadgeLayer).color}
                          onChange={(e) => updateLayer(selectedLayer.id, { color: e.target.value })}
                          className="w-full h-8 rounded bg-slate-900 border border-slate-700 cursor-pointer"
                        />
                      </div>

                      <div className="space-y-1">
                        <div className="flex justify-between items-center">
                          <span className="text-[11px] font-medium text-slate-400">Ukuran</span>
                          <span className="font-mono text-[10px] text-indigo-400">
                            {(selectedLayer as BadgeLayer).size}px
                          </span>
                        </div>
                        <input
                          type="range"
                          min="50"
                          max="220"
                          value={(selectedLayer as BadgeLayer).size}
                          onChange={(e) =>
                            updateLayer(selectedLayer.id, { size: parseInt(e.target.value) })
                          }
                          className="w-full h-1.5 bg-slate-800 rounded appearance-none cursor-pointer mt-2"
                        />
                      </div>
                    </div>
                  </div>
                )}

                {/* ============= TRANSFORM & POSITION ============= */}
                <div className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800 space-y-3 pt-2.5">
                  <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block">
                    Posisi & Transformasi
                  </span>

                  {/* Position Coordinates */}
                  <div className="grid grid-cols-2 gap-2">
                    <div className="space-y-1">
                      <span className="text-[11px] text-slate-400">Posisi X (px)</span>
                      <input
                        type="number"
                        value={selectedLayer.x}
                        onChange={(e) =>
                          updateLayer(selectedLayer.id, { x: parseInt(e.target.value) || 0 })
                        }
                        className="w-full px-2 py-1 bg-slate-800 border border-slate-700 rounded text-xs font-mono text-slate-200"
                      />
                    </div>
                    <div className="space-y-1">
                      <span className="text-[11px] text-slate-400">Posisi Y (px)</span>
                      <input
                        type="number"
                        value={selectedLayer.y}
                        onChange={(e) =>
                          updateLayer(selectedLayer.id, { y: parseInt(e.target.value) || 0 })
                        }
                        className="w-full px-2 py-1 bg-slate-800 border border-slate-700 rounded text-xs font-mono text-slate-200"
                      />
                    </div>
                  </div>

                  {/* Rotation */}
                  <div className="space-y-1">
                    <div className="flex justify-between items-center">
                      <span className="text-[11px] text-slate-400">Rotasi Derajat</span>
                      <span className="font-mono text-[10px] text-indigo-400">
                        {selectedLayer.rotation || 0}°
                      </span>
                    </div>
                    <input
                      type="range"
                      min="-180"
                      max="180"
                      value={selectedLayer.rotation || 0}
                      onChange={(e) =>
                        updateLayer(selectedLayer.id, { rotation: parseInt(e.target.value) })
                      }
                      className="w-full h-1.5 bg-slate-800 rounded appearance-none cursor-pointer"
                    />
                  </div>

                  {/* Opacity */}
                  <div className="space-y-1">
                    <div className="flex justify-between items-center">
                      <span className="text-[11px] text-slate-400">Transparansi (Opacity)</span>
                      <span className="font-mono text-[10px] text-indigo-400">
                        {Math.round(selectedLayer.opacity * 100)}%
                      </span>
                    </div>
                    <input
                      type="range"
                      min="0"
                      max="1"
                      step="0.05"
                      value={selectedLayer.opacity}
                      onChange={(e) =>
                        updateLayer(selectedLayer.id, { opacity: parseFloat(e.target.value) })
                      }
                      className="w-full h-1.5 bg-slate-800 rounded appearance-none cursor-pointer"
                    />
                  </div>
                </div>
              </div>
            ) : (
              /* When no layer is selected: Packaging Canvas Base Properties */
              <div className="space-y-4">
                <div className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800 space-y-3">
                  <div className="flex items-center space-x-2">
                    <Palette className="w-4 h-4 text-indigo-400" />
                    <span className="text-xs font-semibold text-slate-200">
                      Warna Dasar Dieline
                    </span>
                  </div>
                  <p className="text-[11px] text-slate-400">
                    Atur warna dasar bahan karton kemasan yang belum tertutup grafis atau stiker.
                  </p>
                  <div className="flex items-center space-x-2 pt-1">
                    <input
                      type="color"
                      value={backgroundColor}
                      onChange={(e) => setBackgroundColor(e.target.value)}
                      className="w-8 h-8 rounded cursor-pointer border-0 bg-transparent"
                    />
                    <span className="font-mono text-xs text-slate-200 uppercase font-semibold">
                      {backgroundColor}
                    </span>
                  </div>
                </div>

                {/* Quick Add Elements Card */}
                <div className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800 space-y-2.5">
                  <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block">
                    Tambah Elemen Baru
                  </span>
                  <div className="grid grid-cols-2 gap-2 text-xs">
                    <button
                      onClick={() => addTextLayer('NAMA MERK')}
                      className="p-2.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 flex items-center space-x-2 transition"
                    >
                      <Type className="w-4 h-4 text-indigo-400" />
                      <span>Teks</span>
                    </button>
                    <button
                      onClick={() => addBarcodeLayer('899723450912')}
                      className="p-2.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 flex items-center space-x-2 transition"
                    >
                      <Barcode className="w-4 h-4 text-purple-400" />
                      <span>Barcode</span>
                    </button>
                    <button
                      onClick={() => addQRCodeLayer('https://pacdora.com')}
                      className="p-2.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 flex items-center space-x-2 transition"
                    >
                      <QrCode className="w-4 h-4 text-sky-400" />
                      <span>QR Code</span>
                    </button>
                    <button
                      onClick={() => addBadgeLayer('halal')}
                      className="p-2.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 flex items-center space-x-2 transition"
                    >
                      <Award className="w-4 h-4 text-rose-400" />
                      <span>Stempel Halal</span>
                    </button>
                  </div>
                </div>

                {/* Tip */}
                <div className="p-3 rounded-lg bg-indigo-950/40 border border-indigo-900/60 text-[11px] text-indigo-300">
                  <span>💡 Klik salah satu objek pada kanvas 2D untuk mengedit posisi, warna, atau font!</span>
                </div>
              </div>
            )}
          </>
        )}

        {/* ============= LAYERS STACK TAB ============= */}
        {activeRightTab === 'layers' && (
          <div className="space-y-2">
            <div className="flex items-center justify-between pb-1 border-b border-slate-800 text-xs">
              <span className="font-semibold text-slate-300 uppercase tracking-wider">
                Susunan Lapisan ({layers.length})
              </span>
              <span className="text-[11px] text-slate-500">Atas ke Bawah</span>
            </div>

            {layers.length === 0 ? (
              <p className="text-xs text-slate-500 py-6 text-center">Belum ada elemen pada kanvas.</p>
            ) : (
              <div className="space-y-1.5 pt-1">
                {[...layers].reverse().map((layer) => {
                  const isSelected = layer.id === selectedLayerId;
                  return (
                    <div
                      key={layer.id}
                      onClick={() => setSelectedLayerId(layer.id)}
                      className={`p-2.5 rounded-xl border flex items-center justify-between text-xs transition cursor-pointer group ${
                        isSelected
                          ? 'bg-indigo-600/20 border-indigo-500 text-white shadow-sm'
                          : 'bg-slate-800/40 border-slate-700/60 text-slate-300 hover:bg-slate-800 hover:border-slate-600'
                      }`}
                    >
                      <div className="flex items-center space-x-2.5 min-w-0">
                        <div className="text-slate-400">
                          {layer.type === 'text' && <Type className="w-3.5 h-3.5 text-indigo-400" />}
                          {layer.type === 'shape' && <Square className="w-3.5 h-3.5 text-amber-400" />}
                          {layer.type === 'image' && <ImageIcon className="w-3.5 h-3.5 text-emerald-400" />}
                          {layer.type === 'barcode' && <Barcode className="w-3.5 h-3.5 text-purple-400" />}
                          {layer.type === 'qrcode' && <QrCode className="w-3.5 h-3.5 text-sky-400" />}
                          {layer.type === 'badge' && <Award className="w-3.5 h-3.5 text-rose-400" />}
                        </div>
                        <span className="truncate font-medium">{layer.name}</span>
                      </div>

                      {/* Layer controls */}
                      <div className="flex items-center space-x-1 shrink-0">
                        {/* Visibility */}
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            updateLayer(layer.id, { hidden: !layer.hidden });
                          }}
                          className="p-1 hover:text-white text-slate-400 transition"
                          title={layer.hidden ? 'Tampilkan' : 'Sembunyikan'}
                        >
                          {layer.hidden ? <EyeOff className="w-3 h-3 text-rose-400" /> : <Eye className="w-3 h-3" />}
                        </button>

                        {/* Move Up */}
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            reorderLayer(layer.id, 'up');
                          }}
                          className="p-1 hover:text-white text-slate-400 transition"
                          title="Pindah ke Atas"
                        >
                          <ChevronUp className="w-3 h-3" />
                        </button>

                        {/* Move Down */}
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            reorderLayer(layer.id, 'down');
                          }}
                          className="p-1 hover:text-white text-slate-400 transition"
                          title="Pindah ke Bawah"
                        >
                          <ChevronDown className="w-3 h-3" />
                        </button>

                        {/* Delete */}
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            removeLayer(layer.id);
                          }}
                          className="p-1 hover:text-rose-400 text-slate-400 transition"
                          title="Hapus"
                        >
                          <Trash2 className="w-3 h-3" />
                        </button>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        )}
      </div>
    </aside>
  );
};
