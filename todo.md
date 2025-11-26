# Deployment TODO

Keep this list updated as you complete items. Edit this file in future iterations when new action items pop up.

## 1. GitHub repository configuration
- [ ] Confirm the repo’s **Settings → Actions → General** allow GitHub Actions to run (`Allow all actions and reusable workflows`).
- [ ] (Optional) Add repository/environment secrets for external services (e.g., `SENTRY_DSN`) under **Settings → Secrets and variables → Actions**.
- [ ] Decide who can approve deployments (if you need approvals, configure an `environment` in the workflow).

## 2. Provision the self-hosted runner on the production server
The server already has a `miyan` user with `/home/miyan/Miyan_Backend` and `/home/miyan/Miyan_Frontend`. We will reuse that user for the runner so deployments happen inside the existing directories.

1. **Install prerequisites** (as root/sudo, still fine even if packages already exist):
   ```bash
   sudo apt-get update
   sudo apt-get install -y curl tar git docker.io docker-compose-plugin
   sudo systemctl enable --now docker
   ```
2. **Ensure `miyan` is in the docker group** (skip if already true):
   ```bash
   sudo usermod -aG docker miyan
   ```
   Log out and back in as `miyan` (or `su - miyan`) so the new group membership applies.

3. **Download and extract the latest runner** while logged in as `miyan`:
   ```bash
   su - miyan
   mkdir -p ~/actions-runner && cd ~/actions-runner
   RUNNER_VERSION=2.317.0
   curl -o actions-runner-linux-x64-${RUNNER_VERSION}.tar.gz -L https://github.com/actions/runner/releases/download/v${RUNNER_VERSION}/actions-runner-linux-x64-${RUNNER_VERSION}.tar.gz
   tar xzf actions-runner-linux-x64-${RUNNER_VERSION}.tar.gz
   ```
4. **Generate a registration token** from **Repository → Settings → Actions → Runners → New self-hosted runner**.

5. **Configure the runner** (replace `<repo-url>` with your GitHub repo, e.g., `https://github.com/YourOrg/Miyan_Backend`, and paste the token when prompted). Add the `linux` and `production` labels to match the workflow:
   ```bash
   ./config.sh --url <repo-url> --token <token> --labels "self-hosted,linux,production"
   ```
6. **Install and start the runner service** so it survives reboots (still as `miyan`, but using sudo for service install):
   ```bash
   sudo ./svc.sh install
   sudo ./svc.sh start
   ```

7. The repositories already live in `/home/miyan/Miyan_Backend` and `/home/miyan/Miyan_Frontend`. Ensure `/home/miyan/Miyan_Backend/.env` contains the production copy derived from `.env.example`. The workflow runs `docker compose` from that directory, so keep the clone clean (pull latest `main`, stash local edits if necessary).

## 3. Deployment flow verification
- [ ] Ensure the runner shows as “online” under **Settings → Actions → Runners**.
- [ ] After each deploy pull (`git pull origin main`), run `cp config/settings.production.py config/settings.py` (or `mv` if you prefer) inside `/home/miyan/Miyan_Backend` so Django/Gunicorn use the production configuration.
- [ ] Push a commit to `main`. The `CI` workflow should run `test` on GitHub-hosted runners and then trigger the `Deploy to Production` job on the new self-hosted runner.
- [ ] On the server, watch logs (`sudo journalctl -u actions.runner.* -f`) or `docker compose logs -f backend` to confirm the stack restarts and the healthcheck at `https://your-domain/api/core/health/` reports the new version.
- [ ] Update this `todo.md` once the deployment pipeline is verified end-to-end.
