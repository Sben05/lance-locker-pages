# Lance Locker — Streamlit on GitHub Pages (stlite)

A beautiful, zero-cost, custom-domain portfolio powered by **Streamlit** running entirely in the **browser** (via **stlite**) and hosted on **GitHub Pages**.

## ✨ Features
- Gorgeous glass/gradient UI
- Interactive **3D GLB** viewer via `<model-viewer>`
- Search, tag filters, project cards, detail pages
- **Edit content** by updating `your_projects/locker.json` and static files
- Works on GitHub Pages with your **custom domain**

## 🧩 How it works
`index.html` loads `app.py` + `lib/*.py` + `your_projects/locker.json` from the repo at runtime, then boots Streamlit in-browser via stlite (Pyodide/WebAssembly). Static assets (images, `.glb`) are served directly by Pages.

## 🚀 Quick start
1) Create a new GitHub repo and push these files.  
2) (Optional) Put your custom domain in `CNAME` and set up DNS (CNAME → `<youruser>.github.io`).  
3) Go to **Settings → Pages**  
   - Build and deployment: **GitHub Actions**  
   - The supplied workflow (`.github/workflows/pages.yml`) will deploy on every push to `main`.  
4) Visit your Pages URL (or your custom domain).

## 📝 Editing content
- Open `your_projects/locker.json` in GitHub and edit (add projects, images).  
- Upload images as `your_projects/my_img.png` and models as `your_projects/my_model.glb`.  
- Reference them in `locker.json` as relative paths, e.g. `"images": ["your_projects/my_img.png"]`.

## 🧠 Notes
- Packages: keep to **pure-Python** if you add dependencies (no native wheels).  
- Large `.glb` files are fine (they’re fetched as static files by the browser).  
- If deep links (`?p=slug`) don’t work in some browsers, navigation still functions in-session via buttons.

## 🛠 Dev tips
- Change typography/colors in `lib/ui.py`.  
- Add external links per project under `"links"`.  
- For absolute asset hosting (CDN), use full `https://...` URLs in your JSON.

Enjoy! 🧰
