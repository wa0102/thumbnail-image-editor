document.getElementById("uploadForm")?.addEventListener("submit", async e => {
    e.preventDefault();

    const formData = new FormData(e.target);

    const res = await fetch("/api/thumbnail/remove-bg", {
        method: "POST",
        body: formData
    });

    const data = await res.json();

    document.getElementById("result").src =
        "/out/" + data.outputImage.split("\\").pop();

    document.getElementById("result").style.display = "block";
});
const fg = document.getElementById("foreground");

let isDragging = false;
let startX, startY, origX, origY;

fg.addEventListener("mousedown", e => {
    isDragging = true;
    startX = e.clientX;
    startY = e.clientY;
    origX = parseInt(fg.style.left) || 0;
    origY = parseInt(fg.style.top) || 0;
    fg.style.cursor = 'grabbing';
});

document.addEventListener("mousemove", e => {
    if (!isDragging) return;
    const dx = e.clientX - startX;
    const dy = e.clientY - startY;
    fg.style.left = origX + dx + "px";
    fg.style.top = origY + dy + "px";
});

document.addEventListener("mouseup", e => {
    isDragging = false;
    fg.style.cursor = 'grab';
});
let scale = 1;
fg.addEventListener("wheel", e => {
    e.preventDefault();
    if (e.deltaY < 0) scale += 0.05; // 上にスクロールで拡大
    else scale -= 0.05;             // 下にスクロールで縮小
    scale = Math.max(0.1, Math.min(5, scale)); // 最小0.1倍, 最大3倍
    fg.style.transform = `scale(${scale})`;
});

