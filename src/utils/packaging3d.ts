import * as THREE from 'three';
import type { PackagingDimensions, PackagingModelId } from '../types/packaging';

export interface PackagingMeshResult {
  group: THREE.Group;
  mainMesh: THREE.Mesh | THREE.Group;
  accentMeshes: THREE.Mesh[];
  updateDimensions: (dims: PackagingDimensions) => void;
  updateOpenAngle: (factor: number) => void; // 0 to 1
}

/**
 * Creates 3D packaging mesh for the chosen model
 */
export function createPackaging3D(
  modelId: PackagingModelId,
  dimensions: PackagingDimensions,
  mainMaterial: THREE.Material
): PackagingMeshResult {
  const rootGroup = new THREE.Group();
  rootGroup.name = 'PackagingRoot';

  let updateDimensionsFn = (_dims: PackagingDimensions) => {};
  let updateOpenAngleFn = (_factor: number) => {};
  const accentMeshes: THREE.Mesh[] = [];

  // Aluminum / Metal material for cans, caps, hardware
  const metalMaterial = new THREE.MeshPhysicalMaterial({
    color: '#e2e8f0',
    metalness: 0.95,
    roughness: 0.18,
    clearcoat: 0.3,
  });

  // Matte plastic material for bottle caps, lids
  const plasticMaterial = new THREE.MeshPhysicalMaterial({
    color: '#1e293b',
    roughness: 0.45,
    metalness: 0.05,
  });

  switch (modelId) {
    case 'mailer_box': {
      // Scale: 1mm = 0.01 units
      const baseGroup = new THREE.Group();
      const lidGroup = new THREE.Group();
      rootGroup.add(baseGroup);
      rootGroup.add(lidGroup);

      // Create parametric mailer box
      const buildMailer = (dims: PackagingDimensions) => {
        // Clear children
        while (baseGroup.children.length > 0) baseGroup.remove(baseGroup.children[0]);
        while (lidGroup.children.length > 0) lidGroup.remove(lidGroup.children[0]);

        const w = dims.width * 0.01;
        const h = dims.height * 0.01;
        const d = dims.depth * 0.01;
        const t = 0.02; // board thickness

        // 1. Bottom floor
        const bottomGeo = new THREE.BoxGeometry(w, t, d);
        setCustomBoxUVs(bottomGeo, 'bottom', 'mailer_box');
        const bottomMesh = new THREE.Mesh(bottomGeo, mainMaterial);
        bottomMesh.castShadow = true;
        bottomMesh.receiveShadow = true;
        bottomMesh.position.y = t / 2;
        baseGroup.add(bottomMesh);

        // 2. Front wall
        const frontGeo = new THREE.BoxGeometry(w, h, t);
        setCustomBoxUVs(frontGeo, 'front', 'mailer_box');
        const frontMesh = new THREE.Mesh(frontGeo, mainMaterial);
        frontMesh.position.set(0, h / 2, d / 2 - t / 2);
        frontMesh.castShadow = true;
        frontMesh.receiveShadow = true;
        baseGroup.add(frontMesh);

        // 3. Back wall
        const backGeo = new THREE.BoxGeometry(w, h, t);
        setCustomBoxUVs(backGeo, 'back', 'mailer_box');
        const backMesh = new THREE.Mesh(backGeo, mainMaterial);
        backMesh.position.set(0, h / 2, -d / 2 + t / 2);
        backMesh.castShadow = true;
        backMesh.receiveShadow = true;
        baseGroup.add(backMesh);

        // 4. Left wall
        const leftGeo = new THREE.BoxGeometry(t, h, d);
        setCustomBoxUVs(leftGeo, 'left', 'mailer_box');
        const leftMesh = new THREE.Mesh(leftGeo, mainMaterial);
        leftMesh.position.set(-w / 2 + t / 2, h / 2, 0);
        leftMesh.castShadow = true;
        leftMesh.receiveShadow = true;
        baseGroup.add(leftMesh);

        // 5. Right wall
        const rightGeo = new THREE.BoxGeometry(t, h, d);
        setCustomBoxUVs(rightGeo, 'right', 'mailer_box');
        const rightMesh = new THREE.Mesh(rightGeo, mainMaterial);
        rightMesh.position.set(w / 2 - t / 2, h / 2, 0);
        rightMesh.castShadow = true;
        rightMesh.receiveShadow = true;
        baseGroup.add(rightMesh);

        // 6. Hinged Lid: Pivot sits at top of back wall: (0, h, -d/2)
        lidGroup.position.set(0, h, -d / 2);

        // Lid Top plate: extends forward from back wall by depth 'd'
        const lidPlateGeo = new THREE.BoxGeometry(w * 1.01, t, d);
        setCustomBoxUVs(lidPlateGeo, 'lid', 'mailer_box');
        const lidPlate = new THREE.Mesh(lidPlateGeo, mainMaterial);
        lidPlate.position.set(0, t / 2, d / 2);
        lidPlate.castShadow = true;
        lidPlate.receiveShadow = true;
        lidGroup.add(lidPlate);

        // Lid Front Tuck Flap: hangs down at the front edge of lid
        const tuckFlapGeo = new THREE.BoxGeometry(w * 0.99, h * 0.85, t);
        setCustomBoxUVs(tuckFlapGeo, 'front', 'mailer_box');
        const tuckFlap = new THREE.Mesh(tuckFlapGeo, mainMaterial);
        tuckFlap.position.set(0, -h * 0.42, d);
        lidGroup.add(tuckFlap);

        // Lid side dust flaps
        const sideFlapLGeo = new THREE.BoxGeometry(t, h * 0.8, d * 0.95);
        const sideFlapL = new THREE.Mesh(sideFlapLGeo, mainMaterial);
        sideFlapL.position.set(-w * 0.5, -h * 0.38, d / 2);
        lidGroup.add(sideFlapL);

        const sideFlapR = new THREE.Mesh(sideFlapLGeo, mainMaterial);
        sideFlapR.position.set(w * 0.5, -h * 0.38, d / 2);
        lidGroup.add(sideFlapR);
      };

      buildMailer(dimensions);

      updateDimensionsFn = (dims) => {
        buildMailer(dims);
      };

      updateOpenAngleFn = (factor) => {
        // factor 0 (closed) to 1 (fully open 115 degrees)
        lidGroup.rotation.x = -factor * (Math.PI * 0.65);
      };

      return {
        group: rootGroup,
        mainMesh: baseGroup,
        accentMeshes,
        updateDimensions: updateDimensionsFn,
        updateOpenAngle: updateOpenAngleFn,
      };
    }

    case 'tuck_box': {
      const baseGroup = new THREE.Group();
      const topLidGroup = new THREE.Group();
      rootGroup.add(baseGroup);
      rootGroup.add(topLidGroup);

      const buildTuckBox = (dims: PackagingDimensions) => {
        while (baseGroup.children.length > 0) baseGroup.remove(baseGroup.children[0]);
        while (topLidGroup.children.length > 0) topLidGroup.remove(topLidGroup.children[0]);

        const w = dims.width * 0.01;
        const h = dims.height * 0.01;
        const d = dims.depth * 0.01;
        const t = 0.015;

        // Base box: Front, Back, Left, Right, Bottom
        // Front
        const frontGeo = new THREE.BoxGeometry(w, h, t);
        setCustomBoxUVs(frontGeo, 'front', 'tuck_box');
        const frontMesh = new THREE.Mesh(frontGeo, mainMaterial);
        frontMesh.position.set(0, h / 2, d / 2 - t / 2);
        frontMesh.castShadow = true;
        frontMesh.receiveShadow = true;
        baseGroup.add(frontMesh);

        // Back
        const backGeo = new THREE.BoxGeometry(w, h, t);
        setCustomBoxUVs(backGeo, 'back', 'tuck_box');
        const backMesh = new THREE.Mesh(backGeo, mainMaterial);
        backMesh.position.set(0, h / 2, -d / 2 + t / 2);
        backMesh.castShadow = true;
        backMesh.receiveShadow = true;
        baseGroup.add(backMesh);

        // Left
        const leftGeo = new THREE.BoxGeometry(t, h, d);
        setCustomBoxUVs(leftGeo, 'left', 'tuck_box');
        const leftMesh = new THREE.Mesh(leftGeo, mainMaterial);
        leftMesh.position.set(-w / 2 + t / 2, h / 2, 0);
        leftMesh.castShadow = true;
        leftMesh.receiveShadow = true;
        baseGroup.add(leftMesh);

        // Right
        const rightGeo = new THREE.BoxGeometry(t, h, d);
        setCustomBoxUVs(rightGeo, 'right', 'tuck_box');
        const rightMesh = new THREE.Mesh(rightGeo, mainMaterial);
        rightMesh.position.set(w / 2 - t / 2, h / 2, 0);
        rightMesh.castShadow = true;
        rightMesh.receiveShadow = true;
        baseGroup.add(rightMesh);

        // Bottom
        const botGeo = new THREE.BoxGeometry(w, t, d);
        setCustomBoxUVs(botGeo, 'bottom', 'tuck_box');
        const botMesh = new THREE.Mesh(botGeo, mainMaterial);
        botMesh.position.set(0, t / 2, 0);
        botMesh.castShadow = true;
        botMesh.receiveShadow = true;
        baseGroup.add(botMesh);

        // Top Lid: hinge at (0, h, -d/2)
        topLidGroup.position.set(0, h, -d / 2);

        const lidGeo = new THREE.BoxGeometry(w, t, d);
        setCustomBoxUVs(lidGeo, 'top', 'tuck_box');
        const lidMesh = new THREE.Mesh(lidGeo, mainMaterial);
        lidMesh.position.set(0, t / 2, d / 2);
        lidMesh.castShadow = true;
        topLidGroup.add(lidMesh);

        // Tuck flap at front of top lid
        const flapGeo = new THREE.BoxGeometry(w * 0.96, d * 0.35, t);
        setCustomBoxUVs(flapGeo, 'top', 'tuck_box');
        const flapMesh = new THREE.Mesh(flapGeo, mainMaterial);
        flapMesh.position.set(0, -d * 0.16, d);
        topLidGroup.add(flapMesh);
      };

      buildTuckBox(dimensions);

      updateDimensionsFn = (dims) => {
        buildTuckBox(dims);
      };

      updateOpenAngleFn = (factor) => {
        topLidGroup.rotation.x = -factor * (Math.PI * 0.7);
      };

      return {
        group: rootGroup,
        mainMesh: baseGroup,
        accentMeshes,
        updateDimensions: updateDimensionsFn,
        updateOpenAngle: updateOpenAngleFn,
      };
    }

    case 'beverage_can': {
      const canGroup = new THREE.Group();
      rootGroup.add(canGroup);

      const buildCan = (dims: PackagingDimensions) => {
        while (canGroup.children.length > 0) canGroup.remove(canGroup.children[0]);

        const r = (dims.radius || dims.width / 2) * 0.01;
        const h = dims.height * 0.01;

        // 1. Cylindrical printed body
        const bodyGeo = new THREE.CylinderGeometry(r, r, h * 0.88, 64, 1, true);
        const bodyMesh = new THREE.Mesh(bodyGeo, mainMaterial);
        bodyMesh.position.y = h * 0.5;
        bodyMesh.castShadow = true;
        bodyMesh.receiveShadow = true;
        canGroup.add(bodyMesh);

        // 2. Tapered top rim & lid (Aluminum)
        const neckGeo = new THREE.CylinderGeometry(r * 0.88, r, h * 0.06, 64);
        const neckMesh = new THREE.Mesh(neckGeo, metalMaterial);
        neckMesh.position.y = h * 0.94 + h * 0.01;
        neckMesh.castShadow = true;
        canGroup.add(neckMesh);
        accentMeshes.push(neckMesh);

        // Rim ring
        const rimGeo = new THREE.TorusGeometry(r * 0.88, 0.015, 16, 64);
        rimGeo.rotateX(Math.PI / 2);
        const rimMesh = new THREE.Mesh(rimGeo, metalMaterial);
        rimMesh.position.y = h * 0.97;
        canGroup.add(rimMesh);

        // Recessed top cap
        const capGeo = new THREE.CylinderGeometry(r * 0.86, r * 0.86, 0.02, 64);
        const capMesh = new THREE.Mesh(capGeo, metalMaterial);
        capMesh.position.y = h * 0.96;
        canGroup.add(capMesh);

        // Pull Tab
        const tabGeo = new THREE.BoxGeometry(r * 0.3, 0.01, r * 0.6);
        const tabMesh = new THREE.Mesh(tabGeo, metalMaterial);
        tabMesh.position.set(0, h * 0.975, r * 0.2);
        tabMesh.rotation.y = 0.2;
        canGroup.add(tabMesh);

        // 3. Concave bottom rim (Aluminum)
        const botRimGeo = new THREE.CylinderGeometry(r, r * 0.82, h * 0.06, 64);
        const botRimMesh = new THREE.Mesh(botRimGeo, metalMaterial);
        botRimMesh.position.y = h * 0.03;
        canGroup.add(botRimMesh);
        accentMeshes.push(botRimMesh);
      };

      buildCan(dimensions);
      updateDimensionsFn = (dims) => buildCan(dims);

      return {
        group: rootGroup,
        mainMesh: canGroup,
        accentMeshes,
        updateDimensions: updateDimensionsFn,
        updateOpenAngle: updateOpenAngleFn,
      };
    }

    case 'dropper_bottle': {
      const bottleGroup = new THREE.Group();
      const dropperGroup = new THREE.Group();
      rootGroup.add(bottleGroup);
      rootGroup.add(dropperGroup);

      const buildBottle = (dims: PackagingDimensions) => {
        while (bottleGroup.children.length > 0) bottleGroup.remove(bottleGroup.children[0]);
        while (dropperGroup.children.length > 0) dropperGroup.remove(dropperGroup.children[0]);

        const r = (dims.radius || dims.width / 2) * 0.01;
        const h = dims.height * 0.01;

        // Bottle glass body
        const glassGeo = new THREE.CylinderGeometry(r, r, h * 0.65, 48);
        const glassMesh = new THREE.Mesh(glassGeo, mainMaterial);
        glassMesh.position.y = h * 0.35;
        glassMesh.castShadow = true;
        glassMesh.receiveShadow = true;
        bottleGroup.add(glassMesh);

        // Bottle rounded shoulder
        const shoulderGeo = new THREE.CylinderGeometry(r * 0.45, r, h * 0.1, 48);
        const shoulderMesh = new THREE.Mesh(shoulderGeo, mainMaterial);
        shoulderMesh.position.y = h * 0.725;
        bottleGroup.add(shoulderMesh);

        // Bottle neck
        const neckGeo = new THREE.CylinderGeometry(r * 0.42, r * 0.42, h * 0.1, 48);
        const neckMesh = new THREE.Mesh(neckGeo, mainMaterial);
        neckMesh.position.y = h * 0.8;
        bottleGroup.add(neckMesh);

        // Printed label sleeve around cylinder
        const labelGeo = new THREE.CylinderGeometry(r * 1.015, r * 1.015, h * 0.52, 48, 1, true);
        const labelMesh = new THREE.Mesh(labelGeo, mainMaterial);
        labelMesh.position.y = h * 0.35;
        bottleGroup.add(labelMesh);

        // Dropper assembly
        dropperGroup.position.set(0, h * 0.85, 0);

        // Metallic collar ring
        const collarGeo = new THREE.CylinderGeometry(r * 0.48, r * 0.48, h * 0.14, 48);
        const collarMesh = new THREE.Mesh(collarGeo, metalMaterial);
        collarMesh.position.y = h * 0.07;
        collarMesh.castShadow = true;
        dropperGroup.add(collarMesh);

        // Rubber bulb on top
        const bulbGeo = new THREE.SphereGeometry(r * 0.4, 32, 24);
        bulbGeo.scale(1, 1.35, 1);
        const bulbMesh = new THREE.Mesh(bulbGeo, plasticMaterial);
        bulbMesh.position.y = h * 0.19;
        bulbMesh.castShadow = true;
        dropperGroup.add(bulbMesh);

        // Glass pipette inside
        const pipeGeo = new THREE.CylinderGeometry(0.015, 0.012, h * 0.65, 16);
        const pipeMesh = new THREE.Mesh(pipeGeo, mainMaterial);
        pipeMesh.position.y = -h * 0.25;
        dropperGroup.add(pipeMesh);
      };

      buildBottle(dimensions);
      updateDimensionsFn = (dims) => buildBottle(dims);
      updateOpenAngleFn = (factor) => {
        // Lifts dropper out of bottle
        dropperGroup.position.y = dimensions.height * 0.01 * 0.85 + factor * (dimensions.height * 0.01 * 0.6);
        dropperGroup.rotation.z = factor * 0.3;
      };

      return {
        group: rootGroup,
        mainMesh: bottleGroup,
        accentMeshes,
        updateDimensions: updateDimensionsFn,
        updateOpenAngle: updateOpenAngleFn,
      };
    }

    case 'standup_pouch': {
      const pouchGroup = new THREE.Group();
      rootGroup.add(pouchGroup);

      const buildPouch = (dims: PackagingDimensions) => {
        while (pouchGroup.children.length > 0) pouchGroup.remove(pouchGroup.children[0]);

        const w = dims.width * 0.01;
        const h = dims.height * 0.01;
        const d = dims.depth * 0.01;

        // Custom parametric standup pouch shape
        // Front curved panel
        const frontGeo = new THREE.PlaneGeometry(w, h, 32, 32);
        // Bulge center outward
        const pos = frontGeo.attributes.position;
        for (let i = 0; i < pos.count; i++) {
          const px = pos.getX(i);
          const py = pos.getY(i);
          // Normalized -1 to 1
          const nx = px / (w / 2);
          const ny = py / (h / 2);
          // Bulge strongest in lower middle
          const factorX = 1 - nx * nx;
          const factorY = (1 - ny) * 0.5 * (1 - ny * ny * 0.8);
          const z = factorX * factorY * (d * 0.45);
          pos.setZ(i, z);
        }
        frontGeo.computeVertexNormals();

        const frontMesh = new THREE.Mesh(frontGeo, mainMaterial);
        frontMesh.position.set(0, h / 2, 0);
        frontMesh.castShadow = true;
        frontMesh.receiveShadow = true;
        pouchGroup.add(frontMesh);

        // Back curved panel
        const backGeo = frontGeo.clone();
        backGeo.rotateY(Math.PI);
        const backMesh = new THREE.Mesh(backGeo, mainMaterial);
        backMesh.position.set(0, h / 2, 0);
        backMesh.castShadow = true;
        backMesh.receiveShadow = true;
        pouchGroup.add(backMesh);

        // Top sealed ridge / ziplock band
        const sealGeo = new THREE.BoxGeometry(w * 1.02, h * 0.08, 0.02);
        const sealMesh = new THREE.Mesh(sealGeo, mainMaterial);
        sealMesh.position.set(0, h * 0.96, 0);
        sealMesh.castShadow = true;
        pouchGroup.add(sealMesh);

        // Bottom oval gusset
        const botGeo = new THREE.CylinderGeometry(w * 0.45, w * 0.45, 0.01, 32);
        botGeo.scale(1, 1, d / w);
        const botMesh = new THREE.Mesh(botGeo, mainMaterial);
        botMesh.position.set(0, 0.005, 0);
        pouchGroup.add(botMesh);
      };

      buildPouch(dimensions);
      updateDimensionsFn = (dims) => buildPouch(dims);

      return {
        group: rootGroup,
        mainMesh: pouchGroup,
        accentMeshes,
        updateDimensions: updateDimensionsFn,
        updateOpenAngle: updateOpenAngleFn,
      };
    }

    case 'paper_cup': {
      const cupGroup = new THREE.Group();
      const lidGroup = new THREE.Group();
      rootGroup.add(cupGroup);
      rootGroup.add(lidGroup);

      const buildCup = (dims: PackagingDimensions) => {
        while (cupGroup.children.length > 0) cupGroup.remove(cupGroup.children[0]);
        while (lidGroup.children.length > 0) lidGroup.remove(lidGroup.children[0]);

        const rTop = (dims.radius || dims.width / 2) * 0.01;
        const rBot = rTop * 0.68;
        const h = dims.height * 0.01;

        // Cup body
        const cupGeo = new THREE.CylinderGeometry(rTop, rBot, h, 48, 1, true);
        const cupMesh = new THREE.Mesh(cupGeo, mainMaterial);
        cupMesh.position.y = h / 2;
        cupMesh.castShadow = true;
        cupMesh.receiveShadow = true;
        cupGroup.add(cupMesh);

        // Bottom base disk
        const baseGeo = new THREE.CircleGeometry(rBot, 32);
        baseGeo.rotateX(Math.PI / 2);
        const baseMesh = new THREE.Mesh(baseGeo, mainMaterial);
        baseMesh.position.y = 0.02;
        cupGroup.add(baseMesh);

        // Rolled lip
        const lipGeo = new THREE.TorusGeometry(rTop, 0.02, 16, 48);
        lipGeo.rotateX(Math.PI / 2);
        const lipMesh = new THREE.Mesh(lipGeo, mainMaterial);
        lipMesh.position.y = h;
        cupGroup.add(lipMesh);

        // Plastic Snap-on Lid
        lidGroup.position.set(0, h + 0.01, 0);
        const lidRimGeo = new THREE.CylinderGeometry(rTop * 1.03, rTop * 1.03, 0.035, 48);
        const lidRim = new THREE.Mesh(lidRimGeo, plasticMaterial);
        lidRim.position.y = 0.018;
        lidRim.castShadow = true;
        lidGroup.add(lidRim);

        const lidDomeGeo = new THREE.CylinderGeometry(rTop * 0.95, rTop * 0.98, 0.04, 48);
        const lidDome = new THREE.Mesh(lidDomeGeo, plasticMaterial);
        lidDome.position.y = 0.045;
        lidGroup.add(lidDome);
      };

      buildCup(dimensions);
      updateDimensionsFn = (dims) => buildCup(dims);
      updateOpenAngleFn = (factor) => {
        lidGroup.position.y = dimensions.height * 0.01 + 0.01 + factor * 0.6;
        lidGroup.rotation.z = factor * 0.25;
      };

      return {
        group: rootGroup,
        mainMesh: cupGroup,
        accentMeshes,
        updateDimensions: updateDimensionsFn,
        updateOpenAngle: updateOpenAngleFn,
      };
    }

    case 'shopping_bag': {
      const bagGroup = new THREE.Group();
      rootGroup.add(bagGroup);

      const buildBag = (dims: PackagingDimensions) => {
        while (bagGroup.children.length > 0) bagGroup.remove(bagGroup.children[0]);

        const w = dims.width * 0.01;
        const h = dims.height * 0.01;
        const d = dims.depth * 0.01;

        // Bag body
        const bagGeo = new THREE.BoxGeometry(w, h, d, 2, 2, 2);
        // Indent side gussets slightly
        const pos = bagGeo.attributes.position;
        for (let i = 0; i < pos.count; i++) {
          const px = pos.getX(i);
          const pz = pos.getZ(i);
          // if on left or right wall
          if (Math.abs(px) > w * 0.45 && Math.abs(pz) < d * 0.4) {
            // Fold inward
            pos.setX(i, px * 0.9);
          }
        }
        bagGeo.computeVertexNormals();

        const bagMesh = new THREE.Mesh(bagGeo, mainMaterial);
        bagMesh.position.y = h / 2;
        bagMesh.castShadow = true;
        bagMesh.receiveShadow = true;
        bagGroup.add(bagMesh);

        // Twisted rope handles
        const handleCurve1 = new THREE.CatmullRomCurve3([
          new THREE.Vector3(-w * 0.22, h, d * 0.51),
          new THREE.Vector3(-w * 0.2, h + h * 0.25, d * 0.51),
          new THREE.Vector3(0, h + h * 0.32, d * 0.51),
          new THREE.Vector3(w * 0.2, h + h * 0.25, d * 0.51),
          new THREE.Vector3(w * 0.22, h, d * 0.51),
        ]);
        const handleGeo1 = new THREE.TubeGeometry(handleCurve1, 32, 0.02, 8, false);
        const handleMesh1 = new THREE.Mesh(handleGeo1, plasticMaterial);
        handleMesh1.castShadow = true;
        bagGroup.add(handleMesh1);

        // Back handle
        const handleCurve2 = new THREE.CatmullRomCurve3([
          new THREE.Vector3(-w * 0.22, h, -d * 0.51),
          new THREE.Vector3(-w * 0.2, h + h * 0.25, -d * 0.51),
          new THREE.Vector3(0, h + h * 0.32, -d * 0.51),
          new THREE.Vector3(w * 0.2, h + h * 0.25, -d * 0.51),
          new THREE.Vector3(w * 0.22, h, -d * 0.51),
        ]);
        const handleGeo2 = new THREE.TubeGeometry(handleCurve2, 32, 0.02, 8, false);
        const handleMesh2 = new THREE.Mesh(handleGeo2, plasticMaterial);
        handleMesh2.castShadow = true;
        bagGroup.add(handleMesh2);
      };

      buildBag(dimensions);
      updateDimensionsFn = (dims) => buildBag(dims);

      return {
        group: rootGroup,
        mainMesh: bagGroup,
        accentMeshes,
        updateDimensions: updateDimensionsFn,
        updateOpenAngle: updateOpenAngleFn,
      };
    }

    case 'cosmetic_tube': {
      const tubeGroup = new THREE.Group();
      const capGroup = new THREE.Group();
      rootGroup.add(tubeGroup);
      rootGroup.add(capGroup);

      const buildTube = (dims: PackagingDimensions) => {
        while (tubeGroup.children.length > 0) tubeGroup.remove(tubeGroup.children[0]);
        while (capGroup.children.length > 0) capGroup.remove(capGroup.children[0]);

        const r = (dims.width / 2) * 0.01;
        const h = dims.height * 0.01;

        // Tube transitions from round bottom to flat crimped top
        const tubeGeo = new THREE.CylinderGeometry(r * 0.1, r, h * 0.85, 32, 32, true);
        const pos = tubeGeo.attributes.position;
        for (let i = 0; i < pos.count; i++) {
          const py = pos.getY(i);
          // Normalized 0 at bottom to 1 at top
          const factor = (py + (h * 0.85) / 2) / (h * 0.85);
          const px = pos.getX(i);
          const pz = pos.getZ(i);
          // Flatten Z, expand X
          const newZ = pz * (1 - factor * 0.92);
          const newX = px * (1 + factor * 0.55);
          pos.setX(i, newX);
          pos.setZ(i, newZ);
        }
        tubeGeo.computeVertexNormals();

        const tubeMesh = new THREE.Mesh(tubeGeo, mainMaterial);
        tubeMesh.position.y = (h * 0.85) / 2 + h * 0.15;
        tubeMesh.castShadow = true;
        tubeMesh.receiveShadow = true;
        tubeGroup.add(tubeMesh);

        // Top crimp seal
        const crimpGeo = new THREE.BoxGeometry(r * 1.55 * 2, h * 0.06, 0.02);
        const crimpMesh = new THREE.Mesh(crimpGeo, mainMaterial);
        crimpMesh.position.y = h * 0.85 + h * 0.15;
        tubeGroup.add(crimpMesh);

        // Screw Cap at base
        capGroup.position.set(0, h * 0.08, 0);
        const capGeo = new THREE.CylinderGeometry(r * 0.75, r * 0.75, h * 0.15, 32);
        const capMesh = new THREE.Mesh(capGeo, plasticMaterial);
        capMesh.castShadow = true;
        capGroup.add(capMesh);
      };

      buildTube(dimensions);
      updateDimensionsFn = (dims) => buildTube(dims);
      updateOpenAngleFn = (factor) => {
        capGroup.position.y = dimensions.height * 0.01 * 0.08 - factor * 0.5;
        capGroup.rotation.y = factor * Math.PI * 2;
      };

      return {
        group: rootGroup,
        mainMesh: tubeGroup,
        accentMeshes,
        updateDimensions: updateDimensionsFn,
        updateOpenAngle: updateOpenAngleFn,
      };
    }

    case 'cosmetic_jar': {
      const jarGroup = new THREE.Group();
      const lidGroup = new THREE.Group();
      rootGroup.add(jarGroup);
      rootGroup.add(lidGroup);

      const buildJar = (dims: PackagingDimensions) => {
        while (jarGroup.children.length > 0) jarGroup.remove(jarGroup.children[0]);
        while (lidGroup.children.length > 0) lidGroup.remove(lidGroup.children[0]);

        const r = (dims.radius || dims.width / 2) * 0.01;
        const h = dims.height * 0.01;

        // Jar body
        const jarGeo = new THREE.CylinderGeometry(r, r, h * 0.65, 48);
        const jarMesh = new THREE.Mesh(jarGeo, mainMaterial);
        jarMesh.position.y = (h * 0.65) / 2;
        jarMesh.castShadow = true;
        jarMesh.receiveShadow = true;
        jarGroup.add(jarMesh);

        // Screw Lid
        lidGroup.position.set(0, h * 0.65, 0);
        const lidGeo = new THREE.CylinderGeometry(r * 1.02, r * 1.02, h * 0.35, 48);
        const lidMesh = new THREE.Mesh(lidGeo, metalMaterial);
        lidMesh.position.y = (h * 0.35) / 2;
        lidMesh.castShadow = true;
        lidGroup.add(lidMesh);
      };

      buildJar(dimensions);
      updateDimensionsFn = (dims) => buildJar(dims);
      updateOpenAngleFn = (factor) => {
        lidGroup.position.y = dimensions.height * 0.01 * 0.65 + factor * 0.4;
        lidGroup.rotation.y = factor * Math.PI * 3;
      };

      return {
        group: rootGroup,
        mainMesh: jarGroup,
        accentMeshes,
        updateDimensions: updateDimensionsFn,
        updateOpenAngle: updateOpenAngleFn,
      };
    }

    default:
      return {
        group: rootGroup,
        mainMesh: rootGroup,
        accentMeshes,
        updateDimensions: updateDimensionsFn,
        updateOpenAngle: updateOpenAngleFn,
      };
  }
}

/**
 * Assigns custom UV coordinates to BoxGeometry faces matching our packaging dieline regions
 */
function setCustomBoxUVs(
  geo: THREE.BoxGeometry,
  faceType: 'front' | 'back' | 'left' | 'right' | 'lid' | 'bottom' | 'top',
  modelId: PackagingModelId
) {
  const uvAttr = geo.attributes.uv;
  if (!uvAttr) return;

  // UV coordinates: uMin, vMin, uMax, vMax in 0..1
  let u0 = 0, v0 = 0, u1 = 1, v1 = 1;

  if (modelId === 'mailer_box') {
    switch (faceType) {
      case 'lid':
        u0 = 0.28; u1 = 0.72; v0 = 0.58; v1 = 0.90;
        break;
      case 'bottom':
        u0 = 0.28; u1 = 0.72; v0 = 0.26; v1 = 0.58;
        break;
      case 'front':
        u0 = 0.28; u1 = 0.72; v0 = 0.12; v1 = 0.26;
        break;
      case 'back':
        u0 = 0.28; u1 = 0.72; v0 = 0.58; v1 = 0.65;
        break;
      case 'left':
        u0 = 0.14; u1 = 0.28; v0 = 0.26; v1 = 0.58;
        break;
      case 'right':
        u0 = 0.72; u1 = 0.86; v0 = 0.26; v1 = 0.58;
        break;
    }
  } else if (modelId === 'tuck_box') {
    switch (faceType) {
      case 'left':
        u0 = 0.04; u1 = 0.26; v0 = 0.24; v1 = 0.72;
        break;
      case 'front':
        u0 = 0.26; u1 = 0.48; v0 = 0.24; v1 = 0.72;
        break;
      case 'right':
        u0 = 0.48; u1 = 0.70; v0 = 0.24; v1 = 0.72;
        break;
      case 'back':
        u0 = 0.70; u1 = 0.92; v0 = 0.24; v1 = 0.72;
        break;
      case 'top':
        u0 = 0.26; u1 = 0.48; v0 = 0.72; v1 = 0.94;
        break;
      case 'bottom':
        u0 = 0.26; u1 = 0.48; v0 = 0.02; v1 = 0.24;
        break;
    }
  }

  // Box geometry has 6 faces: +X, -X, +Y, -Y, +Z, -Z (each face has 4 vertices, 2 triangles)
  // We map the target face of the box to our UV coordinates
  for (let i = 0; i < uvAttr.count; i++) {
    const u = uvAttr.getX(i);
    const v = uvAttr.getY(i);
    uvAttr.setXY(i, u0 + u * (u1 - u0), v0 + v * (v1 - v0));
  }
  uvAttr.needsUpdate = true;
}
