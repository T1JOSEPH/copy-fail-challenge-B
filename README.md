# Copy Fail Lab — CVE-2026-31431 (v2)

Devcontainer reproducible para experimentar con la vulnerabilidad **Copy Fail**
(CVE-2026-31431) en un kernel Linux 6.12 controlado dentro de QEMU.

Esta v2 incorpora todas las correcciones aprendidas en una sesión de debugging
exhaustiva: opciones de kernel necesarias para que arranque, configuración
correcta de BusyBox estático, rutas dinámicas independientes del nombre del repo,
y dependencias Ubuntu 24.04 corregidas.

---

## Inicio rápido para el estudiante

1. Abre un Codespace desde este repo.
   ```bash
   #CONFIGURACION DE EJEMPLO!!!!!!!!!!!
   apt update
   apt install gh
   
   gh api user --jq '"\(.name) → \(.email // .login)"'
   
   git config --global user.name "Jonathan E. Tito O."
   git config --global user.email "jonathantito@users.noreply.github.com"
   git config --global --add safe.directory /workspaces/copy-fail-challenge-1
   make setup
   ```
3. Configura tu identidad git:
   ```bash
   git config --global user.name "Tu Nombre"
   git config --global user.email "tu@correo.com"
   ```
4. Ejecuta:
   ```bash
   make setup    # descarga kernel + arma rootfs (~5 min)
   make qemu     # arranca la VM vulnerable
   ```

Para salir de QEMU: `Ctrl+A` luego `X`.

---

## Configuración inicial del docente (una sola vez)

### 1. Subir este repo a GitHub

```bash
cd copyfail-v2
git init && git add -A && git commit -m "initial"
git branch -M main
gh repo create TU-ORG/copy-fail-lab --public --source=. --push
```

### 2. Marcarlo como Template

GitHub → tu repo → Settings → marcar `Template repository`.


### 3. Editar `.devcontainer/devcontainer.json`

Cambia el valor `KERNEL_REPO`:
```json
"KERNEL_REPO": "TU-ORG/copy-fail-lab"
```

Commit y push.vi init

### 4. Disparar el workflow del kernel

GitHub → Actions → `Build Vulnerable Kernel` → Run workflow.
Tarda ~25 min en los servidores de GitHub (no en tu Codespace).
Al terminar crea un Release con el `bzImage_vuln` listo para descarga.

### 5. Verificar

Tu repo → Releases → debe aparecer `kernel-v6.12-vuln` con tres archivos
adjuntos. Los estudiantes ahora pueden hacer `make setup` y descarga en 2 min.

---

## Estructura del repo

```
.
├── .devcontainer/
│   ├── Dockerfile             ← Ubuntu 24.04 + deps verificadas
│   └── devcontainer.json      ← sin rutas hardcodeadas
├── .github/workflows/
│   └── build-kernel.yml       ← compila kernel y crea Release
├── scripts/
│   ├── 00_welcome.sh
│   ├── 01_fetch_kernel.sh     ← descarga del Release
│   ├── 02_build_kernel.sh     ← fallback: compila desde fuente
│   ├── 03_build_rootfs.sh     ← BusyBox estático + initramfs
│   └── 04_run_qemu.sh
├── Makefile
└── README.md
```

---

## Comandos disponibles

| Comando | Acción |
|---|---|
| `make setup` | Descarga kernel + arma rootfs (~5 min) |
| `make qemu` | Arranca la VM vulnerable |
| `make info` | Muestra el estado del ambiente |
| `make rootfs` | Reconstruye solo el initramfs |
| `make fetch-kernel` | Solo descarga el bzImage del Release |
| `make build-kernel` | Compila kernel desde fuente (~25 min) |
| `make clean` | Borra builds (mantiene fuentes) |
| `make clean-all` | Borra todo |

---

## Recursos del CVE

- Write-up técnico: https://xint.io/blog/copy-fail-linux-distributions
- Sitio del CVE: https://copy.fail
- PoC oficial: https://github.com/theori-io/copy-fail-CVE-2026-31431

---

## Lecciones aprendidas (referencia para futuras versiones)

Esta v2 incorpora los siguientes fixes respecto a la v1:

- `hexdump` → `bsdextrautils` en Ubuntu 24.04
- `bzip2` agregado al Dockerfile (lo necesita BusyBox)
- Eliminado el `mounts` con ruta hardcodeada en `devcontainer.json`
- Todos los scripts detectan workspace con `SCRIPT_DIR` dinámico
- Kernel: agregadas opciones críticas `BINFMT_ELF`, `BINFMT_SCRIPT`, `RD_GZIP`
- Kernel: agregada dep `CRYPTO_AEAD` antes de `CRYPTO_AUTHENCESN`
- BusyBox: reemplazado `scripts/config` (no existe) por `sed`
- BusyBox: eliminado `olddefconfig` (no existe en BusyBox)
- BusyBox: deshabilitado `CONFIG_TC` (rompe compilación con kernels nuevos)
- BusyBox: forzado `CONFIG_STATIC=y` y verificado con `file`
- Workflow Actions: greps de verificación con `|| echo`, tolerantes

#Comando ejecutados
  ╔═══════════════════════════════════════════════╗
  ║  Kernel vulnerable: 6.12.0               ║
  ║  CVE-2026-31431 Copy Fail Lab                ║
  ╚═══════════════════════════════════════════════╝

-sh: can't access tty; job control turned off
~ $ cat /proc/modules
cat: can't open '/proc/modules': No such file or directory
~ $ {
>   echo "=== HITO 1: KERNEL VULNERABLE CONFIRMADO ==="
>   echo "Fecha: $(date)"
>   echo "Kernel: $(uname -r)"
>   echo "Identidad: $(id)"
>   echo "whoami: $(whoami)"
>   echo "Nota: /proc/modules no disponible en este initramfs minimalista"
> } > /tmp/hito1.txt && cat /tmp/hito1.txtQEMU: Terminated
root@codespaces-53ffae:/workspaces/copy-fail-challenge-B# mkdir -p evidence
root@codespaces-53ffae:/workspaces/copy-fail-challenge-B# cp /tmp/hito1.txt evidence/hito1_vuln_confirmed.txt
cp: cannot stat '/tmp/hito1.txt': No such file or directory
root@codespaces-53ffae:/workspaces/copy-fail-challenge-B# mkdir -p evidence
root@codespaces-53ffae:/workspaces/copy-fail-challenge-B# vi evidence/hito1_vuln_confirmed.txt
root@codespaces-53ffae:/workspaces/copy-fail-challenge-B# history
    1  apt update
    2  apt install gh
    3  gh api user --jq '"\(.name) → \(.email // .login)"'
    4  git config --global user.name T1JOSEPH
    5  git config --global user.email jovacame@uide.edu.ec
    6  git config --global --add safe.directory /workspaces/copy-fail-challenge-1
    7  make qemu
    8  apt update
    9  apt install -y file
   10  make rootfs
   11  make qemu
   12  apt update
   13  apt install -y file bzip2 cpio gzip flex bc build-essential libssl-dev libelf-dev qemu-system-xl
   14  file
   15  make qemu
   16  exit
   17  make setup
   18  make qemu
   19  cd /workspaces/copy-fail-challenge-B/kernel/initramfs
   20  nano init
   21  vi init
   22  cd /workspaces/copy-fail-challenge-B
   23  make rootfs
   24  make qemu
   25  mkdir -p evidence
   26  cp /tmp/hito1.txt evidence/hito1_vuln_confirmed.txt
   27  mkdir -p evidence
   28  vi evidence/hito1_vuln_confirmed.txt
    1  apt update
    2  apt install gh
    3  gh api user --jq '"\(.name) → \(.email // .login)"'
    4  git config --global user.name T1JOSEPH
    5  git config --global user.email jovacame@uide.edu.ec
    6  git config --global --add safe.directory /workspaces/copy-fail-challenge-1
    7  make qemu
    8  apt update
    9  apt install -y file
   10  make rootfs
   11  make qemu
   12  apt update
   13  apt install -y file bzip2 cpio gzip flex bc build-essential libssl-dev libelf-dev qemu-system-xl
   14  file
   15  make qemu
   16  exit
   17  make rootfs
   18  make qemu
   19  ls kernel/initramfs/usr/bin/
   20  cp /usr/bin/python3 kernel/initramfs/usr/bin/python3
   21  ls kernel/initramfs/usr/bin/ | grep python
   22  make clean
   23  make rootfs
   24  vi scripts/03_build_rootfs.sh
   25  make rootfs
   26  vi scripts/03_build_rootfs.sh
   27  grep initramfs.cpio.gz scripts/03_build_rootfs.sh
   28  initramfs.cpio.gzy
   29  vi scripts/03_build_rootfs.sh
   30  make rootfs
   31  grep -n gzy scripts/03_build_rootfs.sh
   32  vi scripts/03_build_rootfs.sh
   33  history
    1  apt update
    2  apt install gh
    3  gh api user --jq '"\(.name) → \(.email // .login)"'
    4  git config --global user.name T1JOSEPH
    5  git config --global user.email jovacame@uide.edu.ec
    6  git config --global --add safe.directory /workspaces/copy-fail-challenge-1
    7  make qemu
    8  apt update
    9  apt install -y file
   10  make rootfs
   11  make qemu
   12  apt update
   13  apt install -y file bzip2 cpio gzip flex bc build-essential libssl-dev libelf-dev qemu-system-x86 wget curl
   14  file
   15  make qemu
   16  exit
   17  cd kernel/linux/crypto
   18  grep -n "_aead_recvmsg" algif_aead.c
   19  vi algif_aead.c
   20  history