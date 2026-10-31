# The Greenhouse | Anil's nature-inspired GitHub profile

A GitHub-compatible profile README, built without JavaScript or custom CSS.

## What's inside

- `README.md`: The actual GitHub profile page. It uses Markdown and safe GitHub HTML, not a screenshot.
- `assets/forest-hero.gif`: Original animated landscape introduction, entirely self-hosted.
- `assets/growth-terminal.gif`: Original animated build-loop terminal, entirely self-hosted.
- `assets/project-*.png`: Four original scenic project illustrations, with links in the README to verified public GitHub repositories where applicable.
- `assets/forest-footer.png`: Nature-themed footer.
- `tools/generate_assets.py`: Source script for reproducing artwork with Pillow. Run with `python tools/generate_assets.py` in this folder. The script uses font paths from this Linux build environment; adapt them for Windows.
- `.github/workflows/snake.yml`: Optional GitHub Actions contribution-snake generator. Not used by the README unless you choose to add it.

## Install using Windows CMD

Open the **extracted `Anil_Nature_Profile` folder** in CMD and run:

```bat
git init
git branch -M main
git remote add origin https://github.com/ani12004/ani12004.git
git fetch origin main
git reset --mixed origin/main
git add README.md assets SETUP.md tools .github
git status
git commit -m "style: redesign profile with animated nature theme"
git push -u origin main
```

The `git remote add origin` command is only for a folder with no existing origin. If one exists, use:

```bat
git remote set-url origin https://github.com/ani12004/ani12004.git
```

If you're **replacing the old Developer OS files in the same folder**, extract this package into that folder and delete only the older unneeded artwork manually. `git add -A` will stage those deletions, so inspect `git status` before committing. Do not use force-push.

## What works on GitHub?

- The header GIF and terminal GIF animate directly in GitHub's README viewer (GIFs, not embedded JavaScript).
- Buttons are standard links, and navigation links jump to sections.
- The greenhouse log uses GitHub's native `<details>` / `<summary>` expansion.
- Project images are self-hosted and work without an animation server.
- Technology icons and badges load from `skillicons.dev` and `shields.io`. If you want 100% self-hosted imagery, replace these third-party icon strips with locally saved images.
- The snake workflow is **optional** and excluded from the README until you explicitly enable and run it, avoiding broken placeholders.

## Optional: add a green contribution snake

In GitHub, open your profile repository, then **Actions > Animate contribution snake > Run workflow**. Depending on your settings, you may need to enable Actions and repository **Settings > Actions > General > Workflow permissions > Read and write permissions**.

After it succeeds, add this Markdown snippet where you want the snake:

```md
![Contribution garden snake](https://raw.githubusercontent.com/ani12004/ani12004/output/github-snake.svg)
```

The workflow creates an `output` branch, so don't add the snippet before a successful run.

## Accurate presentation

- Art is conceptual. It does not depict verified app screenshots, live dashboards, or production status.
- Public repository links: Prompt-Forge-Studio, gini-2.0, and Imperium.
- QuantumFlow BLR is included as private capstone research with no speculative public link.
- GitHub does not run arbitrary HTML/CSS/JS in READMEs, so this is a visual landing-page experience built with supported Markdown, GIFs and safe HTML.
