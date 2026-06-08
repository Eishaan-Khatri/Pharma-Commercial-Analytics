const sections = [...document.querySelectorAll("[data-section]")];
const links = [...document.querySelectorAll("[data-nav]")];
const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

initPharmaScene();

const observer = new IntersectionObserver(
  (entries) => {
    const visible = entries
      .filter((entry) => entry.isIntersecting)
      .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];

    if (!visible) return;

    links.forEach((link) => {
      link.classList.toggle("is-active", link.getAttribute("href") === `#${visible.target.id}`);
    });
  },
  { rootMargin: "-18% 0px -70% 0px", threshold: [0.1, 0.25, 0.5] }
);

sections.forEach((section) => observer.observe(section));

document.querySelectorAll("[data-copy]").forEach((button) => {
  button.addEventListener("click", async () => {
    const value = button.getAttribute("data-copy");
    try {
      await navigator.clipboard.writeText(value);
      const previous = button.textContent;
      button.textContent = "Copied";
      setTimeout(() => {
        button.textContent = previous;
      }, 1200);
    } catch {
      button.textContent = "Copy failed";
    }
  });
});

async function initPharmaScene() {
  const canvas = document.getElementById("pharmaScene");
  if (!canvas) return;

  try {
    const THREE = await import("https://unpkg.com/three@0.160.0/build/three.module.js");
    runThreePharmaScene(THREE, canvas);
  } catch {
    runPharmaFallback(canvas);
  }
}

function runThreePharmaScene(THREE, canvas) {
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(44, 1, 0.1, 100);
  camera.position.set(0, 1.1, 7.2);

  const group = new THREE.Group();
  scene.add(group);

  const materials = [
    new THREE.MeshStandardMaterial({ color: 0x0f766e, roughness: 0.42, metalness: 0.12 }),
    new THREE.MeshStandardMaterial({ color: 0xb17821, roughness: 0.42, metalness: 0.16 }),
    new THREE.MeshStandardMaterial({ color: 0x536d2f, roughness: 0.5, metalness: 0.1 }),
    new THREE.MeshStandardMaterial({ color: 0xa13a34, roughness: 0.48, metalness: 0.14 }),
  ];

  const bars = [];
  for (let i = 0; i < 18; i++) {
    const height = 0.35 + (i % 6) * 0.16;
    const geometry = new THREE.BoxGeometry(0.22, height, 0.22);
    const bar = new THREE.Mesh(geometry, materials[i % materials.length]);
    bar.position.set(-3 + i * 0.36, -1.2 + height / 2, Math.sin(i) * 0.75);
    group.add(bar);
    bars.push(bar);
  }

  const ring = new THREE.Mesh(
    new THREE.TorusGeometry(1.45, 0.035, 8, 96),
    new THREE.MeshStandardMaterial({ color: 0xfffaf1, roughness: 0.4, metalness: 0.2 })
  );
  ring.position.set(1.9, 0.55, -0.4);
  ring.rotation.x = Math.PI * 0.55;
  group.add(ring);

  const grid = new THREE.GridHelper(8, 12, 0xb17821, 0x3a3026);
  grid.position.y = -1.25;
  group.add(grid);

  scene.add(new THREE.AmbientLight(0xffe6c4, 0.7));
  const key = new THREE.DirectionalLight(0xfffaf1, 2.3);
  key.position.set(3, 4, 4);
  scene.add(key);
  const teal = new THREE.PointLight(0x0f766e, 1.6, 8);
  teal.position.set(-3, 1.8, 2);
  scene.add(teal);

  const resize = () => {
    const width = canvas.clientWidth || window.innerWidth;
    const height = canvas.clientHeight || 720;
    renderer.setSize(width, height, false);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
  };

  resize();
  window.addEventListener("resize", resize, { passive: true });

  let t = 0;
  function animate() {
    t += 0.012;
    group.rotation.y = -0.18 + Math.sin(t) * 0.08;
    ring.rotation.z += 0.006;
    bars.forEach((bar, index) => {
      bar.scale.y = 1 + Math.sin(t * 2 + index * 0.4) * 0.08;
    });
    renderer.render(scene, camera);
    if (!reduceMotion) requestAnimationFrame(animate);
  }

  animate();
}

function runPharmaFallback(canvas) {
  const ctx = canvas.getContext("2d");
  if (!ctx) return;

  const colors = ["#0f766e", "#b17821", "#536d2f", "#a13a34"];

  const resize = () => {
    const ratio = Math.min(window.devicePixelRatio || 1, 2);
    canvas.width = Math.floor(canvas.clientWidth * ratio);
    canvas.height = Math.floor(canvas.clientHeight * ratio);
    ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
  };

  resize();
  window.addEventListener("resize", resize, { passive: true });

  let t = 0;
  function draw() {
    t += 0.02;
    const width = canvas.clientWidth;
    const height = canvas.clientHeight;
    ctx.clearRect(0, 0, width, height);
    ctx.fillStyle = "#17130f";
    ctx.fillRect(0, 0, width, height);

    ctx.strokeStyle = "rgba(255, 250, 241, 0.08)";
    for (let x = 0; x < width; x += 58) {
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, height);
      ctx.stroke();
    }

    for (let i = 0; i < 18; i++) {
      const x = width * 0.48 + i * 24;
      const base = height * 0.72;
      const barHeight = 32 + (i % 6) * 18 + Math.sin(t * 2 + i) * 8;
      ctx.fillStyle = colors[i % colors.length];
      ctx.beginPath();
      ctx.moveTo(x, base - barHeight);
      ctx.lineTo(x + 16, base - barHeight - 10);
      ctx.lineTo(x + 16, base);
      ctx.lineTo(x, base + 10);
      ctx.closePath();
      ctx.fill();
    }

    ctx.strokeStyle = "rgba(255, 250, 241, 0.35)";
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.ellipse(width * 0.72, height * 0.38, 86, 28, Math.sin(t) * 0.25, 0, Math.PI * 2);
    ctx.stroke();

    if (!reduceMotion) requestAnimationFrame(draw);
  }

  draw();
}
