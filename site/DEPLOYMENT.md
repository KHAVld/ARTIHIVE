# ARTIHIVE 2.0.4 website deployment

This directory is ready to be published as the root of GitHub Pages.

## Existing repository workflow

The repository workflow `.github/workflows/pages.yml` publishes the `site/` directory when the `ARTIHIVE` branch is updated or the workflow is run manually.

## Manual deployment

Upload the contents of this directory to the branch/folder selected in GitHub:

`Settings → Pages → Build and deployment`

`index.html` must remain at the published root. Do not upload only the enclosing directory.

## Required public package URL

After deployment, this URL must return the firmware package rather than the 404 page:

`https://khavld.github.io/ARTIHIVE/assets/downloads/artihive-2.0.4.fwsc`

The embedded FM-1 emulator uses that exact URL.
