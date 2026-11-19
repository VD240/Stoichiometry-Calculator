import * as THREE from "https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js";

import { OrbitControls } from "https://cdn.jsdelivr.net/npm/three@0.170.0/examples/jsm/controls/OrbitControls.js";

// 1. Get viewer container
const container = document.getElementById("molecule-viewer");

// 2. Create scene
const scene = new THREE.Scene();

// 3. Create camera
const camera = new THREE.PerspectiveCamera(
    45,
    container.clientWidth / container.clientHeight,
    0.1,
    100
);

camera.position.set(0, 2, 5);

// 4. Create renderer
const renderer = new THREE.WebGLRenderer({
    antialias: true,
    alpha: true
});

renderer.setSize(container.clientWidth, container.clientHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

container.appendChild(renderer.domElement);

// 5. Lighting
scene.add(new THREE.AmbientLight(0xffffff, 1.5));

const directionalLight = new THREE.DirectionalLight(0xffffff, 2);
directionalLight.position.set(3, 4, 5);
scene.add(directionalLight);

// 6. Mouse controls
const controls = new OrbitControls(camera, renderer.domElement);

controls.enableDamping = true;
controls.dampingFactor = 0.05;
// Enable zoom
controls.enableZoom = true;

// Set zoom limits
controls.minDistance = 2;
controls.maxDistance = 10;

// 7. Molecule data
const molecules = {
    H2O: {
        name: "Water",
        geometry: "Bent",
        bondAngle: "104.5°",
        atoms: [
            { element: "O", position: [0, 0, 0] },
            { element: "H", position: [0.76, 0, 0.59] },
            { element: "H", position: [-0.76, 0, 0.59] }
        ],
        bonds: [[0, 1], [0, 2]]
    },

    CO2: {
        name: "Carbon Dioxide",
        geometry:"Linear",
        bondAngle: "180°",
        atoms: [
            { element: "C", position: [0, 0, 0] },
            { element: "O", position: [-1.10, 0, 0] },
            { element: "O", position: [1.10, 0, 0] }
        ],
        bonds: [[0, 1], [0, 2]]
    },

    CH4: {
        name: "Methane",
        geometry:"Tetrahedral",
        bondAngle: "109.5°",
        atoms: [
            { element: "C", position: [0, 0, 0] },
            { element: "H", position: [0.63, 0.63, 0.63] },
            { element: "H", position: [-0.63, -0.63, 0.63] },
            { element: "H", position: [-0.63, 0.63, -0.63] },
            { element: "H", position: [0.63, -0.63, -0.63] }
        ],
        bonds: [[0, 1], [0, 2], [0, 3], [0, 4]]
    },

    NH3: {
        name: "Ammonia",
        geometry:"Triogonal Pyramidal",
        bondAngle: "107°",
        atoms: [
            { element: "N", position: [0, 0.25, 0] },
            { element: "H", position: [0.94, -0.35, 0] },
            { element: "H", position: [-0.47, -0.35, 0.81] },
            { element: "H", position: [-0.47, -0.35, -0.81] }
        ],
        bonds: [[0, 1], [0, 2], [0, 3]]
    }
};

// 8. Atom colors and sizes
const atomStyles = {
    H: { color: 0xffffff, radius: 0.22 },
    O: { color: 0xff3030, radius: 0.4 },
    C: { color: 0x555555, radius: 0.35 },
    N: { color: 0x3066ff, radius: 0.35 }
};

// 9. Create molecule group
const moleculeGroup = new THREE.Group();
scene.add(moleculeGroup);

// 10. Molecule generator
function createMolecule(formula) {

    moleculeGroup.clear();

    const molecule = molecules[formula];

    if (!molecule) return;

    // Create atoms
    molecule.atoms.forEach(atom => {

    const style = atomStyles[atom.element];

    const geometry = new THREE.SphereGeometry(
        style.radius, 32, 32
    );

    const material = new THREE.MeshStandardMaterial({
        color: style.color,
        roughness: 0.35
    });

    const sphere = new THREE.Mesh(geometry, material);

    sphere.position.set(...atom.position);

    moleculeGroup.add(sphere);

    // Create atom label
    const canvas = document.createElement("canvas");
    const context = canvas.getContext("2d");

    canvas.width = 128;
    canvas.height = 128;

    context.fillStyle = "white";
    context.font = "bold 70px Arial";
    context.textAlign = "center";
    context.textBaseline = "middle";

    context.fillText(atom.element, 64, 64);

    const texture = new THREE.CanvasTexture(canvas);

    const labelMaterial = new THREE.SpriteMaterial({
        map: texture,
        transparent: true
    });

    const label = new THREE.Sprite(labelMaterial);

    label.position.set(
        atom.position[0],
        atom.position[1] + 0.45,
        atom.position[2]
    );

    label.scale.set(0.35, 0.35, 1);

    moleculeGroup.add(label);
});

    // Create bonds
    molecule.bonds.forEach(([startIndex, endIndex]) => {

        const start = new THREE.Vector3(
            ...molecule.atoms[startIndex].position
        );

        const end = new THREE.Vector3(
            ...molecule.atoms[endIndex].position
        );

        const direction = new THREE.Vector3()
            .subVectors(end, start);

        const geometry = new THREE.CylinderGeometry(
            0.07, 0.07, direction.length(), 16
        );

        const material = new THREE.MeshStandardMaterial({
            color: 0xb8c7e8
        });

        const bond = new THREE.Mesh(geometry, material);

        bond.position.copy(start)
            .add(end)
            .multiplyScalar(0.5);

        bond.quaternion.setFromUnitVectors(
            new THREE.Vector3(0, 1, 0),
            direction.normalize()
        );

        moleculeGroup.add(bond);
    });

    // Update information
   document.getElementById("molecule-info").innerHTML = `
    <h3>${molecule.name} (${formula})</h3>
    <p><strong>Molecular Geometry:</strong> ${molecule.geometry}</p>
    <p><strong>Bond Angle:</strong> ${molecule.bondAngle}</p>
    <p><strong>Total Atoms:</strong> ${molecule.atoms.length}</p>
`;
}

// 11. Display initial molecule
createMolecule("H2O");

// 12. Dropdown functionality
const moleculeSelect = document.getElementById("molecule-select");

moleculeSelect.addEventListener("change", event => {
    createMolecule(event.target.value);
});

// 13. Animation loop
function animate() {

    requestAnimationFrame(animate);

    controls.update();

    renderer.render(scene, camera);
}

animate();

// 14. Resize handling
window.addEventListener("resize", () => {

    const width = container.clientWidth;
    const height = container.clientHeight;

    camera.aspect = width / height;
    camera.updateProjectionMatrix();

    renderer.setSize(width, height);
});