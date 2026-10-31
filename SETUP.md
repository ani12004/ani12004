# BIOME / OS · Profile install and customization

This package is a **real GitHub profile README**, built for `github.com/ani12004/ani12004`. It includes self-hosted artwork and lightweight GIF loops. The project graphics are conceptual illustrations, not application screenshots.

## Windows install (recommended)

1. Unzip the **whole folder** (do not copy only `README.md`).
2. Open `INSTALL_WINDOWS.cmd` by double-clicking, or run it from CMD.
3. Review the staged files when prompted, then select **Y** to publish.
4. The installer **clones the repository to a new `Anil_Biome_Live` directory** beside the extracted folder. It never force-pushes and doesn't depend on your earlier local folders, including a rebase-conflicted directory.

If you still have a rebase conflict in **a different earlier folder**, it remains independent. You can cancel it separately there with `git rebase --abort`, but **do not run that inside a freshly cloned repository**.

## Manual commands from the extracted directory (CMD)

```bat
cd /d D:\downloads
git clone https://github.com/ani12004/ani12004.git Anil_Biome_Live
robocopy "D:\downloads\Anil_Biome_OS_GitHub" "D:\downloads\Anil_Biome_Live" /E /XD .git
cd /d D:\downloads\Anil_Biome_Live
git add README.md SETUP.md assets tools .github\workflows\refresh-biome.yml
git status
git commit -m "style: launch nature-inspired BIOME OS GitHub profile"
git pull --rebase origin main
git push -u origin main
```

**Important:** If `git pull --rebase` has a conflict, stop and resolve it before pushing. Never use `git push --force` just to publish a README.

## Live repository signal (optional)

The profile already includes `assets/activity.svg` as a static initial snapshot. The included `.github/workflows/refresh-biome.yml` action can generate a fresh public-repository activity panel from the GitHub API, scheduled once daily.

To activate it:

1. On GitHub, open the profile repository, **Actions** tab, **Refresh BIOME OS repository signal**.
2. Use **Run workflow** on `main`. If GitHub prompts to enable Actions, do so first.
3. Make sure repository **Settings → Actions → General → Workflow permissions** allows read/write access if GitHub reports an insufficient permission error. Organizational policies may prevent changes.
4. The workflow fetches public repositories only. It writes `assets/activity.svg`, commits only if changed, and has no paid external dependencies.

The workflow may be subject to GitHub Actions schedule delays and public API availability. It is not real-time telemetry.

## Customization

- `README.md`: profile information, sections and links.
- `assets/hero-loop.gif`: animated hero image. `assets/hero-still.png`: static version.
- `assets/project-*.png`: original project cards.
- `assets/ecosystem.png`: technical network panel.
- `assets/pipeline-loop.gif`: animated workflow.
- `assets/activity.svg`: self-hosted repo activity snapshot.
- `tools/generate_assets.py`: editable artwork generator; adjust colors and typography in `C`, then regenerate with:

```bat
python -m pip install pillow cairosvg
python tools\generate_assets.py
```

On Windows, CairoSVG may require a Cairo runtime; the generator is optional because all finished images are already bundled.

The generator is optional for using the README. The actual profile needs no Python process and no server to display its artwork.

### GitHub README constraints

GitHub strips custom JavaScript, style tags and much CSS in READMEs. For this reason the design uses custom GIF/PNG assets, standard headings, linked image cards, semantic tables, working anchor links and interactive `<details>` elements. An interactive website experience in the literal sense requires a separately hosted page; this design takes GitHub Markdown as far as it reasonably goes without fake buttons or broken interactions.

### Sources and link checks

The linked public project repositories are `ani12004/Prompt-Forge-Studio`, `ani12004/gini-2.0` and `ani12004/Imperium`. The QuantumFlow BLR capstone is presented without inventing a public link. The profile is intentionally not displaying made-up project metrics or contribution counts.
