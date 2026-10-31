# Setup guide | ANIL.DEV Developer OS

1. Open the GitHub repository `https://github.com/ani12004/ani12004`.
2. Upload or commit **all files and folders in this ZIP** into that repo root, preserving `assets/` and `.github/workflows/snake.yml`.
3. The `README.md` is the profile page. Custom animated graphics are stored locally under `assets/` (they are not hotlinked to a third-party GIF host).
4. To activate the animated contributions snake: GitHub > repository `ani12004` > Settings > Actions > General > Workflow permissions > select **Read and write permissions** (if the repository allows it) > Save. Then Actions > **Animate contribution snake** > **Run workflow**. It publishes the `output` branch. Github Actions may ask you to enable workflows for the repo first.
5. Wait for the workflow to succeed, then refresh your profile. Future workflow runs are scheduled daily.

## Notes

- GitHub READMEs **do not run JavaScript, custom CSS, WebGL, HTML iframe or real interactive UI**. The interface here is a combination of real links/anchors and custom GIF/PNG visuals designed to look like a web developer dashboard.
- The hero and terminal are original animated illustrations, not telemetry from live running servers. Project visuals are conceptual cards, not screenshots.
- All local assets should display without needing an Actions run. Only the snake is unavailable until the initial Actions run succeeds.
- The streak image is served by a third-party status service and may occasionally fail to load; remove that image block if you want a completely self-hosted profile.
- Repo `ani12004/ani12004` must be public for your profile README to show publicly.
- Most mobile screens show the two-column project grid stacked or very narrow. If necessary, simplify the HTML table to individual cards for mobile.

## Files

README.md                    The profile page
assets/hero.gif              Animated hero dashboard
assets/build-loop.gif        Animated coding / pipeline terminal
assets/*png                  Original project visuals, focus panel, footer & stills
.github/workflows/snake.yml  Automatic contribution snake
