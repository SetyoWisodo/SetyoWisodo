import { useRef, useEffect, useImperativeHandle, forwardRef, useState } from 'react';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { GLTFExporter } from 'three/examples/jsm/exporters/GLTFExporter.js';
import {
  RotateCcw,
  Play,
  Pause,
  Sliders,
  Box,
} from 'lucide-react';
import type { PackagingStudioState } from '../hooks/usePackagingStudio';
import { PACKAGING_MODELS } from '../utils/packagingModels';
import { createPackaging3D } from '../utils/packaging3d';
import type { PackagingMeshResult } from '../utils/packaging3d';
import { applyMaterialProperties } from '../utils/textures';

export interface Viewport3DRef {
  captureSnapshot: (width: number, height: number, transparent?: boolean) => string;
  exportGLTF: () => Promise<Blob>;
  record360Video: (durationMs: number, onProgress?: (p: number) => void) => Promise<Blob>;
}

interface Viewport3DProps {
  studio: PackagingStudioState;
  dielineCanvas: HTMLCanvasElement | null;
}

export const Viewport3D = forwardRef<Viewport3DRef, Viewport3DProps>(({ studio, dielineCanvas }, ref) => {
  const {
    currentModelId,
    dimensions,
    openFactor,
    setOpenFactor,
    material: materialType,
    lighting,
    hasCondensation,
    showWireframe,
    setShowWireframe,
    autoRotate,
    setAutoRotate,
    rotationSpeed,
    backgroundColor,
    isTransparentBg,
  } = studio;

  const containerRef = useRef<HTMLDivElement | null>(null);
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  // Three.js internal references
  const sceneRef = useRef<THREE.Scene | null>(null);
  const cameraRef = useRef<THREE.PerspectiveCamera | null>(null);
  const rendererRef = useRef<THREE.WebGLRenderer | null>(null);
  const controlsRef = useRef<OrbitControls | null>(null);
  const mainMaterialRef = useRef<THREE.MeshPhysicalMaterial | null>(null);
  const meshResultRef = useRef<PackagingMeshResult | null>(null);
  const textureRef = useRef<THREE.CanvasTexture | null>(null);
  const lightsGroupRef = useRef<THREE.Group | null>(null);
  const floorMeshRef = useRef<THREE.Mesh | null>(null);

  const modelDef = PACKAGING_MODELS[currentModelId];
  const [cameraAngle, setCameraAngle] = useState<'default' | 'front' | 'top' | 'right' | 'hero' | 'iso'>('hero');

  // Initialize Three.js Scene
  useEffect(() => {
    if (!containerRef.current || !canvasRef.current) return;

    const width = containerRef.current.clientWidth;
    const height = containerRef.current.clientHeight;

    // 1. Scene
    const scene = new THREE.Scene();
    sceneRef.current = scene;
    scene.background = isTransparentBg ? null : new THREE.Color(backgroundColor);

    // 2. Camera: facing directly front-center like in Screenshot 179
    const camera = new THREE.PerspectiveCamera(40, width / height, 0.1, 100);
    camera.position.set(0.15, 1.25, 3.2);
    cameraRef.current = camera;

    // 3. Renderer
    const renderer = new THREE.WebGLRenderer({
      canvas: canvasRef.current,
      antialias: true,
      alpha: true,
      preserveDrawingBuffer: true,
    });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.1;
    rendererRef.current = renderer;

    // 4. Orbit Controls
    const controls = new OrbitControls(camera, canvasRef.current);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.maxDistance = 15;
    controls.minDistance = 0.8;
    controls.target.set(0, 0.8, 0);
    controlsRef.current = controls;

    // 5. Lighting Rig Group
    const lightsGroup = new THREE.Group();
    scene.add(lightsGroup);
    lightsGroupRef.current = lightsGroup;

    // 6. Floor Shadow Receiver Plane
    const floorGeo = new THREE.PlaneGeometry(30, 30);
    const floorMat = new THREE.ShadowMaterial({ opacity: 0.28 });
    const floor = new THREE.Mesh(floorGeo, floorMat);
    floor.rotation.x = -Math.PI / 2;
    floor.position.y = -0.01;
    floor.receiveShadow = true;
    scene.add(floor);
    floorMeshRef.current = floor;

    // 7. Base Material for Packaging
    const pbrMaterial = new THREE.MeshPhysicalMaterial({
      roughness: 0.4,
      metalness: 0.1,
      clearcoat: 0.2,
    });
    mainMaterialRef.current = pbrMaterial;

    // 8. Animation Render Loop
    let animationId: number;
    const clock = new THREE.Clock();

    const animate = () => {
      animationId = requestAnimationFrame(animate);
      const delta = clock.getDelta();

      if (autoRotate && meshResultRef.current?.group) {
        meshResultRef.current.group.rotation.y += delta * 0.8 * rotationSpeed;
      }

      controls.update();
      renderer.render(scene, camera);
    };
    animate();

    // 9. Resize Observer
    const handleResize = () => {
      if (!containerRef.current || !rendererRef.current || !cameraRef.current) return;
      const w = containerRef.current.clientWidth;
      const h = containerRef.current.clientHeight;
      cameraRef.current.aspect = w / h;
      cameraRef.current.updateProjectionMatrix();
      rendererRef.current.setSize(w, h);
    };
    window.addEventListener('resize', handleResize);

    return () => {
      cancelAnimationFrame(animationId);
      window.removeEventListener('resize', handleResize);
      renderer.dispose();
      controls.dispose();
    };
  }, []);

  // Update Background Color or Transparency
  useEffect(() => {
    if (!sceneRef.current) return;
    if (isTransparentBg) {
      sceneRef.current.background = null;
    } else {
      sceneRef.current.background = new THREE.Color(backgroundColor);
    }
  }, [backgroundColor, isTransparentBg]);

  // Update Lighting Rig when lighting preset changes
  useEffect(() => {
    const group = lightsGroupRef.current;
    if (!group) return;

    // Clear old lights
    while (group.children.length > 0) {
      group.remove(group.children[0]);
    }

    switch (lighting) {
      case 'studio_minimal': {
        const ambient = new THREE.AmbientLight(0xffffff, 0.85);
        group.add(ambient);

        const keyLight = new THREE.DirectionalLight(0xffffff, 1.8);
        keyLight.position.set(4, 6, 4);
        keyLight.castShadow = true;
        keyLight.shadow.mapSize.width = 2048;
        keyLight.shadow.mapSize.height = 2048;
        keyLight.shadow.bias = -0.0005;
        group.add(keyLight);

        const fillLight = new THREE.DirectionalLight(0xe0f2fe, 0.9);
        fillLight.position.set(-4, 3, -3);
        group.add(fillLight);

        const rimLight = new THREE.DirectionalLight(0xffffff, 0.7);
        rimLight.position.set(0, 5, -5);
        group.add(rimLight);
        break;
      }

      case 'warm_commercial': {
        const ambient = new THREE.AmbientLight(0xfffbeb, 0.9);
        group.add(ambient);

        const keyLight = new THREE.DirectionalLight(0xfef3c7, 2.2);
        keyLight.position.set(5, 7, 3);
        keyLight.castShadow = true;
        keyLight.shadow.mapSize.width = 2048;
        keyLight.shadow.mapSize.height = 2048;
        group.add(keyLight);

        const fillLight = new THREE.DirectionalLight(0xfde68a, 0.7);
        fillLight.position.set(-4, 2, 2);
        group.add(fillLight);

        const rimLight = new THREE.DirectionalLight(0xfb923c, 1.1);
        rimLight.position.set(0, 4, -5);
        group.add(rimLight);
        break;
      }

      case 'dramatic_rim': {
        const ambient = new THREE.AmbientLight(0x0f172a, 0.4);
        group.add(ambient);

        const rimLeft = new THREE.DirectionalLight(0x38bdf8, 2.6);
        rimLeft.position.set(-5, 4, -4);
        group.add(rimLeft);

        const rimRight = new THREE.DirectionalLight(0xf43f5e, 2.4);
        rimRight.position.set(5, 4, -4);
        group.add(rimRight);

        const keyLight = new THREE.DirectionalLight(0xffffff, 1.0);
        keyLight.position.set(0, 5, 4);
        keyLight.castShadow = true;
        group.add(keyLight);
        break;
      }

      case 'neon_cyber': {
        const ambient = new THREE.AmbientLight(0x050814, 0.35);
        group.add(ambient);

        const cyanRim = new THREE.DirectionalLight(0x00f2fe, 3.2);
        cyanRim.position.set(4, 5, -3);
        group.add(cyanRim);

        const magentaRim = new THREE.DirectionalLight(0xff007f, 3.0);
        magentaRim.position.set(-4, 4, -3);
        group.add(magentaRim);

        const topKey = new THREE.DirectionalLight(0xffffff, 0.9);
        topKey.position.set(0, 7, 3);
        topKey.castShadow = true;
        group.add(topKey);
        break;
      }

      case 'pure_catalog': {
        const ambient = new THREE.AmbientLight(0xffffff, 1.2);
        group.add(ambient);

        const keyLight = new THREE.DirectionalLight(0xffffff, 1.5);
        keyLight.position.set(3, 8, 4);
        keyLight.castShadow = true;
        keyLight.shadow.mapSize.width = 2048;
        keyLight.shadow.mapSize.height = 2048;
        group.add(keyLight);

        const softFill = new THREE.DirectionalLight(0xffffff, 1.0);
        softFill.position.set(-3, 6, -3);
        group.add(softFill);
        break;
      }
    }
  }, [lighting]);

  // Build / Re-build 3D Packaging Model
  useEffect(() => {
    const scene = sceneRef.current;
    const material = mainMaterialRef.current;
    if (!scene || !material) return;

    // Remove previous mesh
    if (meshResultRef.current?.group) {
      scene.remove(meshResultRef.current.group);
    }

    // Configure material properties
    applyMaterialProperties(material, materialType, hasCondensation);
    material.wireframe = showWireframe;

    // Attach existing texture if present
    if (textureRef.current) {
      material.map = textureRef.current;
      material.needsUpdate = true;
    }

    // Create new 3D packaging mesh
    const result = createPackaging3D(currentModelId, dimensions, material);
    scene.add(result.group);
    meshResultRef.current = result;

    // Apply current open factor
    result.updateOpenAngle(openFactor);

    // Adjust target center based on packaging height
    if (controlsRef.current) {
      const targetY = (dimensions.height * 0.01) / 2;
      controlsRef.current.target.set(0, targetY, 0);
    }
  }, [currentModelId, dimensions, materialType, hasCondensation]);

  // Update Wireframe
  useEffect(() => {
    if (mainMaterialRef.current) {
      mainMaterialRef.current.wireframe = showWireframe;
      mainMaterialRef.current.needsUpdate = true;
    }
  }, [showWireframe]);

  // Update Open Angle when slider moves
  useEffect(() => {
    if (meshResultRef.current) {
      meshResultRef.current.updateOpenAngle(openFactor);
    }
  }, [openFactor]);

  // Real-time Canvas Texture Sync
  useEffect(() => {
    if (!dielineCanvas || !mainMaterialRef.current) return;

    if (!textureRef.current) {
      const texture = new THREE.CanvasTexture(dielineCanvas);
      texture.colorSpace = THREE.SRGBColorSpace;
      texture.generateMipmaps = true;
      texture.minFilter = THREE.LinearMipmapLinearFilter;
      texture.magFilter = THREE.LinearFilter;
      textureRef.current = texture;
      mainMaterialRef.current.map = texture;
      mainMaterialRef.current.needsUpdate = true;
    } else {
      textureRef.current.needsUpdate = true;
    }
  }, [dielineCanvas]);

  // Camera Presets switcher
  const setCameraView = (angle: 'default' | 'front' | 'top' | 'right' | 'hero' | 'iso') => {
    if (!cameraRef.current || !controlsRef.current) return;
    setCameraAngle(angle);

    const centerY = (dimensions.height * 0.01) / 2;
    controlsRef.current.target.set(0, centerY, 0);

    const maxDim = Math.max(dimensions.width, dimensions.height, dimensions.depth) * 0.01;
    const dist = maxDim * 2.8;

    switch (angle) {
      case 'front':
        cameraRef.current.position.set(0, centerY, dist);
        break;
      case 'top':
        cameraRef.current.position.set(0, dist + centerY, 0.001);
        break;
      case 'right':
        cameraRef.current.position.set(dist, centerY, 0);
        break;
      case 'hero':
        cameraRef.current.position.set(dist * 0.75, dist * 0.55 + centerY, dist * 0.75);
        break;
      case 'iso':
        cameraRef.current.position.set(dist * 0.8, dist * 0.8 + centerY, dist * 0.8);
        break;
      case 'default':
        cameraRef.current.position.set(2.4, 2.0, 3.2);
        break;
    }
    controlsRef.current.update();
  };

  // Expose Imperative Methods for Snapshot & Video Recording
  useImperativeHandle(ref, () => ({
    captureSnapshot: (w: number, h: number, transparent: boolean = false) => {
      const renderer = rendererRef.current;
      const scene = sceneRef.current;
      const camera = cameraRef.current;
      if (!renderer || !scene || !camera) return '';

      // Temporarily resize renderer for high-resolution render
      const origSize = new THREE.Vector2();
      renderer.getSize(origSize);
      const origPixelRatio = renderer.getPixelRatio();
      const origBg = scene.background;

      if (transparent) {
        scene.background = null;
      }

      renderer.setSize(w, h, false);
      camera.aspect = w / h;
      camera.updateProjectionMatrix();

      renderer.render(scene, camera);
      const dataUrl = renderer.domElement.toDataURL(transparent ? 'image/png' : 'image/jpeg', 0.95);

      // Restore
      renderer.setSize(origSize.x, origSize.y, false);
      renderer.setPixelRatio(origPixelRatio);
      scene.background = origBg;
      camera.aspect = origSize.x / origSize.y;
      camera.updateProjectionMatrix();
      renderer.render(scene, camera);

      return dataUrl;
    },

    exportGLTF: () => {
      return new Promise<Blob>((resolve, reject) => {
        const scene = sceneRef.current;
        const meshGroup = meshResultRef.current?.group;
        if (!scene || !meshGroup) {
          reject(new Error('Scene or Mesh not ready'));
          return;
        }

        const exporter = new GLTFExporter();
        exporter.parse(
          meshGroup,
          (gltf) => {
            const blob = new Blob([gltf as ArrayBuffer], { type: 'model/gltf-binary' });
            resolve(blob);
          },
          (err) => reject(err),
          { binary: true }
        );
      });
    },

    record360Video: (durationMs: number = 4000, onProgress?: (p: number) => void) => {
      return new Promise<Blob>((resolve, reject) => {
        const canvas = canvasRef.current;
        const meshGroup = meshResultRef.current?.group;
        if (!canvas || !meshGroup) {
          reject(new Error('Canvas or mesh not found'));
          return;
        }

        const stream = canvas.captureStream(30);
        const recordedChunks: Blob[] = [];
        const mediaRecorder = new MediaRecorder(stream, { mimeType: 'video/webm' });

        mediaRecorder.ondataavailable = (e) => {
          if (e.data.size > 0) recordedChunks.push(e.data);
        };

        mediaRecorder.onstop = () => {
          const blob = new Blob(recordedChunks, { type: 'video/webm' });
          resolve(blob);
        };

        const initialRot = meshGroup.rotation.y;
        const startTime = performance.now();

        mediaRecorder.start();

        const spinInterval = setInterval(() => {
          const elapsed = performance.now() - startTime;
          const progress = Math.min(1, elapsed / durationMs);

          meshGroup.rotation.y = initialRot + progress * Math.PI * 2;
          if (onProgress) onProgress(progress);

          if (progress >= 1) {
            clearInterval(spinInterval);
            mediaRecorder.stop();
            meshGroup.rotation.y = initialRot;
          }
        }, 33);
      });
    },
  }));

  return (
    <div ref={containerRef} className="relative w-full h-full overflow-hidden bg-slate-950">
      {/* Three.js Canvas */}
      <canvas ref={canvasRef} className="w-full h-full block cursor-grab active:cursor-grabbing" />

      {/* Top Floating Viewport Control Bar */}
      <div className="absolute top-3 left-3 right-3 flex items-center justify-between pointer-events-none">
        {/* Camera Presets Buttons */}
        <div className="flex items-center space-x-1 bg-slate-900/85 backdrop-blur-md border border-slate-800/80 rounded-lg p-1 pointer-events-auto shadow-lg">
          <button
            onClick={() => setCameraView('front')}
            className={`px-2 py-1 rounded text-xs font-medium transition ${
              cameraAngle === 'front'
                ? 'bg-indigo-600 text-white'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'
            }`}
          >
            Depan
          </button>
          <button
            onClick={() => setCameraView('top')}
            className={`px-2 py-1 rounded text-xs font-medium transition ${
              cameraAngle === 'top'
                ? 'bg-indigo-600 text-white'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'
            }`}
          >
            Atas
          </button>
          <button
            onClick={() => setCameraView('right')}
            className={`px-2 py-1 rounded text-xs font-medium transition ${
              cameraAngle === 'right'
                ? 'bg-indigo-600 text-white'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'
            }`}
          >
            Kanan
          </button>
          <button
            onClick={() => setCameraView('hero')}
            className={`px-2 py-1 rounded text-xs font-medium transition ${
              cameraAngle === 'hero'
                ? 'bg-indigo-600 text-white'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'
            }`}
          >
            Hero 45°
          </button>
          <button
            onClick={() => setCameraView('iso')}
            className={`px-2 py-1 rounded text-xs font-medium transition ${
              cameraAngle === 'iso'
                ? 'bg-indigo-600 text-white'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'
            }`}
          >
            Isometrik
          </button>
        </div>

        {/* Viewport Action Buttons */}
        <div className="flex items-center space-x-1.5 bg-slate-900/85 backdrop-blur-md border border-slate-800/80 rounded-lg p-1 pointer-events-auto shadow-lg">
          {/* Auto Rotate Turntable */}
          <button
            onClick={() => setAutoRotate(!autoRotate)}
            className={`p-1.5 rounded-md transition ${
              autoRotate ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'
            }`}
            title={autoRotate ? 'Hentikan Putaran 360°' : 'Putar 360° Otomatis'}
          >
            {autoRotate ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
          </button>

          {/* Wireframe */}
          <button
            onClick={() => setShowWireframe(!showWireframe)}
            className={`p-1.5 rounded-md transition ${
              showWireframe ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'
            }`}
            title="Wireframe Mesh"
          >
            <Box className="w-4 h-4" />
          </button>

          {/* Reset View */}
          <button
            onClick={() => setCameraView('hero')}
            className="p-1.5 rounded-md text-slate-400 hover:text-slate-200 hover:bg-slate-800 transition"
            title="Reset Sudut Pandang"
          >
            <RotateCcw className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Interactive Lid Open / Close Mechanism Slider (Pacdora signature feature!) */}
      {modelDef.hasOpenAnimation && (
        <div className="absolute bottom-4 left-1/2 -translate-x-1/2 bg-slate-900/90 backdrop-blur-md border border-slate-800/80 rounded-xl px-4 py-2.5 flex items-center space-x-3 shadow-2xl z-10 w-80 max-w-[90%]">
          <Sliders className="w-4 h-4 text-indigo-400 shrink-0" />
          <div className="flex-1 flex flex-col space-y-1">
            <div className="flex justify-between items-center text-[11px]">
              <span className="text-slate-300 font-medium">{modelDef.openLabel || 'Buka Tutup Kemasan'}</span>
              <span className="text-indigo-400 font-mono font-semibold">{Math.round(openFactor * 100)}%</span>
            </div>
            <input
              type="range"
              min="0"
              max="1"
              step="0.01"
              value={openFactor}
              onChange={(e) => setOpenFactor(parseFloat(e.target.value))}
              className="w-full h-1.5 bg-slate-700 rounded-lg appearance-none cursor-pointer"
            />
          </div>
        </div>
      )}

      {/* Orbit Helper Tip */}
      <div className="absolute bottom-3 left-3 text-[11px] text-slate-500 bg-slate-950/60 px-2 py-1 rounded backdrop-blur pointer-events-none">
        <span>Klik kiri drag untuk rotasi • Scroll untuk zoom • Klik kanan pan</span>
      </div>
    </div>
  );
});
