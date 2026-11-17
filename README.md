# IPTV Player para Nintendo Switch

Player de IPTV homebrew para Nintendo Switch (Atmosphère/hbmenu), escrito em
C++ com [borealis](https://github.com/dragonflylee/borealis) (UI nativa com
navegação por controle) e [mpv](https://mpv.io/)/FFmpeg para reprodução.

## Recursos

- Login **Xtream Codes** (URL/usuário/senha) ou **playlist M3U direta**
- Abas de Ao Vivo, Filmes e Séries (ou categorias da playlist, no modo M3U)
- Player com EPG (programação) nos canais ao vivo, zapping com Cima/Baixo,
  pausa/seek em filmes e episódios, barra de progresso
- Retomada de reprodução ("Continuar de onde parou" / "Do início")
- Busca global (botão R)
- Favoritos e histórico — armazenados **somente no cartão SD** (nenhum dado
  sai do console)
- "Surpreenda-me": sorteia um filme aleatório
- Interface em português

## Instalação

1. Baixe o `IptvPlayerSwitch.nro` da página de releases.
2. Copie para a pasta `/switch/` do cartão SD.
3. Abra pelo Homebrew Launcher.

## Compilando

### Nintendo Switch (Switch 1)

Pré-requisitos: [devkitPro](https://devkitpro.org/) com `devkitA64` e as
portlibs de Switch (`switch-curl`, `switch-libmpv`, `switch-ffmpeg`,
`switch-glfw`, `switch-mesa`).

```bash
git clone --recursive <url-deste-repo>
cd switch2iptv

# Aplica os ajustes locais na borealis (correções de fonte/estilo e APIs
# extras de TabFrame/Recycler que o app usa — ver patches/)
git -C library/borealis apply ../../patches/borealis-iptv.patch

cmake -S . -B build-switch -G Ninja -DPLATFORM_SWITCH=ON
cmake --build build-switch --target IptvPlayerSwitch.nro
```

O `.nro` sai em `build-switch/IptvPlayerSwitch.nro`.

### Nintendo Switch 2 (`libounce` + `OunceVK`)

Pré-requisitos: `devkitPro` (`devkitA64`), portlibs (`switch-curl`,
`switch-libmpv`, `switch-ffmpeg`) e o
[ounce-devkit](https://github.com/ouncebrew/ounce-devkit) instalado em `$DEVKITPRO`.

```bash
bash scripts/build-switch2.sh
```

O script aplica `patches/borealis-iptv.patch` e `patches/borealis-switch2.patch`,
compila o `.nro` usando EGL + OpenGL ES 3.0 (`OunceVK`) e valida o binário
com `tools/verify_switch2_package.py` (`OUN0` + `ASET` + link map).
O `.nro` sai em `build/switch2/IptvPlayerSwitch-switch2.nro`.

Para testar sem trocar o cartão SD toda hora, use `nxlink -s <caminho-do-nro>`
com o console no menu do `hbmenu` / `ounce-hbmenu` segurando Y.

## Aviso

Este app é apenas um player: não fornece, hospeda nem distribui nenhum
conteúdo. Você precisa das credenciais do seu próprio provedor de IPTV ou de
uma playlist M3U de sua escolha. A playlist sugerida na tela de login (canais
públicos em português) faz parte do repositório
[iptv-org/iptv](https://github.com/iptv-org/iptv).

## Créditos

- [borealis](https://github.com/dragonflylee/borealis) (fork do dragonflylee,
  branch `switchfin`) — biblioteca de UI, com pequenos ajustes locais em
  `patches/`
- [Switchfin](https://github.com/dragonflylee/switchfin) — referência
  arquitetural de app borealis + mpv para Switch
- [mpv](https://mpv.io/) / [FFmpeg](https://ffmpeg.org/) — reprodução de vídeo
- [lunasvg](https://github.com/sammycage/lunasvg) — renderização de SVG
- [nlohmann/json](https://github.com/nlohmann/json) — parse de JSON
  (vendorizada em `source/third_party/`)
- [libcurl](https://curl.se/libcurl/) — HTTP
- [devkitPro](https://devkitpro.org/) / libnx — toolchain de homebrew
- [iptv-org/iptv](https://github.com/iptv-org/iptv) — playlist M3U pública
  sugerida na tela de login

Desenvolvido por GomGeek com o [Claude Code](https://claude.com/claude-code)
(Anthropic).

Adaptação e port para Nintendo Switch 2 (`libounce` + `OunceVK`) por
David Kalil Braga ([@davidkalil10](https://github.com/davidkalil10)).

## Agradecimentos

CostelaBR e AurelioEB.

## Licença

[GPLv3](LICENSE).
