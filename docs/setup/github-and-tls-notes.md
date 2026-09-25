# GitHub connection notes

## Symptom
`gh auth status` reported "The token in /root/.config/gh/hosts.yml is invalid", and `gh api` failed with
`tls: failed to verify certificate: x509: certificate signed by unknown authority`, while `curl` worked.

## Cause
`gh` (a Go program) did not trust the system certificate bundle in this Termux/proot environment. The saved login token was actually valid.

## Fix
Point `gh` and `git` at the Termux CA bundle:

```
export SSL_CERT_FILE=/data/data/com.termux/files/usr/etc/tls/cert.pem
git config --global http.sslCAInfo "$SSL_CERT_FILE"
gh auth setup-git
```

The export was also added to `~/.bashrc` and `~/.profile`. After this, `gh auth status` shows a valid login with `repo`, `workflow`, `gist` and `read:org` scopes, and push access to this repository.

## Notes
- Do not paste tokens into chat. Log in with `gh auth login` in the terminal.
- Some shell utilities (`ls`, `mkdir`, `head`, `tail`) are blocked by the sandbox wrapper here; use `printf`, `find`, the file tools, or `git` instead.
