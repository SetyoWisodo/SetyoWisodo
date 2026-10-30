/**
 * Komposisi Remotion — 9 detik, 1080×1920, 60 fps, 540 frame.
 *
 * Angka dan teks TIDAK ditulis di sini: semuanya dibaca dari
 * `data/film-sheet.json` (salinan `motion/film-sheet.json`). Kalau lembar film
 * berubah, komposisi ini ikut berubah tanpa menyunting JSX.
 *
 * Remotion dipasang (npm), tetapi MERENDER butuh Chrome. Sandbox ini tidak
 * punya Chrome yang bisa jalan (libnss3 tidak tersedia), jadi `npm run
 * remotion:render` akan gagal di sini dan berhasil di mesin yang punya Chrome.
 * Bundling TIDAK butuh Chrome — `npm run remotion:bundle` lolos di sini.
 */
import React from 'react';
import { AbsoluteFill, Composition, Sequence, interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { film } from './data.js';

const WARNA = {
  paper: '#F5EFE4',
  paper2: '#EFE6D6',
  ink: '#16110D',
  orange: '#E1542B',
  espresso: '#4A2C1A',
  gold: '#D9A441',
};

const HURUF = {
  display: '"Bricolage Grotesque", "Archivo Black", Impact, sans-serif',
  serif: 'Fraunces, Georgia, serif',
  body: 'Inter, system-ui, sans-serif',
};

/** Satu cue = satu lapisan teks. Durasi & teks dari lembar film. */
const Cue = ({ cue }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const durasi = cue.frame[1] - cue.frame[0];

  // masuk: spring tanpa overshoot besar (damping tinggi), keluar: 65% durasi masuk
  const masuk = spring({ frame, fps, config: { damping: 200, stiffness: 120, mass: 0.6 }, durationInFrames: 26 });
  const keluar = interpolate(frame, [durasi - 18, durasi], [1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const naik = interpolate(masuk, [0, 1], [46, 0]);       // transform saja
  const skala = 0.97 + masuk * 0.03;
  const akhir = frame > durasi - 18 ? keluar : 1;

  const judul = cue.cue === 1;
  const payoff = cue.tier === 5;

  return (
    <AbsoluteFill
      style={{
        padding: '180px 84px 200px',
        justifyContent: 'center',
        alignItems: 'flex-start',
        fontFamily: HURUF.body,
        color: WARNA.ink,
      }}
    >
      <div
        style={{
          opacity: Math.min(masuk, akhir),
          transform: `translate3d(0, ${naik}px, 0) scale(${skala})`,
          maxWidth: 960,
        }}
      >
        <div
          style={{
            fontFamily: HURUF.body,
            fontSize: 22,
            letterSpacing: '0.22em',
            textTransform: 'uppercase',
            color: WARNA.espresso,
            marginBottom: 34,
          }}
        >
          {cue.perangkat} · tier {cue.tier}
        </div>
        <div
          style={{
            fontFamily: judul || payoff ? HURUF.display : HURUF.serif,
            fontWeight: judul || payoff ? 800 : 300,
            fontSize: judul ? 92 : payoff ? 84 : 64,
            lineHeight: 0.98,
            letterSpacing: judul ? '-0.035em' : '-0.02em',
            textShadow: judul ? `0 3px 0 rgba(74,44,26,.12), 0 18px 30px rgba(74,44,26,.12)` : 'none',
          }}
        >
          {cue.teks}
        </div>
        <div
          style={{
            marginTop: 40,
            width: 120,
            height: 4,
            background: cue.tier === 5 ? WARNA.orange : WARNA.ink,
          }}
        />
        <div style={{ marginTop: 22, fontSize: 20, letterSpacing: '0.1em', color: 'rgba(22,17,13,.55)' }}>
          cue {cue.cue} · {cue.mulai}s–{cue.selesai}s · sumber: {cue.sumber}
        </div>
      </div>
    </AbsoluteFill>
  );
};

/** Bilah kemajuan: satu-satunya gerak yang terus berjalan sepanjang film. */
const Kemajuan = ({ total }) => {
  const frame = useCurrentFrame();
  return (
    <div style={{ position: 'absolute', top: 0, left: 0, right: 0, height: 6, background: WARNA.paper2 }}>
      <div
        style={{
          height: '100%',
          width: `${(frame / total) * 100}%`,
          background: WARNA.orange,
        }}
      />
    </div>
  );
};

/** Pemetaan tier → satu gerak latar. Tier 1-2 = diam (lembah), 3-5 = bergerak. */
const Latar = ({ cue }) => {
  const frame = useCurrentFrame();
  const dorong = cue.tier >= 3 ? interpolate(frame, [0, 60], [1, 1.04], { extrapolateRight: 'clamp' }) : 1;
  return (
    <AbsoluteFill style={{ background: cue.cue === 1 ? WARNA.paper : WARNA.paper2, transform: `scale(${dorong})` }}>
      <div
        style={{
          position: 'absolute',
          inset: 0,
          background: `repeating-linear-gradient(0deg, rgba(22,17,13,.055) 0 1px, transparent 1px 96px)`,
          opacity: cue.tier >= 3 ? 1 : 0.45,
        }}
      />
    </AbsoluteFill>
  );
};

export const KlipNocturne = () => {
  const { durationInFrames } = useVideoConfig();
  const adegan = film.adegan[0];                    // adegan 01 (bisa dipilih lewat props nanti)
  return (
    <AbsoluteFill style={{ background: WARNA.paper }}>
      <Kemajuan total={durationInFrames} />
      {adegan.cues.map((cue) => (
        <Sequence key={cue.cue} from={cue.frame[0]} durationInFrames={cue.frame[1] - cue.frame[0]}>
          <Latar cue={cue} />
          <Cue cue={cue} />
        </Sequence>
      ))}
      <AbsoluteFill style={{ pointerEvents: 'none' }}>
        <div
          style={{
            position: 'absolute',
            bottom: 96,
            left: 84,
            right: 84,
            display: 'flex',
            justifyContent: 'space-between',
            fontFamily: HURUF.body,
            fontSize: 20,
            letterSpacing: '0.16em',
            textTransform: 'uppercase',
            color: 'rgba(22,17,13,.55)',
          }}
        >
          <span>Nocturne Koffie</span>
          <span>{adegan.arc} · {film.grid.bpm} BPM</span>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

export const Root = () => (
  <Composition
    id="KlipNocturne"
    component={KlipNocturne}
    durationInFrames={film.grid.frame_total}
    fps={film.grid.fps}
    width={1080}
    height={1920}
  />
);
